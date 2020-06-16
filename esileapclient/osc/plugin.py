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
import argparse

from osc_lib import utils


DEFAULT_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'lease'
API_VERSION_OPTION = 'os_lease_api_version'
API_VERSIONS = {
    '1': 'esileapclient.v1.client.Client',
}

OS_LEAP_API_LATEST = True
LAST_KNOWN_API_VERSION = '1'
LATEST_VERSION = '1'


LOG = logging.getLogger(__name__)


def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """

    requested_api_version = instance._api_version[API_NAME]

    plugin_client = utils.get_client_class(
        API_NAME,
        requested_api_version,
        API_VERSIONS)

    client = plugin_client(
        os_esileap_api_version=requested_api_version,
        session=instance.session,
        region_name=instance._region_name,
        endpoint_override=None
        )

    return client


def build_option_parser(parser):

    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-lease-api-version',
        metavar='<esileapclient-api-version>',
        default=utils.env(
            'OS_LEASE_API_VERSION',
            default=DEFAULT_API_VERSION),
        help='ESI Leap Client API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: OS_LEASE_API_VERSION)')
    return parser

