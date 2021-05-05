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


class OwnerChange(base.Resource):

    detailed_fields = {
        'end_time': "End Time",
        'expire_time': "Expire Time",
        'from_owner_id': "From Owner ID",
        'fulfill_time': "Fulfill Time",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'start_time': "Start Time",
        'status': "Status",
        'to_owner_id': "To Owner ID",
        'uuid': "UUID",
    }

    fields = {
        'uuid': "UUID",
        'status': "Status",
        'from_owner_id': "From Owner ID",
        'to_owner_id': "To Owner ID",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'start_time': "Start Time",
        'end_time': "End Time",
    }

    _creation_attributes = ['resource_type', 'resource_uuid',
                            'start_time', 'end_time',
                            'from_owner_id', 'to_owner_id']

    def __repr__(self):
        return "<OwnerChange %s>" % self._info


class OwnerChangeManager(base.Manager):
    resource_class = OwnerChange
    _resource_name = 'owner_changes'

    def create(self, os_esileap_api_version=None, **kwargs):
        """Create an owner change based on a kwargs dictionary of attributes.
        :returns: a :class: `OwnerChange` object
        """

        owner_change = self._create(
            os_esileap_api_version=os_esileap_api_version, **kwargs)

        return owner_change

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of owner changes.
        :returns: A list of owner changes.
        """

        resource_id = ''

        url_variables = OwnerChangeManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        owner_changes = self._list(
            url, os_esileap_api_version=os_esileap_api_version)

        if type(owner_changes) is list:
            return owner_changes

    def get(self, owner_change_uuid):
        """Get an owner_change with the specified identifier.
        :param owner_change_uuid: The uuid of an owner_change.
        :returns: a :class:`OwnerChange` object.
        """

        owner_change = self._get(owner_change_uuid)

        return owner_change

    def delete(self, owner_change_uuid):
        """Delete an owner_change with the specified identifier.
        :param owner_change_uuid: The uuid of an owner_change.
        :returns: a :class:`OwnerChange` object.
        """

        self._delete(resource_id=owner_change_uuid)
