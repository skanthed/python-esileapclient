import json
import esileapclient.tests.functional.utils.output_utils as utils


def offer_create(client, node_uuid, parse=True, **kwargs):
    valid_flags = ('resource_type', 'start_time', 'end_time',
                   'lessee', 'name', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer create', flags, node_uuid)
    return json.loads(output) if parse else output


def offer_delete(client, offer_uuid):
    return client.esi('offer delete', '', offer_uuid)


def offer_list(client, parse=True, **kwargs):
    valid_flags = ('long', 'status', 'project', 'resource_uuid',
                   'resource_type', 'time_range', 'availability_range')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer list', flags, '')
    return json.loads(output) if parse else output


def offer_show(client, offer_uuid, parse=True, **kwargs):
    flags = '-f json' if parse else ''
    output = client.esi('offer show', flags, offer_uuid)
    return json.loads(output) if parse else output


def offer_claim(client, offer_uuid, parse=True, **kwargs):
    valid_flags = ('start_time', 'end_time', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer claim', flags, offer_uuid)
    return json.loads(output) if parse else output


def lease_create(client, node_uuid, lessee, parse=True, **kwargs):
    valid_flags = ('resource_type', 'start_time', 'end_time',
                   'name', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('lease create', flags, '%s %s' %
                        (node_uuid, lessee))
    return json.loads(output) if parse else output


def lease_list(client, parse=True, **kwargs):
    valid_flags = ('long', 'all', 'status', 'offer_uuid', 'time_range',
                   'project', 'owner', 'resource_type', 'resource_uuid')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('lease list', flags, '')
    return json.loads(output) if parse else output


def lease_delete(client, lease_uuid):
    return client.esi('lease delete', '', lease_uuid)


def lease_show(client, lease_uuid, parse=True):
    flags = '-f json' if parse else ''
    output = client.esi('lease show', flags, lease_uuid)
    return json.loads(output) if parse else output
