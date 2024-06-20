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
from unittest import mock

from esileapclient.osc.v1 import node
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestNode(base.TestESILeapCommand):

    def setUp(self):
        super(TestNode, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestNodeList(TestNode):

    def setUp(self):
        super(TestNodeList, self).setUp()

        self.client_mock.nodes.return_value = [
            base.FakeResource(copy.deepcopy(fakes.NODE))
        ]
        self.cmd = node.ListNode(self.app, None)

    def test_node_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'resource_class': parsed_args.resource_class,
            'owner': parsed_args.owner,
            'lessee': parsed_args.lessee
        }

        self.client_mock.nodes.assert_called_with(**filters)

        collist = [
            "Name",
            "Owner",
            "Lessee",
            "Resource Class",
            "Provision State",
            "Maintenance",
            "Offer UUID",
            "Lease UUID",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.node_name,
                     fakes.node_owner,
                     '', fakes.lease_resource_class,
                     '', '', '', ''
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_node_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'resource_class': parsed_args.resource_class,
            'owner': parsed_args.owner,
            'lessee': parsed_args.lessee
        }

        self.client_mock.nodes.assert_called_with(**filters)

        long_collist = [
            "UUID",
            "Name",
            "Owner",
            "Lessee",
            "Provision State",
            "Maintenance",
            "Offer UUID",
            "Lease UUID",
            "Future Offers",
            "Future Leases"
        ]
        long_collist = [
            'UUID',
            'Name',
            'Owner',
            'Lessee',
            'Resource Class',
            'Provision State',
            'Maintenance',
            'Properties',
            'Offer UUID',
            'Lease UUID',
            'Future Offers',
            'Future Leases'
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((fakes.node_uuid,
                     fakes.node_name,
                     fakes.node_owner,
                     '',
                     fakes.lease_resource_class,
                     '', '',
                     fakes.node_properties,
                     '', '', '', ''
                     ),)
        self.assertEqual(datalist, tuple(data))

    @mock.patch('esileapclient.common.utils.filter_nodes_by_properties')
    def test_node_list_with_property_filter(self, mock_filter_nodes):
        arglist = ['--property', 'cpus>=40']
        verifylist = [('properties', ['cpus>=40'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'resource_class': parsed_args.resource_class,
            'owner': parsed_args.owner,
            'lessee': parsed_args.lessee
        }

        self.client_mock.nodes.assert_called_with(**filters)
        mock_filter_nodes.assert_called_with(mock.ANY, parsed_args.properties)

    @mock.patch('esileapclient.common.utils.filter_nodes_by_properties')
    def test_node_list_long_with_property_filter(self, mock_filter_nodes):
        arglist = ['--long', '--property', 'memory_mb>=131072']
        verifylist = [('long', True), ('properties', ['memory_mb>=131072'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'resource_class': parsed_args.resource_class,
            'owner': parsed_args.owner,
            'lessee': parsed_args.lessee
        }

        self.client_mock.nodes.assert_called_with(**filters)
        mock_filter_nodes.assert_called_with(mock.ANY, parsed_args.properties)
