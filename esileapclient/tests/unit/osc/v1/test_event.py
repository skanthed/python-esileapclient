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

import copy

from esileapclient.osc.v1 import event
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestEvent(base.TestESILeapCommand):

    def setUp(self):
        super(TestEvent, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestEventList(TestEvent):

    def setUp(self):
        super(TestEventList, self).setUp()

        self.client_mock.events.return_value = [
            base.FakeResource(copy.deepcopy(fakes.EVENT))
        ]
        self.cmd = event.ListEvent(self.app, None)

    def test_event_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'lessee_or_owner_id': parsed_args.project_id,
            'last_event_id': parsed_args.last_event_id,
            'last_event_time': parsed_args.last_event_time,
            'event_type': parsed_args.event_type,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid,
        }

        self.client_mock.events.assert_called_with(**filters)

        collist = [
            "ID",
            "Event Type",
            "Event Time",
            "Object Type",
            "Object UUID",
            "Resource Type",
            "Resource UUID",
            "Lessee ID",
            "Owner ID",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.event_id,
                     fakes.event_type,
                     fakes.event_time,
                     fakes.object_type,
                     fakes.lease_uuid,
                     fakes.lease_resource_type,
                     fakes.lease_resource_uuid,
                     fakes.lease_project_id,
                     fakes.lease_owner_id,
                     ),)
        self.assertEqual(datalist, tuple(data))
