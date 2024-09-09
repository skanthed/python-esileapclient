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


class ConsoleAuthToken(base.Resource):

    fields = {
        'node_uuid': "Node UUID",
        'token': "Token",
        'access_url': "Access URL",
    }

    _creation_attributes = ['node_uuid_or_name']

    def __repr__(self):
        return "<ConsoleAuthToken %s>" % self._info
