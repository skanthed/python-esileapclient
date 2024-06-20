import re
import operator
import logging

# Configure the logger
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define constants for operator pattern and filter pattern
OPS = {
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt,
    '=': operator.eq,
}

OPERATOR_PATTERN = '|'.join(re.escape(op) for op in OPS.keys())
FILTER_PATTERN = re.compile(rf'([^><=]+)({OPERATOR_PATTERN})(.+)')


def convert_value(value_str):
    """Convert a value string to an appropriate type for comparison."""
    try:
        return int(value_str)
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            return value_str


def parse_property_filter(filter_str):
    """Parse a property filter string into a key, operator, and value."""
    match = FILTER_PATTERN.match(filter_str)
    if not match:
        raise ValueError(f"Invalid property filter format: {filter_str}")
    key, op_str, value_str = match.groups()
    if op_str not in OPS:
        raise ValueError(f"Invalid operator in property filter: {op_str}")
    value = convert_value(value_str)
    return key.strip(), OPS[op_str], value


def node_matches_property_filters(node, property_filters):
    """Check if a node matches all property filters."""
    properties = node.get('resource_properties', node.get('properties', {}))
    for key, op, value in property_filters:
        if key not in properties:
            return False
        node_value = convert_value(properties.get(key, ''))
        if not op(node_value, value):
            return False
    return True


def filter_nodes_by_properties(nodes, properties):
    """Filter a list of nodes based on property filters."""
    if not properties:
        return nodes
    property_filters = []
    for prop in properties:
        try:
            property_filters.append(parse_property_filter(prop))
        except ValueError as e:
            LOG.error(f"Error parsing property filter '{prop}': {e}")
            raise

    filtered_nodes = [
        node for node in nodes
        if node_matches_property_filters(node, property_filters)
    ]

    return filtered_nodes
