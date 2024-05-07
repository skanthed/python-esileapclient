import copy

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

        self.client_mock.node.list.return_value = [
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

        self.client_mock.node.list.assert_called_with(filters)

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
        }

        self.client_mock.node.list.assert_called_with(filters)

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
                     fakes.formatted_node_properties,
                     '', '', '', ''
                     ),)
        self.assertEqual(datalist, tuple(data))
