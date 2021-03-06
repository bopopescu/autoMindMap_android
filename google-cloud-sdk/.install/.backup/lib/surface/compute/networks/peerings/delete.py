# Copyright 2016 Google Inc. All Rights Reserved.
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
"""Command for deleting network peerings."""

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import networks_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core.resource import resource_projector


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class DeleteBeta(base.DeleteCommand):
  """Delete a Google Compute Engine network peering."""

  @staticmethod
  def Args(parser):

    parser.add_argument(
        'name',
        help='The name of the peering to delete.')

    parser.add_argument(
        '--network',
        required=True,
        help='The name of the network in the current project containing the '
             'peering.')

  def Run(self, args):
    """Issues the request necessary for deleting the peering."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    request = client.messages.ComputeNetworksRemovePeeringRequest(
        network=args.network,
        networksRemovePeeringRequest=(
            client.messages.NetworksRemovePeeringRequest(name=args.name)),
        project=properties.VALUES.core.project.GetOrFail())

    response = client.MakeRequests([(client.apitools_client.networks,
                                     'RemovePeering', request)])

    return networks_utils.AddMode(
        [resource_projector.MakeSerializable(m) for m in response])
