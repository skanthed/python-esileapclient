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


import logging

from esileapclient.common import base

LOG = logging.getLogger(__name__)


class Lease(base.Resource):

    detailed_fields = {
        'end_time': "End Time",
        'expire_time': "Expire Time",
        'fulfill_time': "Fulfill Time",
        'name': "Name",
        'offer_uuid': "Offer UUID",
        'owner': "Owner",
        'owner_id': "Owner ID",
        'parent_lease_uuid': "Parent Lease UUID",
        'project': "Project",
        'project_id': "Project ID",
        'properties': "Properties",
        'resource': "Resource",
        'resource_class': "Resource Class",
        'resource_properties': "Resource Properties",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'start_time': "Start Time",
        'status': "Status",
        'uuid': "UUID",
        'purpose': "Purpose",
    }

    long_fields = {
        'uuid': "UUID",
        'resource': "Resource",
        'resource_class': "Resource Class",
        'resource_properties': "Resource Properties",
        'project': "Project",
        'start_time': "Start Time",
        'end_time': "End Time",
        'expire_time': "Expire Time",
        'fulfill_time': "Fulfill Time",
        'offer_uuid': "Offer UUID",
        'owner': "Owner",
        'parent_lease_uuid': "Parent Lease UUID",
        'status': "Status",
        'purpose': "Purpose",
    }

    fields = {
        'uuid': "UUID",
        'resource': "Resource",
        'resource_class': "Resource Class",
        'project': "Project",
        'start_time': "Start Time",
        'end_time': "End Time",
        'offer_uuid': "Offer UUID",
        'status': "Status",
        'purpose': "Purpose",
    }

    _creation_attributes = ['start_time', 'end_time', 'status', 'name',
                            'properties', 'project_id', 'resource_type',
                            'resource_uuid', 'purpose']
    _update_attributes = ['end_time']

    def __repr__(self):
        return "<Lease %s>" % self._info
