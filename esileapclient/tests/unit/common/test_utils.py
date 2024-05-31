import unittest
from esileapclient.common import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.nodes = [
            {'properties': {'cpus': '40', 'memory_mb': '131072'}},
            {'properties': {'cpus': '80', 'memory_mb': '262144'}},
            {'properties': {'cpus': '20', 'memory_mb': '65536'}},
        ]

    def test_convert_value(self):
        self.assertEqual(utils.convert_value('10'), 10)
        self.assertEqual(utils.convert_value('10.5'), 10.5)
        self.assertEqual(utils.convert_value('text'), 'text')

    def test_parse_property_filter(self):
        key, op, value = utils.parse_property_filter('cpus>=40')
        self.assertEqual(key, 'cpus')
        self.assertEqual(op, utils.OPS['>='])
        self.assertEqual(value, 40)

        key, op, value = utils.parse_property_filter('memory_mb<=131072')
        self.assertEqual(key, 'memory_mb')
        self.assertEqual(op, utils.OPS['<='])
        self.assertEqual(value, 131072)

        # Test for invalid filter format
        self.assertRaisesRegex(
            ValueError,
            'Invalid property filter format: invalid_filter',
            utils.parse_property_filter, 'invalid_filter'
        )

        # Test for invalid operator
        self.assertRaisesRegex(
            ValueError,
            'Invalid property filter format: cpus!40',
            utils.parse_property_filter, 'cpus!40'
        )

    def test_node_matches_property_filters(self):
        filters = [
            utils.parse_property_filter('cpus>=40'),
            utils.parse_property_filter('memory_mb>=131072')
        ]
        self.assertTrue(utils.node_matches_property_filters(
            self.nodes[1], filters))
        self.assertFalse(utils.node_matches_property_filters(
            self.nodes[2], filters))

        # Test for non-existent property
        filters = [utils.parse_property_filter('non_existent_property>=100')]
        self.assertFalse(utils.node_matches_property_filters(
            self.nodes[0], filters))

    def test_filter_nodes_by_properties(self):
        properties = ['cpus>=40']
        filtered_nodes = utils.filter_nodes_by_properties(
            self.nodes, properties)
        self.assertEqual(len(filtered_nodes), 2)

        properties = ['memory_mb<=131072']
        filtered_nodes = utils.filter_nodes_by_properties(
            self.nodes, properties)
        self.assertEqual(len(filtered_nodes), 2)

        properties = ['cpus>100']
        filtered_nodes = utils.filter_nodes_by_properties(
            self.nodes, properties)
        self.assertEqual(len(filtered_nodes), 0)

        properties = ['cpus<40']
        filtered_nodes = utils.filter_nodes_by_properties(
            self.nodes, properties)
        self.assertEqual(len(filtered_nodes), 1)
        self.assertEqual(filtered_nodes[0]['properties']['cpus'], '20')

        # Test for error parsing property filter
        properties = ['invalid_filter']
        with self.assertLogs('esileapclient.common.utils', level='ERROR') as c:
            self.assertRaisesRegex(
                ValueError,
                "Invalid property filter format: invalid_filter",
                utils.filter_nodes_by_properties, self.nodes, properties
            )
            self.assertTrue(any(
                "Invalid property filter format: invalid_filter" in message
                for message in c.output))
