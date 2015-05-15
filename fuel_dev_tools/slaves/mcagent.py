import os

from fuel_dev_tools import command
from fuel_dev_tools import rsync
from fuel_dev_tools import slaves
from fuel_dev_tools import ssh


class Rsync(slaves.SlavesMixin,
            ssh.SSHMixin,
            rsync.RsyncMixin,
            command.BaseCommand):

    def get_parser(self, prog_name):
        parser = super(Rsync, self).get_parser(prog_name)

        parser.add_argument(
            '-s', '--source',
            nargs='?',
            default='.',
            help='Source of the rsync-ed directory.'
        )

        return parser

    def target_for_slave(self, slave):
        if slave['status'] == 'discover':
            return '/usr/libexec/mcollective/mcollective/agent'

        raise Exception(
            'Don\'t know target for status {status} for node {name}'.format(
                **slave)
        )

    def take_action(self, parsed_args):
        for slave in self.discover_slaves():
            self.print_debug('Syncing to slave {name} [{ip}]'.format(**slave))

            source = parsed_args.source
            target = ':{}'.format(self.target_for_slave(slave))

            hop_args = [
                '-e',
                'ssh -A -t root@{} -p {} ssh -A -t root@{}'.format(
                    self.app_args.ip,
                    self.app_args.port,
                    slave['ip']
                )
            ]

            self.rsync(source, target, *hop_args)
