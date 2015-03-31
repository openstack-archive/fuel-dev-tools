#!/usr/bin/env python

"""
Command-line utility to help developers work with Fuel master.
"""

import logging
import os
from oslo.utils import encodeutils
import six
import sys
import traceback

from cliff import app
from cliff import commandmanager

from docker import nailgun
from docker import nginx
import exc
import info


COMMANDS = {
    'info': info.Info,

    'nailgun-id': nailgun.Id,
    'nailgun-config': nailgun.Config,
    'nailgun-dir': nailgun.Dir,
    'nailgun-log': nailgun.Log,
    'nailgun-restart': nailgun.Restart,
    'nailgun-rsync': nailgun.Rsync,
    'nailgun-rsync-static': nginx.Rsync,
    'nailgun-shell': nailgun.Shell,
    'nailgun-start': nailgun.Start,
    'nailgun-stop': nailgun.Stop,
    'nailgun-tail': nailgun.Tail,
    'nailgun-volumes': nailgun.Volumes,
}


class ToolsApp(app.App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(ToolsApp, self).__init__(
            description=__doc__.strip(),
            version='1.0',
            command_manager=commandmanager.CommandManager('fuel.cli')
        )

        self.commands = COMMANDS

        for k, v in self.commands.items():
            self.command_manager.add_command(k, v)

    def build_option_parser(self, description, version):
        """Return an argparse option parser for this application.

        Subclasses may override this method to extend
        the parser with more global options.

        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        """
        parser = super(ToolsApp, self).build_option_parser(
            description, version)

        parser.add_argument(
            '--IP',
            default='10.20.0.2',
            help='Fuel master node IP address'
        )
        parser.add_argument(
            '-I', '--identity-file',
            default=os.path.join(
                os.environ['HOME'], '.ssh','id_rsa.openstack'),
            help='SSH identity file'
        )

        return parser


def main(argv=sys.argv[1:]):
    try:
        return ToolsApp().run(
            list(map(encodeutils.safe_decode, argv))
        )
    except KeyboardInterrupt:
        six.print_("... terminating client", file=sys.stderr)
        return 130
    except exc.ClientException:
        six.print_('ClientException')
        return 1
    except exc.SSHError:
        six.print_('SSHError')
        return 1
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    main()
