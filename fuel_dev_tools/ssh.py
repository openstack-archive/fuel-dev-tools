import os
import six
import subprocess

import exc


SSH_PASSWORD_CHECKED = False


print_verbose = six.print_


# TODO: ssh_command should be in some utils, not necessarily in this class?
class SSHMixin(object):
    def send_identity(self):
        print_verbose('Sending identity %s for passwordless authentication' %
                      self.app_args.identity_file)

        with open('%s.pub' % self.app_args.identity_file) as f:
            contents = f.read()

        result = self.ssh_command("echo '%s' >> ~/.ssh/authorized_keys" % contents)
        print_verbose(result)

        # And while we're here, let's fix /etc/hosts for which 10.20.0.2 points to some non-existing domain
        # (with misconfigured reverse-DNS lookups each SSH connection can be quite slow)
        result = self.ssh_command(
            "sed -i 's/^%(IP)s.*/%(IP)s localhost/' /etc/hosts" % {
                'IP': self.app_args.IP
            }
        )
        print_verbose(result)

        # Need to restart after /etc/hosts change
        result = self.ssh_command('service sshd restart')
        print_verbose(result)

        return result

    def ssh_command(self, *args):
        global SSH_PASSWORD_CHECKED

        print_verbose("COMMAND: %r" % list(args))

        commands = ['ssh',
                    'root@%s' % self.app_args.IP,
                    '-i',
                    self.app_args.identity_file,
                    '-C'] + list(args)

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

        return subprocess.check_output(commands).strip()

    def ssh_command_interactive(self, *args):
        print_verbose("COMMAND: %r" % list(args))

        commands = ['ssh',
                    '-t',
                    'root@%s' % self.app_args.IP,
                    '-i',
                    self.app_args.identity_file]

        if args:
            commands.append('-C')
            commands.extend(list(args))

        print_verbose('interactive', commands)

        os.execvp('ssh', commands)
