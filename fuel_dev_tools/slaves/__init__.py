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

from fabric import api as fabric_api

from fuel_dev_tools import cmd_parser


class SlavesMixin(cmd_parser.CmdParserMixin):
    def discover_slaves(self):
        slaves = self.ssh_command('fuel', 'node')

        return self.parse_output(slaves)

    def rsync_slave(self, slave, source, target):
        self.print_debug('Syncing to slave {name} [{ip}]'.format(**slave))

        target = ':{}'.format(target)

        hop_args = [
            '-e',
            'ssh -A -t root@{} -p {} ssh -A -t root@{}'.format(
                self.app_args.ip,
                self.app_args.port,
                slave['ip']
            )
        ]

        self.rsync(source, target, *hop_args)

    def slave_command(self, slave, *cmd):
        cmd = [
            'ssh', '-A', '-t',
            '{}@{}'.format(self.app_args.user, self.app_args.ip),
            '-p', self.app_args.port,
            'ssh', '-A', '-t',
            'root@{ip}'.format(**slave)
        ] + list(cmd)

        return fabric_api.run(' '.join(cmd))
