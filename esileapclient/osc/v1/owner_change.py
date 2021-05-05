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

from esileapclient.v1.owner_change import OwnerChange as OWNER_CHANGE_RESOURCE

LOG = logging.getLogger(__name__)


class CreateOwnerChange(command.ShowOne):
    """Create a new owner change."""

    log = logging.getLogger(__name__ + ".CreateOwnerChange")

    def get_parser(self, prog_name):
        parser = super(CreateOwnerChange, self).get_parser(prog_name)

        parser.add_argument(
            "from_owner_id",
            metavar="<from_owner_id>",
            help="From Owner ID")
        parser.add_argument(
            "to_owner_id",
            metavar="<to_owner_id>",
            help="To Owner ID")
        parser.add_argument(
            "resource_uuid",
            metavar="<resource_uuid>",
            help="Resource UUID")
        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=False,
            help="Time when the owner change will expire.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Use this resource type instead of the default.")
        parser.add_argument(
            '--start-time',
            dest='start_time',
            required=False,
            help="Time when the owner change will be active.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        field_list = OWNER_CHANGE_RESOURCE._creation_attributes

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        owner_change = client.owner_change.create(**fields)

        data = dict([(f, getattr(owner_change, f, '')) for f in
                    OWNER_CHANGE_RESOURCE.fields])

        return self.dict2columns(data)


class ListOwnerChange(command.Lister):
    """List owner changes."""

    log = logging.getLogger(__name__ + ".ListOwnerChange")

    def get_parser(self, prog_name):
        parser = super(ListOwnerChange, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the owner changes.",
            action='store_true')
        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help="Show all owner changes with given status.")
        parser.add_argument(
            '--time-range',
            dest='time_range',
            nargs=2,
            required=False,
            help="Show all owner changes with start and end times "
                 "which begin and end in the given range."
                 "Must pass in two valid datetime strings."
                 "Example: --time-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")
        parser.add_argument(
            '--from-owner-id',
            dest='from_owner_id',
            required=False,
            help="Show all owner changes from given project id.")
        parser.add_argument(
            '--to-owner-id',
            dest='to_owner_id',
            required=False,
            help="Show all owner changes to given project id.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all owner changes with given resource type.")
        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=False,
            help="Show all owner changes with given resource uuid.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        filters = {
            'status': parsed_args.status,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'from_owner_id': parsed_args.from_owner_id,
            'to_owner_id': parsed_args.to_owner_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        data = client.owner_change.list(filters)

        if parsed_args.long:
            columns = OWNER_CHANGE_RESOURCE.detailed_fields.keys()
            labels = OWNER_CHANGE_RESOURCE.detailed_fields.values()
        else:
            columns = OWNER_CHANGE_RESOURCE.fields.keys()
            labels = OWNER_CHANGE_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class ShowOwnerChange(command.ShowOne):
    """Show owner change details."""

    log = logging.getLogger(__name__ + ".ShowOwnerChange")

    def get_parser(self, prog_name):
        parser = super(ShowOwnerChange, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="UUID of the owner change")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        owner_change = client.owner_change.get(parsed_args.uuid)._info

        return zip(*sorted(owner_change.items()))


class DeleteOwnerChange(command.Command):
    """Cancel owner change"""

    log = logging.getLogger(__name__ + ".DeleteOwnerChange")

    def get_parser(self, prog_name):
        parser = super(DeleteOwnerChange, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="Owner change to cancel (UUID)")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease
        client.owner_change.delete(parsed_args.uuid)
        print('Canceled owner change %s' % parsed_args.uuid)
