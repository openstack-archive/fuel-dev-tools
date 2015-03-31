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
from fuel_dev_tools import info


class DockerNailgunMixin(object):
    container = 'nailgun'
    default_command = 'python'

    def get_log_directory(self):
        return '/var/log/docker-logs/nailgun'


class NailgunInfo(DockerNailgunMixin, info.BasicInfo):
    @classmethod
    def get_info(cls):
        return ('If you login to the shell you have the possibility to '
                'reset the database with commands\n'
                '/usr/bin/nailgun_syncdb\n'
                '/usr/bin/naligun_fixtures')


class Id(DockerNailgunMixin, docker.IdCommand):
    """Print Docker container id."""


class Config(DockerNailgunMixin, docker.ConfigCommand):
    """Print Docker container config."""


class Dir(DockerNailgunMixin, docker.DirCommand):
    """Print Docker container directory on master."""


class Log(DockerNailgunMixin, docker.LogCommand):
    """Display logs for container."""


class Restart(DockerNailgunMixin, docker.RestartCommand):
    """Restart Docker container."""


class Rsync(DockerNailgunMixin, docker.RsyncCommand):
    """Rsync local directory to the Docker container."""
    @property
    def source_path(self):
        return 'nailgun/nailgun'

    @property
    def target_path(self):
        return 'usr/lib/python2.6/site-packages/nailgun'

    def post_sync(self, parsed_args):
        self.restart_container()


class Start(DockerNailgunMixin, docker.StartCommand):
    """Start Docker container."""


class Stop(DockerNailgunMixin, docker.StopCommand):
    """Stop Docker container."""


class Shell(DockerNailgunMixin, docker.ShellCommand):
    """Shell into a nailgun Docker container."""


class Tail(DockerNailgunMixin, docker.TailCommand):
    """Display logs for container."""


class Volumes(DockerNailgunMixin, docker.VolumesCommand):
    """Print all volumes of a container."""
