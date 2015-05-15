from fuel_dev_tools import cmd_parser


class SlavesMixin(cmd_parser.CmdParserMixin):
    def discover_slaves(self):
        slaves = self.ssh_command('fuel', 'node')

        return self.parse_output(slaves)
