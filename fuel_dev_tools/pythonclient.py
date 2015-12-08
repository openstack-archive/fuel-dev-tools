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
from fuel_dev_tools import rsync
from fuel_dev_tools import ssh


class Rsync(ssh.SSHMixin,
            command.RsyncCommand):
    """Rsync local CLI directory to the main machine."""

    def take_action(self, parsed_args):
        source_dir = os.path.join(parsed_args.source, 'fuelclient/')

        # Target is in /usr/lib/python2.6/site-packages/fuelclient
        target_dir = os.path.join(
            '/usr', 'lib', 'python2.6', 'site-packages', 'fuelclient'
        )

        target, args = self.build_app_args_target(target_dir)

        self.print_debug('Rsyncing to master')
        self.rsync(source_dir, target, *args)

    def build_app_args_target(self, target):
        target, args = super(Rsync, self).build_app_args_target(target)

        return target, ['--exclude=*.pyc'] + args
