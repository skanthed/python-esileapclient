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

from osc_lib.tests import utils as osctestutils

from esileapclient.osc.v1 import owner_change
from esileapclient.tests.unit.osc.v1 import base


class TestOwnerChange(base.TestESILeapCommand):

    def setUp(self):
        super(TestOwnerChange, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()
        self.owner_change_data = {
            'end_time': '2020-07-31',
            'expire_time': '2020-07-31',
            'from_owner_id': 'from-owner-id',
            'fulfill_time': '2020-07-24',
            'resource_type': 'dummy_node',
            'resource_uuid': '12345',
            'start_time': '2020-07-24',
            'status': 'ACTIVE',
            'to_owner_id': 'to-owner-id',
            'uuid': 'owner-change-id'
        }


class TestOwnerChangeCreate(TestOwnerChange):

    def setUp(self):
        super(TestOwnerChangeCreate, self).setUp()

        self.client_mock.owner_change.create.return_value = (
            base.FakeResource(self.owner_change_data)
        )

        # Get the command object to test
        self.cmd = owner_change.CreateOwnerChange(self.app, None)

    def test_owner_change_create(self):
        arglist = [
            self.owner_change_data['from_owner_id'],
            self.owner_change_data['to_owner_id'],
            self.owner_change_data['resource_uuid'],
            '--end-time', self.owner_change_data['end_time'],
            '--resource-type', self.owner_change_data['resource_type'],
            '--start-time', self.owner_change_data['start_time'],
        ]

        verifylist = [
            ('end_time', self.owner_change_data['end_time']),
            ('from_owner_id', self.owner_change_data['from_owner_id']),
            ('resource_type', self.owner_change_data['resource_type']),
            ('resource_uuid', self.owner_change_data['resource_uuid']),
            ('start_time', self.owner_change_data['start_time']),
            ('to_owner_id', self.owner_change_data['to_owner_id']),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'end_time': self.owner_change_data['end_time'],
            'from_owner_id': self.owner_change_data['from_owner_id'],
            'resource_type': self.owner_change_data['resource_type'],
            'resource_uuid': self.owner_change_data['resource_uuid'],
            'start_time': self.owner_change_data['start_time'],
            'to_owner_id': self.owner_change_data['to_owner_id'],
        }

        self.client_mock.owner_change.create.assert_called_once_with(**args)


class TestOwnerChangeList(TestOwnerChange):

    def setUp(self):
        super(TestOwnerChangeList, self).setUp()

        self.client_mock.owner_change.list.return_value = [
            base.FakeResource(self.owner_change_data)
        ]
        self.cmd = owner_change.ListOwnerChange(self.app, None)

    def test_owner_change_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        expected_filters = {
            'end_time': None,
            'from_owner_id': None,
            'resource_type': None,
            'resource_uuid': None,
            'status': None,
            'start_time': None,
            'to_owner_id': None,
        }
        expected_collist = [
            "UUID",
            "Status",
            "From Owner ID",
            "To Owner ID",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "End Time",
        ]
        expected_datalist = ((
            self.owner_change_data['uuid'],
            self.owner_change_data['status'],
            self.owner_change_data['from_owner_id'],
            self.owner_change_data['to_owner_id'],
            self.owner_change_data['resource_type'],
            self.owner_change_data['resource_uuid'],
            self.owner_change_data['start_time'],
            self.owner_change_data['end_time'],
        ),)

        self.client_mock.owner_change.list.assert_called_with(expected_filters)
        self.assertEqual(expected_collist, list(columns))
        self.assertEqual(expected_datalist, tuple(data))

    def test_owner_change_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        expected_filters = {
            'end_time': None,
            'from_owner_id': None,
            'resource_type': None,
            'resource_uuid': None,
            'status': None,
            'start_time': None,
            'to_owner_id': None,
        }
        expected_collist = [
            "End Time",
            "Expire Time",
            "From Owner ID",
            "Fulfill Time",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "Status",
            "To Owner ID",
            "UUID",
        ]
        expected_datalist = ((
            self.owner_change_data['end_time'],
            self.owner_change_data['expire_time'],
            self.owner_change_data['from_owner_id'],
            self.owner_change_data['fulfill_time'],
            self.owner_change_data['resource_type'],
            self.owner_change_data['resource_uuid'],
            self.owner_change_data['start_time'],
            self.owner_change_data['status'],
            self.owner_change_data['to_owner_id'],
            self.owner_change_data['uuid'],
        ),)

        self.client_mock.owner_change.list.assert_called_with(expected_filters)
        self.assertEqual(expected_collist, list(columns))
        self.assertEqual(expected_datalist, tuple(data))


class TestOwnerChangeShow(TestOwnerChange):

    def setUp(self):
        super(TestOwnerChangeShow, self).setUp()

        self.client_mock.owner_change.get.return_value = \
            base.FakeResource(self.owner_change_data)
        self.cmd = owner_change.ShowOwnerChange(self.app, None)

    def test_owner_change_show(self):
        arglist = [self.owner_change_data['uuid']]
        verifylist = [('uuid', self.owner_change_data['uuid'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client_mock.owner_change.get.assert_called_once_with(
            self.owner_change_data['uuid'])

        expected_collist = (
            "end_time",
            "expire_time",
            "from_owner_id",
            "fulfill_time",
            "resource_type",
            "resource_uuid",
            "start_time",
            "status",
            "to_owner_id",
            "uuid",
        )
        expected_datalist = (
            self.owner_change_data['end_time'],
            self.owner_change_data['expire_time'],
            self.owner_change_data['from_owner_id'],
            self.owner_change_data['fulfill_time'],
            self.owner_change_data['resource_type'],
            self.owner_change_data['resource_uuid'],
            self.owner_change_data['start_time'],
            self.owner_change_data['status'],
            self.owner_change_data['to_owner_id'],
            self.owner_change_data['uuid'],
        )

        self.assertEqual(expected_collist, columns)
        self.assertEqual(expected_datalist, tuple(data))

    def test_owner_change_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestOwnerChangeDelete(TestOwnerChange):
    def setUp(self):
        super(TestOwnerChangeDelete, self).setUp()

        self.cmd = owner_change.DeleteOwnerChange(self.app, None)

    def test_owner_change_delete(self):
        arglist = [self.owner_change_data['uuid']]
        verifylist = [('uuid', self.owner_change_data['uuid'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.client_mock.owner_change.delete.assert_called_once_with(
            self.owner_change_data['uuid'])

    def test_owner_change_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
