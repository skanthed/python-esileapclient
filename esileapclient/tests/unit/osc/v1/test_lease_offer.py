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

from esileapclient.osc.v1 import lease_offer
from esileapclient.tests.unit.osc.v1 import fakes as lease_fakes


class TestLeaseOffer(lease_fakes.TestLease):

    def setUp(self):
        super(TestLeaseOffer, self).setUp()

        self.lease_mock = self.app.client_manager.lease
        self.lease_mock.reset_mock()


class TestLeaseOfferCreate(TestLeaseOffer):

    def setUp(self):
        super(TestLeaseOfferCreate, self).setUp()

        self.lease_mock.offer.create.return_value = (
            lease_fakes.FakeLeaseResource(
                None,
                copy.deepcopy(lease_fakes.OFFER)
            ))

        # Get the command object to test
        self.cmd = lease_offer.CreateLeaseOffer(self.app, None)

    def test_market_offer_create(self):

        arglist = [
            '--end-time', lease_fakes.lease_end_time,
            '--name', lease_fakes.lease_offer_name,
            '--properties', lease_fakes.lease_properties,
            '--resource-type', lease_fakes.lease_resource_type,
            '--resource-uuid', lease_fakes.lease_resource_uuid,
            '--start-time', lease_fakes.lease_start_time,
            '--status', lease_fakes.lease_status,
        ]

        verifylist = [
            ('end_time', lease_fakes.lease_end_time),
            ('name', lease_fakes.lease_offer_name),
            ('properties', lease_fakes.lease_properties),
            ('resource_type', lease_fakes.lease_resource_type),
            ('resource_uuid', lease_fakes.lease_resource_uuid),
            ('start_time', lease_fakes.lease_start_time),
            ('status', lease_fakes.lease_status),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'end_time': lease_fakes.lease_end_time,
            'name': lease_fakes.lease_offer_name,
            'properties': json.loads(lease_fakes.lease_properties),
            'resource_type': lease_fakes.lease_resource_type,
            'resource_uuid': lease_fakes.lease_resource_uuid,
            'start_time': lease_fakes.lease_start_time,
            'status': lease_fakes.lease_status,
        }

        self.lease_mock.offer.create.assert_called_once_with(**args)


class TestLeaseOfferList(TestLeaseOffer):
    def setUp(self):
        super(TestLeaseOfferList, self).setUp()

        self.lease_mock.offer.list.return_value = [
            lease_fakes.FakeLeaseResource(
                None,
                copy.deepcopy(lease_fakes.OFFER))
        ]
        self.cmd = lease_offer.ListLeaseOffer(self.app, None)

    def test_lease_offer_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'status': parsed_args.status,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'available_start_time': str(parsed_args.availability_range[0]) if
            parsed_args.availability_range else None,
            'available_end_time': str(parsed_args.availability_range[1]) if
            parsed_args.availability_range else None,
            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        self.lease_mock.offer.list.assert_called_with(filters)

        collist = [
            "UUID",
            "Name",
            "Start Time",
            "End Time",
            "Resource Type",
            "Resource UUID",
            "Status",
            "Availabilities"
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((lease_fakes.lease_offer_uuid,
                     lease_fakes.lease_offer_name,
                     lease_fakes.lease_start_time,
                     lease_fakes.lease_end_time,
                     lease_fakes.lease_resource_type,
                     lease_fakes.lease_resource_uuid,
                     lease_fakes.lease_status,
                     json.loads(lease_fakes.lease_availabilities)
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_lease_offer_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'status': parsed_args.status,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'available_start_time': str(parsed_args.availability_range[0]) if
            parsed_args.availability_range else None,
            'available_end_time': str(parsed_args.availability_range[1]) if
            parsed_args.availability_range else None,
            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        self.lease_mock.offer.list.assert_called_with(filters)

        long_collist = [
            "Availabilities",
            "End Time",
            "Name",
            "Project ID",
            "Properties",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "Status",
            "UUID",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((json.loads(lease_fakes.lease_availabilities),
                     lease_fakes.lease_end_time,
                     lease_fakes.lease_offer_name,
                     lease_fakes.lease_project_id,
                     json.loads(lease_fakes.lease_properties),
                     lease_fakes.lease_resource_type,
                     lease_fakes.lease_resource_uuid,
                     lease_fakes.lease_start_time,
                     lease_fakes.lease_status,
                     lease_fakes.lease_offer_uuid
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestLeaseOfferShow(TestLeaseOffer):
    def setUp(self):
        super(TestLeaseOfferShow, self).setUp()

        self.lease_mock.offer.get.return_value = \
            lease_fakes.FakeLeaseResource(None,
                                          copy.deepcopy(lease_fakes.OFFER))

        self.cmd = lease_offer.ShowLeaseOffer(self.app, None)

    def test_market_offer_show(self):
        arglist = [lease_fakes.lease_offer_uuid]
        verifylist = [('uuid', lease_fakes.lease_offer_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.lease_mock.offer.get.assert_called_once_with(
            lease_fakes.lease_offer_uuid)

        collist = (
            "availabilities",
            "end_time",
            "name",
            "project_id",
            "properties",
            "resource_type",
            "resource_uuid",
            "start_time",
            "status",
            "uuid",
        )

        self.assertEqual(collist, columns)

        datalist = (json.loads(lease_fakes.lease_availabilities),
                    lease_fakes.lease_end_time,
                    lease_fakes.lease_offer_name,
                    lease_fakes.lease_project_id,
                    json.loads(lease_fakes.lease_properties),
                    lease_fakes.lease_resource_type,
                    lease_fakes.lease_resource_uuid,
                    lease_fakes.lease_start_time,
                    lease_fakes.lease_status,
                    lease_fakes.lease_offer_uuid
                    )
        self.assertEqual(datalist, tuple(data))

    def test_lease_offer_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestLeaseOfferDelete(TestLeaseOffer):
    def setUp(self):
        super(TestLeaseOfferDelete, self).setUp()

        self.cmd = lease_offer.DeleteLeaseOffer(self.app, None)

    def test_lease_offer_delete(self):
        arglist = [lease_fakes.lease_offer_uuid]
        verifylist = [('uuid', lease_fakes.lease_offer_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.lease_mock.offer.delete.assert_called_once_with(
            lease_fakes.lease_offer_uuid)

    def test_lease_offer_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
