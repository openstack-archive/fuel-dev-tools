from fabric import api as fabric_api

from fuel_dev_tools import cmd_parser
from fuel_dev_tools import ssh


class SlavesMixin(cmd_parser.CmdParserMixin, ssh.SSHMixin):
    def discover_slaves(self):
        slaves = self.ssh_command('fuel', 'node')

        return self.parse_output(slaves)

    def slave_command(self, slave, *cmd):
        cmd = [
            'ssh', '-A', '-t',
            '{}@{}'.format(self.app_args.user, self.app_args.ip),
            '-p', self.app_args.port,
            'ssh', '-A', '-t',
            'root@{ip}'.format(**slave)
        ] + list(cmd)

        return fabric_api.run(' '.join(cmd))
