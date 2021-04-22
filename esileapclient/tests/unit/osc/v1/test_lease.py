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
import json
from osc_lib.tests import utils as osctestutils

from esileapclient.osc.v1 import lease
from esileapclient.tests.unit.osc.v1 import fakes


class TestLease(fakes.TestLease):

    def setUp(self):
        super(TestLease, self).setUp()

        self.lease_mock = self.app.client_manager.lease
        self.lease_mock.reset_mock()


class TestCreateLease(TestLease):

    def setUp(self):
        super(TestCreateLease, self).setUp()

        self.lease_mock.lease.create.return_value = (
            fakes.FakeLeaseResource(
                None,
                copy.deepcopy(fakes.LEASE)
            ))

        # Get the command object to test
        self.cmd = lease.CreateLease(self.app, None)

    def test_lease_create(self):

        arglist = [
            fakes.lease_resource_type,
            fakes.lease_resource_uuid,
            fakes.lease_project_id,
            '--end-time', fakes.lease_end_time,
            '--name', fakes.lease_name,
            '--properties', fakes.lease_properties,
            '--start-time', fakes.lease_start_time,
            '--status', fakes.lease_status,
        ]

        verifylist = [
            ('end_time', fakes.lease_end_time),
            ('name', fakes.lease_name),
            ('project_id', fakes.lease_project_id),
            ('properties', fakes.lease_properties),
            ('resource_type', fakes.lease_resource_type),
            ('resource_uuid', fakes.lease_resource_uuid),
            ('start_time', fakes.lease_start_time),
            ('status', fakes.lease_status),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'resource_type': fakes.lease_resource_type,
            'resource_uuid': fakes.lease_resource_uuid,
            'project_id': fakes.lease_project_id,
            'end_time': fakes.lease_end_time,
            'name': fakes.lease_name,
            'properties': json.loads(fakes.lease_properties),
            'start_time': fakes.lease_start_time,
            'status': fakes.lease_status,
        }

        self.lease_mock.lease.create.assert_called_once_with(**args)


class TestLeaseList(TestLease):

    def setUp(self):
        super(TestLeaseList, self).setUp()

        self.lease_mock.lease.list.return_value = [
            fakes.FakeLeaseResource(
                None,
                copy.deepcopy(fakes.LEASE))
        ]
        self.cmd = lease.ListLease(self.app, None)

    def test_lease_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'status': parsed_args.status,
            'offer_uuid': parsed_args.offer_uuid,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'project_id': parsed_args.project_id,
            'owner': parsed_args.owner,
            'view': 'all' if parsed_args.all else None
        }

        self.lease_mock.lease.list.assert_called_with(filters)

        collist = [
            "UUID",
            "Name",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.lease_uuid,
                     fakes.lease_name,
                     fakes.lease_resource_type,
                     fakes.lease_resource_uuid,
                     fakes.lease_start_time,
                     fakes.lease_end_time,
                     fakes.offer_uuid,
                     fakes.lease_status,
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_lease_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'status': parsed_args.status,
            'offer_uuid': parsed_args.offer_uuid,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'project_id': parsed_args.project_id,
            'owner': parsed_args.owner,
            'view': 'all' if parsed_args.all else None
        }

        self.lease_mock.lease.list.assert_called_with(filters)

        long_collist = [
            "End Time",
            "Expire Time",
            "Fulfill Time",
            "Name",
            "Offer UUID",
            "Owner ID",
            "Project ID",
            "Properties",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "Status",
            "UUID",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((fakes.lease_end_time,
                     fakes.lease_expire_time,
                     fakes.lease_fulfill_time,
                     fakes.lease_name,
                     fakes.offer_uuid,
                     fakes.lease_owner_id,
                     fakes.lease_project_id,
                     json.loads(fakes.lease_properties),
                     fakes.lease_resource_type,
                     fakes.lease_resource_uuid,
                     fakes.lease_start_time,
                     fakes.lease_status,
                     fakes.lease_uuid
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestLeaseShow(TestLease):
    def setUp(self):
        super(TestLeaseShow, self).setUp()

        self.lease_mock.lease.get.return_value = \
            fakes.FakeLeaseResource(None,
                                    copy.deepcopy(fakes.LEASE))

        self.cmd = lease.ShowLease(self.app, None)

    def test_lease_show(self):
        arglist = [fakes.lease_uuid]
        verifylist = [('uuid', fakes.lease_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.lease_mock.lease.get.assert_called_once_with(
            fakes.lease_uuid)

        collist = (
            "end_time",
            "expire_time",
            "fulfill_time",
            "name",
            "offer_uuid",
            "owner_id",
            "project_id",
            "properties",
            "resource_type",
            "resource_uuid",
            "start_time",
            "status",
            "uuid",
        )

        self.assertEqual(collist, columns)

        datalist = (fakes.lease_end_time,
                    fakes.lease_expire_time,
                    fakes.lease_fulfill_time,
                    fakes.lease_name,
                    fakes.offer_uuid,
                    fakes.lease_owner_id,
                    fakes.lease_project_id,
                    json.loads(fakes.lease_properties),
                    fakes.lease_resource_type,
                    fakes.lease_resource_uuid,
                    fakes.lease_start_time,
                    fakes.lease_status,
                    fakes.lease_uuid
                    )
        self.assertEqual(datalist, tuple(data))

    def test_lease_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestLeaseDelete(TestLease):
    def setUp(self):
        super(TestLeaseDelete, self).setUp()

        self.cmd = lease.DeleteLease(self.app, None)

    def test_lease_delete(self):
        arglist = [fakes.lease_uuid]
        verifylist = [('uuid', fakes.lease_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.lease_mock.lease.delete.assert_called_once_with(
            fakes.lease_uuid)

    def test_lease_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
