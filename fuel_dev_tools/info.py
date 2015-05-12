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

import logging
import six

from fuel_dev_tools import command


class BasicInfo(object):
    pass


class Info(command.BaseCommand):
    """Various useful information about the Fuel master node."""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        urls = [
            ('OpenStackAPI', 5000,
             'http://developer.openstack.org/api-ref.html'),
            ('RabbitMQ', 5672, 'User/password: <empty>'),
            ('RabbitMQ Management', 15672, 'User/password: <empty>'),
        ]

        six.print_('URLS:')
        for name, port, info in urls:
            six.print_('{name:{fill}{align}{width}}http://{ip}:{port:{fill}'
                       '{align}{width}}{info}'.format(
                           name=name,
                           ip=self.app_args.ip,
                           port=port,
                           info=info,
                           fill=' ',
                           width=20,
                           align='<')
                       )

        classes = BasicInfo.__subclasses__()
        for klass in sorted(classes, key=lambda k: k.__name__):
            six.print_('-' * 20)
            six.print_(klass.container.title())
            if hasattr(klass, 'get_info'):
                six.print_(klass.get_info())

            six.print_('')
