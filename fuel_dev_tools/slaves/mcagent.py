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
            command.RsyncCommand):

    def target_for_slave(self, slave):
        if slave['status'] in ['discover', 'error']:
            return '/usr/libexec/mcollective/mcollective/agent'

        raise Exception(
            'Don\'t know target for status {status} for node {name}'.format(
                **slave)
        )

    def take_action(self, parsed_args):
        for slave in self.discover_slaves():
            source = parsed_args.source
            target = self.target_for_slave(slave)

            self.rsync_slave(slave, source, target)

            self.print_debug('Restarting mcollective')
            self.slave_command(slave, '/etc/init.d/mcollective', 'restart')

        mc = mcollective.RsyncAgent(self.app, self.app_args)
        mc.take_action(parsed_args)

        ac = astute.RsyncAgent(self.app, self.app_args)
        ac.take_action(parsed_args)
