import os
import six
import subprocess

import docker


class DockerNginxMixin(object):
    container = 'nginx'
    default_command = '/bin/bash'

    def get_log_directory(self):
        return '/var/log/docker-logs/nginx'


class Rsync(DockerNginxMixin, docker.RsyncCommand):
    """Rsync static files to the Docker container.
    """
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
        target = 'root@%s:%s' % (self.app_args.IP, target_dir)

        self.rsync(source, target)

    def build_gulp_static(self, source_dir):
        cwd = os.path.join(source_dir, 'nailgun')

        six.print_(
            'Building gulp static in %s, temporary static dir is: %s...' % (
                cwd,
                self.temporary_build_dir
            )
        )

        cmd = (
            'cd %(cwd)s && '
            'gulp build --static-dir=%(temporary_build_dir)s'
        ) % {
            'cwd': cwd,
            'temporary_build_dir': self.temporary_build_dir,
        }

        try:
            result = subprocess.check_output([
                cmd
            ], shell=True)

            six.print_(result)
        except subprocess.CalledProcessError as e:
            six.print_('GULP ERROR')
            six.print_(e.output)
            raise