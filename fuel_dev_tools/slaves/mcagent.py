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

from fuel_dev_tools import command
from fuel_dev_tools.docker import astute
from fuel_dev_tools.docker import mcollective
from fuel_dev_tools import rsync
from fuel_dev_tools import slaves
from fuel_dev_tools import ssh


class Rsync(slaves.SlavesMixin,
            ssh.SSHMixin,
            rsync.RsyncMixin,
            command.BaseCommand):

    def get_parser(self, prog_name):
        parser = super(Rsync, self).get_parser(prog_name)

        parser.add_argument(
            '-s', '--source',
            nargs='?',
            default='.',
            help='Source of the rsync-ed directory.'
        )

        return parser

    def target_for_slave(self, slave):
        if slave['status'] in ['discover', 'error']:
            return '/usr/libexec/mcollective/mcollective/agent'

        raise Exception(
            'Don\'t know target for status {status} for node {name}'.format(
                **slave)
        )

    def take_action(self, parsed_args):
        for slave in self.discover_slaves():
            self.print_debug('Syncing to slave {name} [{ip}]'.format(**slave))

            source = parsed_args.source
            target = ':{}'.format(self.target_for_slave(slave))

            hop_args = [
                '-e',
                'ssh -A -t root@{} -p {} ssh -A -t root@{}'.format(
                    self.app_args.ip,
                    self.app_args.port,
                    slave['ip']
                )
            ]

            self.rsync(source, target, *hop_args)

            self.print_debug('Restarting mcollective')
            self.slave_command(slave, '/etc/init.d/mcollective', 'restart')

        mc = mcollective.RsyncAgent(self.app, self.app_args)
        mc.take_action(parsed_args)

        ac = astute.RsyncAgent(self.app, self.app_args)
        ac.take_action(parsed_args)
