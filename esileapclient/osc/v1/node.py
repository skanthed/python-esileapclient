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
from osc_lib import utils as oscutils

from esileapclient.v1.node import Node as NODE_RESOURCE
from esileapclient.common import utils

LOG = logging.getLogger(__name__)


class ListNode(command.Lister):
    """List nodes."""

    log = logging.getLogger(__name__ + ".ListNode")

    def get_parser(self, prog_name):
        parser = super(ListNode, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the nodes.",
            action='store_true')
        parser.add_argument(
            '--resource-class',
            dest='resource_class',
            required=False,
            help="Filter nodes by resource class.")
        parser.add_argument(
            '--owner',
            dest='owner',
            required=False,
            help="Filter nodes by owner.")
        parser.add_argument(
            '--lessee',
            dest='lessee',
            required=False,
            help="Filter nodes by lessee.")
        parser.add_argument(
            '--property',
            dest='properties',
            required=False,
            action='append',
            help="Filter offers by properties. Format: 'key>=value'. "
                 "Can be specified multiple times. "
                 f"Supported operators are: {', '.join(utils.OPS.keys())}",
            metavar='"key>=value"')

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        # Initial filters dictionary
        filters = {
            'resource_class': parsed_args.resource_class,
            'owner': parsed_args.owner,
            'lessee': parsed_args.lessee
        }

        # Retrieve all nodes with initial filters
        all_nodes = list(client.nodes(**filters))

        # Apply filtering based on properties
        filtered_nodes = utils.filter_nodes_by_properties(
            all_nodes, parsed_args.properties
        )

        if parsed_args.long:
            columns = NODE_RESOURCE.detailed_fields.keys()
            labels = NODE_RESOURCE.detailed_fields.values()
        else:
            columns = NODE_RESOURCE.fields.keys()
            labels = NODE_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns)
                 for s in filtered_nodes))
