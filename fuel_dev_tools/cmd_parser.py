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