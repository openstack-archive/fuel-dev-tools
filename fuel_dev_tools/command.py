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

from cliff import command

from fuel_dev_tools import debug
from fuel_dev_tools import rsync


class BaseCommand(debug.DebugMixin, command.Command):
    pass


class RsyncCommand(rsync.RsyncMixin, BaseCommand):
    def pre_sync(self, parsed_args):
        pass

    def post_sync(self, parsed_args):
        pass

    @property
    def source_path(self):
        raise NotImplementedError

    @property
    def target_path(self):
        raise NotImplementedError

    @property
    def base_target_dir(self):
        return '/'

    def take_action(self, parsed_args):
        self.pre_sync(parsed_args)

        source_dir = parsed_args.source

        base_target_dir = self.base_target_dir
        source = os.path.join(source_dir, self.source_path)
        # target is on the remote
        target = os.path.join(base_target_dir, self.target_path)

        target, args = self.build_app_args_target(target)

        self.rsync(source, target, *args)

        self.post_sync(parsed_args)
