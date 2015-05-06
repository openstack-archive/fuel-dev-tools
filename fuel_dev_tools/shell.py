#!/usr/bin/env python
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

from docker import astute
from docker import nailgun
from docker import nginx
import exc
import info


COMMANDS = {
    'info': info.Info,

    'astute-id': astute.Id,
    'astute-config': astute.Config,
    'astute-dir': astute.Dir,
    'astute-log': astute.Log,
    'astute-restart': astute.Restart,
    'astute-rsync': astute.Rsync,
    'astute-shell': astute.Shell,
    'astute-start': astute.Start,
    'astute-stop': astute.Stop,
    'astute-tail': astute.Tail,
    'astute-volumes': astute.Volumes,

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
                os.environ['HOME'], '.ssh', 'id_rsa.openstack'),
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
