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

from fabric import api as fabric_api

from fuel_dev_tools import docker


class DockerNginxMixin(object):
    container = 'nginx'
    default_command = '/bin/bash'

    def get_log_directory(self):
        return '/var/log/docker-logs/nginx'


class Rsync(DockerNginxMixin, docker.RsyncCommand):
    """Rsync static files to the Docker container."""
    temporary_build_dir = 'built-static'

    def get_parser(self, prog_name):
        parser = super(Rsync, self).get_parser(prog_name)

        parser.add_argument(
            '--no-gulp',
            action='store_true',
            help=('Don\'t run Gulp building task (default: false; note that '
                  'by default the minified version is used.')
        )

        return parser

    def take_action(self, parsed_args):
        source_dir = parsed_args.source

        # NOTE: slash at the end is important in source_path!
        source_path = 'nailgun/%s/' % self.temporary_build_dir

        if not parsed_args.no_gulp:
            self.build_gulp_static(source_dir)

        config = self.get_container_config()
        target_dir = config['Volumes']['/usr/share/nailgun/static']

        source = os.path.join(source_dir, source_path)

        target, args = self.build_app_args_target(target_dir)

        self.rsync(source, target, *args)

        self.rsync(source, target)

    def build_gulp_static(self, source_dir):
        cwd = os.path.join(source_dir, 'nailgun')

        self.print_debug(
            'Building gulp static in %s, temporary static dir is: %s...' % (
                cwd,
                self.temporary_build_dir
            )
        )

        with fabric_api.lcd(cwd):
            result = fabric_api.run(
                fabric_api.local(
                    'gulp build --static-dir=%s' % self.temporary_build_dir
                )
            )

            self.print_debug(result)
