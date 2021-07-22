import copy

from esileapclient.osc.v1 import node
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestNode(base.TestESILeapCommand):

    def setUp(self):
        super(TestNode, self).setUp()

        self.client_mock = self.app.client_manager.node
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
        }

        self.client_mock.lease.list.assert_called_with(filters)

        collist = [
            "Name",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.node_name
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_lease_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
        }

        self.client_mock.lease.list.assert_called_with(filters)

        long_collist = [
            "Name",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((fakes.node_name,
                     ),)
        self.assertEqual(datalist, tuple(data))
