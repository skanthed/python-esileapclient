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
import json

from osc_lib.command import command
from osc_lib import utils as oscutils

from esileapclient.v1.contract import Contract as CONTRACT_RESOURCE

LOG = logging.getLogger(__name__)


class CreateLeaseContract(command.ShowOne):
    """Create a new lease contract."""

    log = logging.getLogger(__name__ + ".CreateLeaseContract")

    def get_parser(self, prog_name):
        parser = super(CreateLeaseContract, self).get_parser(prog_name)

        parser.add_argument(
            '--end-date',
            dest='end_date',
            required=False,
            help="Time when the contract will expire.")
        parser.add_argument(
            '--offer-uuid',
            dest='offer_uuid',
            required=True,
            help="UUID of the offer")
        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help='State which the offer should be created in.')
        parser.add_argument(
            '--start-date',
            dest='start_date',
            required=False,
            help="Time when the resource will become usable.")
        parser.add_argument(
            '--properties',
            dest='properties',
            required=False,
            help="Record arbitrary key/value resource property "
                 "information. Pass in as a json object.")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease

        field_list = ['start_date', 'end_date',
                      'status', 'offer_uuid', 'properties']

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        contract = lease_client.contract.create(**fields)

        data = dict([(f, getattr(contract, f, '')) for f in
                    CONTRACT_RESOURCE.fields])

        return self.dict2columns(data)


class ListLeaseContract(command.Lister):
    """List lease contracts."""

    log = logging.getLogger(__name__ + ".ListLeaseContrct")

    def get_parser(self, prog_name):
        parser = super(ListLeaseContract, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the contracts.",
            action='store_true')

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease
        data = lease_client.contract.list()

        if parsed_args.long:
            columns = CONTRACT_RESOURCE.detailed_fields.keys()
            labels = CONTRACT_RESOURCE.detailed_fields.values()
        else:
            columns = CONTRACT_RESOURCE.fields.keys()
            labels = CONTRACT_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class ShowLeaseContract(command.ShowOne):
    """Show lease contract details."""

    log = logging.getLogger(__name__ + ".ShowLeaseContract")

    def get_parser(self, prog_name):
        parser = super(ShowLeaseContract, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="UUID of the contract")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease

        contract = lease_client.contract.get(parsed_args.uuid)._info

        return zip(*sorted(contract.items()))


class DeleteLeaseContract(command.Command):
    """Unregister lease contract"""

    log = logging.getLogger(__name__ + ".DeleteLeaseContract")

    def get_parser(self, prog_name):
        parser = super(DeleteLeaseContract, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="Contract to delete (UUID)")

        return parser

    def take_action(self, parsed_args):

        lease_client = self.app.client_manager.lease
        lease_client.contract.delete(parsed_args.uuid)
        print('Deleted contract %s' % parsed_args.uuid)
