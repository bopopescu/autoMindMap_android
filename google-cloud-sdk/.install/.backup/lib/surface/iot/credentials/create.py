# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""`gcloud iot credentials create` command."""
from googlecloudsdk.api_lib.cloudiot import devices
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.iot import flags
from googlecloudsdk.command_lib.iot import util


class Create(base.CreateCommand):
  """Add a new credential to a device.

  A device may have at most 3 credentials.
  """

  @staticmethod
  def Args(parser):
    flags.AddDeviceResourceFlags(parser, 'for which to create credentials',
                                 positional=False)
    flags.AddDeviceCredentialFlagsToParser(parser, combine_flags=False)

  def Run(self, args):
    client = devices.DevicesClient()

    device_ref = util.ParseDevice(args.device, registry=args.registry,
                                  region=args.region)
    new_credential = util.ParseCredential(
        args.path, args.type, args.expiration_time, messages=client.messages)

    credentials = client.Get(device_ref).credentials
    if len(credentials) >= util.MAX_PUBLIC_KEY_NUM:
      raise util.InvalidPublicKeySpecificationError(
          'Cannot create a new public key credential for this device; '
          'maximum {} keys are allowed.'.format(util.MAX_PUBLIC_KEY_NUM))
    credentials.append(new_credential)
    return client.Patch(device_ref, credentials=credentials)
