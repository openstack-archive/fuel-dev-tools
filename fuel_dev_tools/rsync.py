import six
import subprocess


class RsyncMixin(object):
    def rsync(self, source, target):
        six.print_('RSYNC: %s --> %s' % (source, target))

        result = subprocess.check_output(
            ['rsync'] + self.rsync_args() + [source, target]
        )

        six.print_(result.decode('utf-8'))

    @property
    def base_rsync_args(self):
        return ['-a', '-v', '-z', '-e', 'ssh']

    def rsync_args(self):
        return self.base_rsync_args