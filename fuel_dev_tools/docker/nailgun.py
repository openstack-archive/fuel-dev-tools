
import docker


class DockerNailgunMixin(object):
    container = 'nailgun'
    default_command = 'python'

    def get_log_directory(self):
        return '/var/log/docker-logs/nailgun'


class Id(DockerNailgunMixin, docker.IdCommand):
    """Print Docker container id.
    """


class Config(DockerNailgunMixin, docker.ConfigCommand):
    """Print Docker container config.
    """


class Dir(DockerNailgunMixin, docker.DirCommand):
    """Print Docker container directory on master.
    """


class Log(DockerNailgunMixin, docker.LogCommand):
    """Display logs for container.
    """


class Restart(DockerNailgunMixin, docker.RestartCommand):
    """Restart Docker container.
    """


class Rsync(DockerNailgunMixin, docker.RsyncCommand):
    """Rsync local directory to the Docker container.
    """
    @property
    def source_path(self):
        return 'nailgun/nailgun'

    @property
    def target_path(self):
        return 'usr/lib/python2.6/site-packages/nailgun'

    def post_sync(self):
        self.restart_container()


class Start(DockerNailgunMixin, docker.StartCommand):
    """Start Docker container.
    """


class Stop(DockerNailgunMixin, docker.StopCommand):
    """Stop Docker container.
    """


class Shell(DockerNailgunMixin, docker.ShellCommand):
    """Shell into a nailgun Docker container.
    """


class Tail(DockerNailgunMixin, docker.TailCommand):
    """Display logs for container.
    """


class Volumes(DockerNailgunMixin, docker.VolumesCommand):
    """Print all volumes of a container.
    """
