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

import subprocess


class RsyncMixin(object):
    def build_app_args_target(self, target):
        target = '{}@{}:{}'.format(self.app_args.user, self.app_args.ip, target)
        args = ['-e', 'ssh -p {}'.format(self.app_args.port)]

        return target, args

    def rsync(self, source, target, *args):
        self.print_debug('RSYNC: %s --> %s' % (source, target))

        #result = project.rsync_project(
        #    local_dir=source,
        #    remote_dir=target
        #)

        result = subprocess.check_output(
            ['rsync', '-avz'] + list(args) + [source, target]
        )

        self.print_debug(result.decode('utf-8'))
