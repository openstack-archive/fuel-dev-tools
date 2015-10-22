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


class DockerRabbitMQMixin(docker.DockerMixin):
    container = 'RabbitMQ'
    default_command = '/bin/bash'

    def get_log_directory(self):
        return '/var/log/docker-logs/rabbitmq'


class RabbitMQInfo(DockerRabbitMQMixin, info.BasicInfo):
    @classmethod
    def get_info(cls):
        return ''


class Id(DockerRabbitMQMixin, docker.IdCommand):
    """Print Docker container id."""


class Config(DockerRabbitMQMixin, docker.ConfigCommand):
    """Print Docker container config."""


class Dir(DockerRabbitMQMixin, docker.DirCommand):
    """Print Docker container directory on master."""


class Log(DockerRabbitMQMixin, docker.LogCommand):
    """Display logs for container."""


class Restart(DockerRabbitMQMixin, docker.RestartCommand):
    """Restart Docker container."""


class Start(DockerRabbitMQMixin, docker.StartCommand):
    """Start Docker container."""


class Stop(DockerRabbitMQMixin, docker.StopCommand):
    """Stop Docker container."""


class Shell(DockerRabbitMQMixin, docker.ShellCommand):
    """Shell into a nailgun Docker container."""


class Tail(DockerRabbitMQMixin, docker.TailCommand):
    """Display logs for container."""


class Volumes(DockerRabbitMQMixin, docker.VolumesCommand):
    """Print all volumes of a container."""
