class CmdParserMixin(object):
    """Mixin for parsing fuel CLI output."""

    def parse_output(self, output):
        ret = []
        header = []

        lines = output.split('\n')
        # brutal
        lines = [line for line in lines
                 if not line.startswith('DEPRECATION WARNING')]

        for name in lines[0].split('|'):
            header.append(name.strip())

        # lines[1] is just '----'

        for line in lines[2:]:
            values = [v.strip() for v in line.split('|')]
            ret.append(dict(zip(header, values)))

        return ret