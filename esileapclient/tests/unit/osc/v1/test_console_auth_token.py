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

import copy

from esileapclient.osc.v1 import console_auth_token
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestConsoleAuthToken(base.TestESILeapCommand):

    def setUp(self):
        super(TestConsoleAuthToken, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestCreateConsoleAuthToken(TestConsoleAuthToken):

    def setUp(self):
        super(TestCreateConsoleAuthToken, self).setUp()

        self.client_mock.create_console_auth_token.return_value = (
            base.FakeResource(copy.deepcopy(fakes.CONSOLE_AUTH_TOKEN))
        )

        # Get the command object to test
        self.cmd = console_auth_token.CreateConsoleAuthToken(self.app, None)

    def test_console_auth_token_create(self):
        arglist = [fakes.node_uuid]
        verifylist = [('node_uuid_or_name', fakes.node_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        args = {
            'node_uuid_or_name': fakes.node_uuid
        }

        self.client_mock.create_console_auth_token.assert_called_once_with(
            **args)


class TestConsoleAuthTokenDelete(TestConsoleAuthToken):
    def setUp(self):
        super(TestConsoleAuthTokenDelete, self).setUp()

        self.cmd = console_auth_token.DeleteConsoleAuthToken(self.app, None)

    def test_console_auth_token_delete(self):
        arglist = [fakes.node_uuid]
        verifylist = [('node_uuid_or_name', fakes.node_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.client_mock.delete_console_auth_token.assert_called_once_with(
            fakes.node_uuid)
