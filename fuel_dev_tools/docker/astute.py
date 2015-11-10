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

import six
import subprocess

from fuel_dev_tools import docker
from fuel_dev_tools import info


class DockerAstuteMixin(docker.DockerMixin):
    container = 'astute'
    default_command = '/bin/bash'

    def get_log_directory(self):
        return '/var/log/docker-logs/astute'


class AstuteInfo(DockerAstuteMixin, info.BasicInfo):
    @classmethod
    def get_info(cls):
        return """Admin token is stored in /etc/fuel/astute.yaml on Fuel Main.

If you want to send custom receiverd response from Astute:
http://sprunge.us/UJfb
        """


class Id(DockerAstuteMixin, docker.IdCommand):
    """Print Docker container id."""


class Config(DockerAstuteMixin, docker.ConfigCommand):
    """Print Docker container config."""


class Dir(DockerAstuteMixin, docker.DirCommand):
    """Print Docker container directory on master."""


class Log(DockerAstuteMixin, docker.LogCommand):
    """Display logs for container."""


class Restart(DockerAstuteMixin, docker.RestartCommand):
    """Restart Docker container."""


class Rsync(DockerAstuteMixin, docker.RsyncCommand, docker.ShellCommand):
    """Rsync local directory to the Docker container."""

    gemspec = 'astute.gemspec'
    gemfile_template = 'astute-{}.gem'
    gemfile = 'astute-8.0.0.gem'

    @property
    def source_path(self):
        return self.gemfile

    @property
    def target_path(self):
        return 'tmp/%s' % self.gemfile

    def pre_sync(self, parsed_args):
        self._update_gemfile(parsed_args.astute_version)
        self.build_gem(parsed_args.source)

    def post_sync(self, parsed_args):
        self.ssh_command(*self.container_command(
            'gem install', '--local', '-q', '-f', self.target_path
        ))

        self.restart_container()

    def build_gem(self, source_dir):
        cmd = (
            'cd %(cwd)s && '
            'gem build %(gemspec)s'
        ) % {
            'cwd': source_dir,
            'gemspec': self.gemspec,
        }

        try:
            result = subprocess.check_output([
                cmd
            ], shell=True)

            self.print_debug(result)
        except subprocess.CalledProcessError as e:
            six.print_('GEM BUILD ERROR')
            six.print_(e.output)
            raise

    def get_parser(self, prog_name):
        parser = super(Rsync, self).get_parser(prog_name)

        parser.add_argument(
            '-a', '--astute-version',
            default='8.0.0',
            help=('Astute gem version (default: 8.0.0). '
                  'Change if master node version is changed.')
        )

        return parser

    def _update_gemfile(self, version):
        self.gemfile = self.gemfile_template.format(version)


class RsyncAgent(DockerAstuteMixin, docker.RsyncCommand):
    """Rsync files to the Docker container."""
    @property
    def source_path(self):
        return '.'

    @property
    def target_path(self):
        return 'usr/libexec/mcollective/mcollective/agent'

    def post_sync(self, parsed_args):
        self.restart_container()


class Start(DockerAstuteMixin, docker.StartCommand):
    """Start Docker container."""


class Stop(DockerAstuteMixin, docker.StopCommand):
    """Stop Docker container."""


class Shell(DockerAstuteMixin, docker.ShellCommand):
    """Shell into a nailgun Docker container."""


class Tail(DockerAstuteMixin, docker.TailCommand):
    """Display logs for container."""


class Volumes(DockerAstuteMixin, docker.VolumesCommand):
    """Print all volumes of a container."""
