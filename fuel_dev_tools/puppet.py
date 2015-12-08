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

import os

from fuel_dev_tools import command
from fuel_dev_tools import docker
from fuel_dev_tools import info
from fuel_dev_tools import ssh


class PuppetInfo(info.BasicInfo):
    @classmethod
    def get_info(cls):
        return ''


class Rsync(ssh.SSHMixin,
            command.RsyncCommand):
    """Rsync local directory to the Docker container."""

    def take_action(self, parsed_args):
        source_dir = os.path.join(parsed_args.source, 'deployment', 'puppet/')

        # Target is in /etc/puppet/<release-version>
        release_version = self.ssh_command(
            'ls', '/etc/puppet'
        ).decode('utf-8').split()[0]
        target_dir = os.path.join(
            '/etc', 'puppet', release_version, 'modules'
        )

        target, args = self.build_app_args_target(target_dir)

        self.print_debug('Rsyncing to master')
        self.rsync(source_dir, target, *args)

        updated_containers = set([None])

        # Get DockerMixin subclasses which are also subclasses of
        # command.Basecommand -- only such classes can be used by
        # SSHMixin which requires self.app IP, port and user data
        command_mixins = []
        for docker_mixin_klass in docker.DockerMixin.__subclasses__():
            command_mixins.extend(docker_mixin_klass.__subclasses__())

        for klass in command_mixins:
            if not issubclass(klass, command.BaseCommand) or \
                    klass.container in updated_containers:
                continue

            self.print_debug('Rsyncing to container %s' % klass.container)

            executor = klass(self.app, self.app_args)

            target_dir = os.path.join(
                executor.get_container_directory(),
                'rootfs', 'etc', 'puppet', release_version, 'modules'
            )

            target, args = self.build_app_args_target(target_dir)

            self.rsync(source_dir, target, *args)

            updated_containers.add(klass.container)
