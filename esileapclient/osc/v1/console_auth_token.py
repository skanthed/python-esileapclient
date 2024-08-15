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

from osc_lib.command import command

from esileapclient.v1.console_auth_token import ConsoleAuthToken \
    as CONSOLE_AUTH_TOKEN_RESOURCE


LOG = logging.getLogger(__name__)


class CreateConsoleAuthToken(command.ShowOne):
    """Create a new console auth token."""

    log = logging.getLogger(__name__ + ".CreateConsoleAuthToken")

    def get_parser(self, prog_name):
        parser = super(CreateConsoleAuthToken, self).get_parser(prog_name)

        parser.add_argument(
            "node_uuid_or_name",
            metavar="<node_uuid_or_name>",
            help="Node UUID or name")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.lease

        field_list = CONSOLE_AUTH_TOKEN_RESOURCE._creation_attributes

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        cat = client.create_console_auth_token(**fields)

        data = dict([(f, getattr(cat, f, '')) for f in
                     CONSOLE_AUTH_TOKEN_RESOURCE.fields])

        return self.dict2columns(data)


class DeleteConsoleAuthToken(command.Command):
    """Delete console auth token"""

    log = logging.getLogger(__name__ + ".DeleteConsoleAuthToken")

    def get_parser(self, prog_name):
        parser = super(DeleteConsoleAuthToken, self).get_parser(prog_name)
        parser.add_argument(
            "node_uuid_or_name",
            metavar="<node_uuid_or_name>",
            help="Node UUID or name")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.lease
        client.delete_console_auth_token(parsed_args.node_uuid_or_name)
        print('Disabled console auth tokens for node %s' %
              parsed_args.node_uuid_or_name)
