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


class Node(base.Resource):

    detailed_fields = {
        'uuid': "UUID",
        'name': "Name",
        'owner': "Owner",
        'lessee': "Lessee",
        'resource_class': "Resource Class",
        'provision_state': "Provision State",
        'maintenance': "Maintenance",
        'properties': "Properties",
        'offer_uuid': "Offer UUID",
        'lease_uuid': "Lease UUID",
        'future_offers': "Future Offers",
        'future_leases': "Future Leases"
    }

    fields = {
        'name': "Name",
        'owner': "Owner",
        'lessee': "Lessee",
        'resource_class': "Resource Class",
        'provision_state': "Provision State",
        'maintenance': "Maintenance",
        'offer_uuid': "Offer UUID",
        'lease_uuid': "Lease UUID",
    }

    _creation_attributes = ['name', 'uuid', 'owner', 'offer_uuid',
                            'lessee', 'lease_uuid', 'future_offers',
                            'future_leases', 'resource_class',
                            'provision_state', 'maintenance']

    def __repr__(self):
        return "<Node %s>" % self._info
