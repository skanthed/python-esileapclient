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

from esileapclient.osc.v1 import lease_contract
from esileapclient.tests.unit.osc.v1 import fakes as lease_fakes


class TestLeaseContract(lease_fakes.TestLease):

    def setUp(self):
        super(TestLeaseContract, self).setUp()

        self.lease_mock = self.app.client_manager.lease
        self.lease_mock.reset_mock()


class TestCreateLeaseContract(TestLeaseContract):

    def setUp(self):
        super(TestCreateLeaseContract, self).setUp()

        self.lease_mock.contract.create.return_value = (
            lease_fakes.FakeLeaseResource(
                None,
                copy.deepcopy(lease_fakes.CONTRACT)
            ))

        # Get the command object to test
        self.cmd = lease_contract.CreateLeaseContract(self.app, None)

    def test_market_contract_create(self):

        arglist = [
            '--end-time', lease_fakes.lease_end_time,
            '--name', lease_fakes.lease_contract_name,
            '--offer', lease_fakes.lease_offer_uuid,
            '--properties', lease_fakes.lease_properties,
            '--start-time', lease_fakes.lease_start_time,
            '--status', lease_fakes.lease_status,
        ]

        verifylist = [
            ('end_time', lease_fakes.lease_end_time),
            ('name', lease_fakes.lease_contract_name),
            ('offer_uuid_or_name', lease_fakes.lease_offer_uuid),
            ('properties', lease_fakes.lease_properties),
            ('start_time', lease_fakes.lease_start_time),
            ('status', lease_fakes.lease_status),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'end_time': lease_fakes.lease_end_time,
            'name': lease_fakes.lease_contract_name,
            'offer_uuid_or_name': lease_fakes.lease_offer_uuid,
            'properties': json.loads(lease_fakes.lease_properties),
            'start_time': lease_fakes.lease_start_time,
            'status': lease_fakes.lease_status,
        }

        self.lease_mock.contract.create.assert_called_once_with(**args)


class TestLeaseContractList(TestLeaseContract):
    def setUp(self):
        super(TestLeaseContractList, self).setUp()

        self.lease_mock.contract.list.return_value = [
            lease_fakes.FakeLeaseResource(
                None,
                copy.deepcopy(lease_fakes.CONTRACT))
        ]
        self.cmd = lease_contract.ListLeaseContract(self.app, None)

    def test_lease_contract_list(self):
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

        self.lease_mock.contract.list.assert_called_with(filters)

        collist = [
            "UUID",
            "Name",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((lease_fakes.lease_contract_uuid,
                     lease_fakes.lease_contract_name,
                     lease_fakes.lease_start_time,
                     lease_fakes.lease_end_time,
                     lease_fakes.lease_offer_uuid,
                     lease_fakes.lease_status,
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_lease_contract_list_long(self):
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

        self.lease_mock.contract.list.assert_called_with(filters)

        long_collist = [
            "End Time",
            "Expire Time",
            "Fulfill Time",
            "Name",
            "Offer UUID",
            "Project ID",
            "Properties",
            "Start Time",
            "Status",
            "UUID",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((lease_fakes.lease_end_time,
                     lease_fakes.lease_expire_time,
                     lease_fakes.lease_fulfill_time,
                     lease_fakes.lease_contract_name,
                     lease_fakes.lease_offer_uuid,
                     lease_fakes.lease_project_id,
                     json.loads(lease_fakes.lease_properties),
                     lease_fakes.lease_start_time,
                     lease_fakes.lease_status,
                     lease_fakes.lease_contract_uuid
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestLeaseContractShow(TestLeaseContract):
    def setUp(self):
        super(TestLeaseContractShow, self).setUp()

        self.lease_mock.contract.get.return_value = \
            lease_fakes.FakeLeaseResource(None,
                                          copy.deepcopy(lease_fakes.CONTRACT))

        self.cmd = lease_contract.ShowLeaseContract(self.app, None)

    def test_market_contract_show(self):
        arglist = [lease_fakes.lease_contract_uuid]
        verifylist = [('uuid', lease_fakes.lease_contract_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.lease_mock.contract.get.assert_called_once_with(
            lease_fakes.lease_contract_uuid)

        collist = (
            "end_time",
            "expire_time",
            "fulfill_time",
            "name",
            "offer_uuid",
            "project_id",
            "properties",
            "start_time",
            "status",
            "uuid",
        )

        self.assertEqual(collist, columns)

        datalist = (lease_fakes.lease_end_time,
                    lease_fakes.lease_expire_time,
                    lease_fakes.lease_fulfill_time,
                    lease_fakes.lease_contract_name,
                    lease_fakes.lease_offer_uuid,
                    lease_fakes.lease_project_id,
                    json.loads(lease_fakes.lease_properties),
                    lease_fakes.lease_start_time,
                    lease_fakes.lease_status,
                    lease_fakes.lease_contract_uuid
                    )
        self.assertEqual(datalist, tuple(data))

    def test_lease_contract_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestLeaseContractDelete(TestLeaseContract):
    def setUp(self):
        super(TestLeaseContractDelete, self).setUp()

        self.cmd = lease_contract.DeleteLeaseContract(self.app, None)

    def test_lease_contract_delete(self):
        arglist = [lease_fakes.lease_contract_uuid]
        verifylist = [('uuid', lease_fakes.lease_contract_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.lease_mock.contract.delete.assert_called_once_with(
            lease_fakes.lease_contract_uuid)

    def test_lease_contract_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
