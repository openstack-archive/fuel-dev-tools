#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function

import argparse
from ipaddress import ip_network
import os
import shutil
import sys
import tempfile

import paramiko
import psycopg2
import requests
import yaml


class EnvironmentDoesntExistException(Exception):
    pass


def get_env_networks(name, host='localhost', user='fuel_devops',
                     database='fuel_devops', password='fuel_devops'):
    conn = psycopg2.connect(host=host, user=user, database=database,
                            password=password)

    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT id FROM devops_environment WHERE name=%s',
                   [name])

    env_id = cursor.fetchone()

    if env_id is not None:
        env_id = env_id[0]
    else:
        error = 'No environment named "{}" has been found.'.format(name)
        raise EnvironmentDoesntExistException(error)

    cursor.execute(('SELECT name,ip_network FROM devops_network'
                    ' WHERE environment_id=%s'), [env_id])
    env_networks = cursor.fetchall()

    cursor.close()
    conn.close()

    return dict(env_networks)


def cidr_to_iprange(cidr, start=0, end=-1):
    hosts = list(ip_network(cidr).hosts())

    if start > 0:
        start -= 1

    if end != -1:
        end -= 1

    start_host = str(hosts[start])
    end_host = str(hosts[end])

    return (start_host, end_host)


class MasterNode(object):
    def __init__(self, ipaddress, port=22, username='root', password='r00tme'):
        self.command = '/usr/bin/fuel {subcommand} --env-id {env_id} {action}'
        self.tmpdir = tempfile.mkdtemp()
        self.transport = paramiko.Transport(ipaddress, port)
        self.transport.connect(username=username, password=password)

        self.version = requests.get(
            'http://{}:8000/api/v1/version'.format(ipaddress)
        ).json()['release']

        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def __exec(self, command):
        session = self.transport.open_session()
        session.exec_command(command)
        exit_code = session.recv_exit_status()

        if exit_code != 0:
            error = ('Command {cmd} failed to execute correctly. '
                     'Exit code: {exit_code}.')
            raise RuntimeError(error.format(cmd=command, exit_code=exit_code))

    def download(self, subcommand, env_id=1):
        command = self.command.format(subcommand=subcommand, env_id=env_id,
                                      action='--download')
        self.__exec(command)

        yamlfile = '{}_{}.yaml'.format(subcommand, env_id)
        src = os.path.join('/root', yamlfile)
        dest = os.path.join(self.tmpdir, yamlfile)

        self.sftp.get(src, dest)

    def upload(self, subcommand, env_id=1):
        yamlfile = '{}_{}.yaml'.format(subcommand, env_id)
        src = os.path.join(self.tmpdir, yamlfile)
        dest = os.path.join('/root', yamlfile)

        self.sftp.put(src, dest)

        command = self.command.format(subcommand=subcommand, env_id=env_id,
                                      action='--upload')
        self.__exec(command)

    def verify(self, env_id=1):
        command = self.command.format(subcommand='network', env_id=env_id,
                                      action='--verify')
        self.__exec(command)

    def close(self):
        self.sftp.close()
        self.transport.close()
        shutil.rmtree(self.tmpdir)


class MasterNodeNetwork(MasterNode):
    def update_yaml(self, networks, yamlfile):
        fuel_networks = frozenset(['public', 'management', 'storage',
                                  'private'])

        with open(yamlfile, 'r') as f:
            cluster = yaml.safe_load(f)

        for network in cluster['networks']:
            network_name = network['name']

            if network_name not in fuel_networks:
                continue

            cidr = networks[network_name]
            iprange = cidr_to_iprange(cidr)

            if 'cidr' in network:
                network['cidr'] = cidr

            if 'cidr' in network['meta']:
                network['meta']['cidr'] = cidr

            if network_name == 'public':
                public_iprange = cidr_to_iprange(cidr, start=2, end=126)
                floating_range = cidr_to_iprange(cidr, start=130)
                public_gateway = cidr_to_iprange(cidr)[0]

                network['ip_ranges'] = [public_iprange]
                network['meta']['ip_range'] = public_iprange
                network['gateway'] = public_gateway
                cluster['networking_parameters']['floating_ranges'] = \
                    [floating_range]
            else:
                network['ip_ranges'] = [iprange]

        with open(yamlfile, 'w') as f:
            yaml.safe_dump(cluster, f)

    def update(self, env_id, networks):
        subcommand = 'network'
        yamlfile = os.path.join(self.tmpdir, '{}_{}.yaml'.format(subcommand,
                                                                 env_id))

        self.download(subcommand, env_id)
        self.update_yaml(networks, yamlfile)
        self.upload(subcommand, env_id)


class MasterNodeRepo(MasterNode):
    def __init__(self, ipaddress, port=22, username='root', password='r00tme',
                 repo_ubuntu=False, repo_mos=False):
        super(MasterNodeRepo, self).__init__(ipaddress, port,
                                             username, password)
        self.repo_ubuntu = os.environ.get('UBUNTU_LATEST', False)
        self.repo_mos = os.environ.get('MOS_REPOS', False)

        if self.repo_mos:
            self.repo_mos = '{}/ubuntu/{}'.format(self.repo_mos, self.version)

    def update_yaml(self, yamlfile, repo_ubuntu, repo_mos):
        with open(yamlfile, 'r') as f:
            settings = yaml.safe_load(f)

        for repo in settings['editable']['repo_setup']['repos']['value']:
            if repo_ubuntu and repo['name'].startswith('ubuntu'):
                repo['uri'] = repo_ubuntu

            if repo_mos and repo['name'].startswith('mos'):
                repo['uri'] = repo_mos

        with open(yamlfile, 'w') as f:
            yaml.safe_dump(settings, f)

    def update(self, env_id, repo_ubuntu=None, repo_mos=None):
        subcommand = 'settings'
        yamlfile = os.path.join(self.tmpdir, '{}_{}.yaml'.format(subcommand,
                                                                 env_id))

        if repo_ubuntu is None:
            repo_ubuntu = self.repo_ubuntu

        if repo_mos is None:
            repo_mos = self.repo_mos

        self.download(subcommand, env_id)
        self.update_yaml(yamlfile, repo_ubuntu, repo_mos)
        self.upload(subcommand, env_id)


if __name__ == '__main__':
    action_choices = ['network', 'repos', 'verify']

    parser = argparse.ArgumentParser()
    parser.add_argument('action',
                        help='available commands',
                        choices=action_choices)
    parser.add_argument('-n', '--env',
                        help='name of the environment to configure')
    parser.add_argument('-i', '--id', default='1',
                        help='ID of the cluster which network should be setup')
    args = parser.parse_args()

    networks = get_env_networks(args.env)
    master_node_address = cidr_to_iprange(networks['admin'], start=2)[0]

    if args.action == 'network':
        master_node = MasterNodeNetwork(master_node_address)
        master_node.update(args.id, networks)
    elif args.action == 'repos':
        master_node = MasterNodeRepo(master_node_address)
        master_node.update(args.id)
    elif args.action == 'verify':
        master_node = MasterNode(master_node_address)
        master_node.verify(args.id)
    else:
        print('Unknown action given', file=sys.stderr)
        sys.exit(1)

    master_node.close()
