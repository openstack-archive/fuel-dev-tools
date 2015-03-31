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

import six
import subprocess

import fabric
from fabric import api as fabric_api

import exc


SSH_PASSWORD_CHECKED = False


print_verbose = six.print_


# TODO(pkaminski): ssh_command should be in some utils, not necessarily
# in this class?
class SSHMixin(object):
    def __init__(self, *args, **kwargs):
        super(SSHMixin, self).__init__(*args, **kwargs)

        if self.app_args:
            fabric_api.env.host_string = self.app_args.IP
            fabric_api.env.user = 'root'

            if not self.app_args.debug:
                for key in fabric.state.output:
                    fabric.state.output[key] = False

    def send_identity(self):
        print_verbose('Sending identity %s for passwordless authentication' %
                      self.app_args.identity_file)

        with open('%s.pub' % self.app_args.identity_file) as f:
            contents = f.read()

        result = fabric_api.run(
            "echo '%s' >> ~/.ssh/authorized_keys" % contents
        )
        print_verbose(result)

        # And while we're here, let's fix /etc/hosts for which 10.20.0.2
        # points to some non-existing domain (with misconfigured reverse-DNS
        # lookups each SSH connection can be quite slow)
        result = fabric_api.run(
            "sed -i 's/^%(IP)s.*/%(IP)s localhost/' /etc/hosts" % {
                'IP': self.app_args.IP
            }
        )
        print_verbose(result)

        # Need to restart after /etc/hosts change
        result = fabric_api.run('service sshd restart')
        print_verbose(result)

        return result

    def ssh_command(self, *args):
        global SSH_PASSWORD_CHECKED

        if not SSH_PASSWORD_CHECKED:
            # NOTE: test if key is added to .authorized_keys with

            SSH_PASSWORD_CHECKED = True

            try:
                subprocess.check_output([
                    'ssh',
                    '-o',
                    'PasswordAuthentication=no',
                    'root@%s' % self.app_args.IP,
                    'echo 1'
                ], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                if 'remote host identification has changed' in \
                        six.u(e.output).decode('utf-8').lower():
                    # .ssh/known_hosts error
                    raise exc.SSHError(e.output)

                # Exit code error -- send .pub key to host
                self.send_identity()

        return fabric_api.run(' '.join(args))

    def ssh_command_interactive(self, *args):
        print_verbose("COMMAND: %r" % list(args))

        command = None

        if args:
            command = ' '.join(args)

        print_verbose('interactive', command)

        fabric_api.open_shell(command=command)
