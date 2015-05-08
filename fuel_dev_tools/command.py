from cliff import command

from fuel_dev_tools import debug


class BaseCommand(debug.DebugMixin, command.Command):
    pass