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

import unittest.mock as mock
import testtools

from esileapclient.osc import plugin

from esi import connection

API_VERSION = '1'


class FakeClientManager(object):
    def __init__(self):
        self.identity = None
        self.auth_ref = None
        self.interface = 'public'
        self._region_name = 'RegionOne'
        self.session = 'fake session'
        self._api_version = {'lease': API_VERSION}
        self._cli_options = None


class MakeClientTest(testtools.TestCase):

    @mock.patch.object(connection, 'ESIConnection')
    def test_make_client_explicit_version(self, mock_conn):
        instance = FakeClientManager()
        mock_conn.return_value.lease = mock.Mock()
        instance._api_version = {'lease': API_VERSION}
        lease = plugin.make_client(instance)
        mock_conn.assert_called_once_with(config=None)
        self.assertEqual(lease, mock_conn.return_value.lease)

    @mock.patch.object(connection, 'ESIConnection')
    def test_make_client_latest(self, mock_conn):
        instance = FakeClientManager()
        mock_conn.return_value.lease = mock.Mock()
        instance._api_version = {'lease': plugin.LATEST_VERSION}
        lease = plugin.make_client(instance)
        mock_conn.assert_called_once_with(config=None)
        self.assertEqual(lease, mock_conn.return_value.lease)

    @mock.patch.object(connection, 'ESIConnection')
    def test_make_client_v1(self, mock_conn):
        instance = FakeClientManager()
        mock_conn.return_value.lease = mock.Mock()
        instance._api_version = {'lease': '1'}
        lease = plugin.make_client(instance)
        mock_conn.assert_called_once_with(config=None)
        self.assertEqual(lease, mock_conn.return_value.lease)
