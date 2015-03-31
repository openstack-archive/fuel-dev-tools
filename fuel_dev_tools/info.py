
import logging
import six

from cliff import command


class Info(command.Command):
    """Various useful information about the Fuel master node.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        urls = [
            ('OpenStackAPI', 5000, 'http://developer.openstack.org/api-ref.html'),
            ('RabbitMQ', 5672, 'User/password: <empty>'),
            ('RabbitMQ Management', 15672, 'User/password: <empty>'),
        ]

        six.print_('URLS:')
        for name, port, info in urls:
            six.print_('{name:{fill}{align}{width}}http://{IP}:{port:{fill}{align}{width}}{info}'.format(
                name=name,
                IP=self.app_args.IP,
                port=port,
                info=info,
                fill=' ',
                width=20,
                align='<')
            )

        classes = DockerCommand.__subclasses__()
        for klass in sorted(classes, key=lambda k: k.__name__):
            six.print_('-' * 20)
            six.print_(klass.container.title())
            if hasattr(klass, 'get_info'):
                six.print_(klass.get_info())

            six.print_('')
