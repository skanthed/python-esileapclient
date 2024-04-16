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


class Offer(base.Resource):

    detailed_fields = {
        'availabilities': "Availabilities",
        'end_time': "End Time",
        'lessee': "Lessee",
        'lessee_id': "Lessee ID",
        'name': "Name",
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
    }

    long_fields = {
        'uuid': "UUID",
        'resource': "Resource",
        'resource_class': "Resource Class",
        'resource_properties': "Resource Properties",
        'lessee': "Lessee",
        'start_time': "Start Time",
        'end_time': "End Time",
        'status': "Status",
        'availabilities': "Availabilities",
        'project': "Project",
        'parent_lease_uuid': "Parent Lease UUID",
    }

    fields = {
        'uuid': "UUID",
        'resource': "Resource",
        'resource_class': "Resource Class",
        'lessee': "Lessee",
        'start_time': "Start Time",
        'end_time': "End Time",
        'status': "Status",
        'availabilities': "Availabilities",
    }

    _creation_attributes = ['resource_type', 'resource_uuid',
                            'start_time', 'end_time', 'status',
                            'project_id', 'properties', 'name',
                            'lessee_id']

    def __repr__(self):
        return "<Offer %s>" % self._info
