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
"""`gcloud iot devices update` command."""
from googlecloudsdk.api_lib.cloudiot import devices
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.iot import flags
from googlecloudsdk.command_lib.iot import util


class Update(base.UpdateCommand):
  """Update an existing device."""

  @staticmethod
  def Args(parser):
    flags.AddDeviceResourceFlags(parser, 'to update')
    for flag in flags.GetDeviceFlags(defaults=False):
      flag.AddToParser(parser)

  def Run(self, args):
    client = devices.DevicesClient()

    device_ref = util.ParseDevice(args.id, registry=args.registry,
                                  region=args.region)
    enabled_state = util.ParseEnableDevice(args.enable_device, client=client)

    return client.Patch(
        device_ref,
        enabled_state=enabled_state)
