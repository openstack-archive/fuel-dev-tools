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

from fuel_dev_tools import docker


class DockerMcollectiveMixin(docker.DockerMixin):
    container = 'mcollective'
    default_command = '/bin/bash'

    def get_log_directory(self):
        return '/var/log/docker-logs/mcollective'


class RsyncAgent(DockerMcollectiveMixin, docker.RsyncCommand):
    """Rsync mcagent files to the Docker container."""
    @property
    def source_path(self):
        return '.'

    @property
    def target_path(self):
        return 'usr/libexec/mcollective/mcollective/agent'

    def post_sync(self, parsed_args):
        self.restart_container()


class RsyncShotgun(DockerMcollectiveMixin, docker.RsyncCommand):
    """Rsync shotgun files to the Docker container."""
    @property
    def source_path(self):
        return 'shotgun/shotgun'

    @property
    def target_path(self):
        return 'usr/lib/python2.6/site-packages/shotgun'

    def post_sync(self, parsed_args):
        self.restart_container()


class Shell(DockerMcollectiveMixin, docker.ShellCommand):
    """Shell into the container."""
