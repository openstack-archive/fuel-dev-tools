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


class Rsync(command.RsyncCommand):
    @property
    def source_path(self):
        return 'fuelmenu/'

    @property
    def target_path(self):
        return 'usr/lib/python2.6/site-packages/fuelmenu'

    def build_app_args_target(self, target):
        target, args = super(Rsync, self).build_app_args_target(target)

        return target, ['--exclude=*.pyc', '--exclude=test'] + args
