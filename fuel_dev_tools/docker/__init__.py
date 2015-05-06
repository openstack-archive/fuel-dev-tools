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

import json
import logging
import os
import six

from cliff import command

from fuel_dev_tools import exc
from fuel_dev_tools import rsync
from fuel_dev_tools import ssh


DOCKER_CONTAINER_PATH = '/var/lib/docker/containers/'
DOCKER_DEVICEMAPPER_PATH = '/var/lib/docker/devicemapper/mnt/'

# TODO(pkaminski)
print_verbose = six.print_


class DockerMixin(object):
    container = None

    def get_container_config(self):
        d = self.get_container_config_directory()

        config = self.ssh_command('cat %s/config.json' % d).decode('utf-8')

        return json.loads(config)

    def get_container_config_directory(self):
        iid = self.get_docker_id()

        paths = self.ssh_command(
            'ls %s | grep %s' % (DOCKER_CONTAINER_PATH, iid)
        ).decode('utf-8')

        return os.path.join(DOCKER_CONTAINER_PATH, paths.split()[0])

    def get_container_directory(self):
        iid = self.get_docker_id()

        paths = self.ssh_command(
            'ls %s | grep %s' % (DOCKER_DEVICEMAPPER_PATH, iid)
        ).decode('utf-8')

        return os.path.join(DOCKER_DEVICEMAPPER_PATH, paths.split()[0])

    def get_docker_id(self, get_exited=False):
        """Returns first 12 characters of LXC container ID.

        (as returned by the 'docker ps' command)

        :param get_exited:
        :return:
        """

        up = self.ssh_command(
            'docker ps -a | grep -i %s | grep Up | cut -f 1 -d " "' %
            self.container
        ).decode('utf-8')

        print_verbose('FOUND CONTAINERS: %r' % up)

        if not up and get_exited:
            print_verbose('Container not Up, trying Exited')

            up = self.ssh_command(
                'docker ps -a | grep -i %s | grep Exited | cut -f 1 -d " "' %
                self.container
            ).decode('utf-8')

            print_verbose('FOUND CONTAINERS: %r' % up)

            if not up:
                raise exc.DockerError(
                    "Container '%s' not found or not functional" %
                    self.container
                )

        return up

    def get_full_docker_id(self, get_exited=False):
        """Returns full container ID.

        :return:
        """

        iid = self.get_docker_id(get_exited=get_exited)

        iid = self.ssh_command(
            "docker inspect -f '{{.Id}}' %s" % iid
        ).decode('utf-8').strip()

        return iid

    def get_log_files(self, args):
        log_dir = self.get_log_directory()
        files = '*.log'

        if args.files:
            if len(args.files) == 1:
                files = '%s.log' % args.files[0]
            else:
                files = '{%s}.log' % ','.join(args.files)

        return os.path.join(log_dir, files)

    def restart_container(self):
        result = self.ssh_command(
            'docker restart %s' % self.get_docker_id()
        )

        print_verbose(result)

    def start_container(self):
        result = self.ssh_command(
            'docker start %s' % self.get_docker_id(get_exited=True)
        )

        print_verbose(result)

    def stop_container(self):
        result = self.ssh_command(
            'docker stop %s' % self.get_docker_id()
        )

        print_verbose(result)


class IdCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        six.print_(self.get_docker_id(get_exited=True))


class ConfigCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        six.print_(json.dumps(self.get_container_config(), indent=2))


class DirCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        six.print_(self.get_container_directory())


class LogCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def get_log_directory(self):
        raise NotImplementedError('No log directory for this command')

    def get_parser(self, prog_name):
        parser = super(LogCommand, self).get_parser(prog_name)

        parser.add_argument(
            'files',
            type=str,
            nargs='*',
            help='List of files to show (all by default).'
        )

        return parser

    def take_action(self, parsed_args):
        six.print_(
            self.ssh_command(
                'tail', '-n', '100000', self.get_log_files(parsed_args)
            )
        )


class RestartCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        self.restart_container()


class RsyncCommand(rsync.RsyncMixin,
                   DockerMixin,
                   ssh.SSHMixin,
                   command.Command):
    def pre_sync(self, parsed_args):
        pass

    def post_sync(self, parsed_args):
        pass

    @property
    def source_path(self):
        return ''

    @property
    def target_path(self):
        return ''

    def get_parser(self, prog_name):
        parser = super(RsyncCommand, self).get_parser(prog_name)

        parser.add_argument(
            '-s', '--source',
            nargs='?',
            default='.',
            help='Source of the rsync-ed directory.'
        )

        return parser

    def take_action(self, parsed_args):
        self.pre_sync(parsed_args)

        source_dir = parsed_args.source

        base_target_dir = os.path.join(
            self.get_container_directory(),
            'rootfs'
        )

        source = os.path.join(source_dir, self.source_path)
        # target is on the remote
        target = os.path.join(base_target_dir, self.target_path)

        self.rsync(source, target)

        self.post_sync(parsed_args)


class ShellCommand(DockerMixin, ssh.SSHMixin, command.Command):
    default_command = None

    log = logging.getLogger(__name__)

    def container_command(self, *commands):
        return [
            #'lxc-attach', '--name', self.get_full_docker_id()
            'docker', 'exec', self.get_docker_id()
        ] + list(commands)

    def get_parser(self, prog_name):
        parser = super(ShellCommand, self).get_parser(prog_name)

        help_msg = 'Command to execute'
        if self.default_command:
            help_msg = '%s (default: %s)' % (help_msg, self.default_command)

        parser.add_argument(
            '-c', '--command',
            default=None,
            help=help_msg
        )

        return parser

    def take_action(self, parsed_args):
        command = parsed_args.command

        if not command:
            command = self.default_command

        if not command:
            command = '/bin/bash'

        return self.ssh_command_interactive(self.container_command(command))


class StartCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        self.start_container()


class StopCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        self.stop_container()


class TailCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def get_log_directory(self):
        raise NotImplementedError('No log directory for this command')

    def get_parser(self, prog_name):
        parser = super(TailCommand, self).get_parser(prog_name)

        parser.add_argument(
            'files',
            type=str,
            nargs='*',
            help='List of files to show (all by default).'
        )

        return parser

    def take_action(self, parsed_args):
        self.ssh_command_interactive(
            'tail', '-F', self.get_log_files(parsed_args)
        )


class VolumesCommand(DockerMixin, ssh.SSHMixin, command.Command):
    def take_action(self, parsed_args):
        six.print_(
            json.dumps(
                self.get_container_config().get('Volumes', {}), indent=2
            )
        )
