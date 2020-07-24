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


class Contract(base.Resource):

    detailed_fields = {
        'end_time': "End Time",
        'name': "Name",
        'offer_uuid': "Offer UUID",
        'project_id': "Project ID",
        'properties': "Properties",
        'start_time': "Start Time",
        'status': "Status",
        'uuid': "UUID",
    }

    fields = {
        'uuid': "UUID",
        'name': "Name",
        'start_time': "Start Time",
        'end_time': "End Time",
        'offer_uuid': "Offer UUID",
        'status': "Status",
    }

    _creation_attributes = ['start_time', 'end_time', 'status', 'name',
                            'offer_uuid_or_name', 'properties', 'project_id']

    def __repr__(self):
        return "<Contract %s>" % self._info


class ContractManager(base.Manager):
    resource_class = Contract
    _resource_name = 'contracts'

    def create(self, os_esileap_api_version=None, **kwargs):
        """Create a contract based on a kwargs dictionary of attributes.
        :returns: a :class: `Contract` object
        """

        contract = self._create(os_esileap_api_version=os_esileap_api_version,
                                **kwargs)

        return contract

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of contracts.
        :returns: A list of contracts.
        """

        resource_id = ""

        url_variables = ContractManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        contracts = self._list(url,
                               os_esileap_api_version=os_esileap_api_version)

        if type(contracts) is list:
            return contracts

    def get(self, contract_uuid):
        """Get a contract with the specified identifier.
        :param contract_uuid: The uuid of a contract.
        :returns: a :class:`Contract` object.
        """

        contract = self._get(contract_uuid)

        return contract

    def delete(self, contract_uuid):
        """Delete a contract with the specified identifier.
        :param contract_uuid: The uuid of a contract.
        :returns: a :class:`Contract` object.
        """

        self._delete(resource_id=contract_uuid)
