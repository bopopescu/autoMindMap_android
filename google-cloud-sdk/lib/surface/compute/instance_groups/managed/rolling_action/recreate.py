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
"""Command for recreating instances of managed instance group."""

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.instance_groups import flags as instance_groups_flags
from googlecloudsdk.command_lib.compute.instance_groups.managed import flags as instance_groups_managed_flags
from googlecloudsdk.command_lib.compute.instance_groups.managed import rolling_action
from googlecloudsdk.command_lib.compute.managed_instance_groups import update_instances_utils


@base.Deprecate(
    is_removed=False,
    warning=('Use gcloud alpha compute instance-groups managed rolling-action '
             'replace instead.'))
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class StartUpdate(base.Command):
  """Start recreate instances of managed instance group."""

  @staticmethod
  def Args(parser):
    instance_groups_managed_flags.AddMaxSurgeArg(parser)
    instance_groups_managed_flags.AddMaxUnavailableArg(parser)
    instance_groups_managed_flags.AddMinReadyArg(parser)
    instance_groups_flags.MULTISCOPE_INSTANCE_GROUP_MANAGER_ARG.AddArgument(
        parser)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client
    resources = holder.resources

    cleared_fields = []

    with client.apitools_client.IncludeFields(cleared_fields):
      minimal_action = (client.messages.InstanceGroupManagerUpdatePolicy.
                        MinimalActionValueValuesEnum.REPLACE)
      max_surge = update_instances_utils.ParseFixedOrPercent(
          '--max-surge', 'max-surge', args.max_surge, client.messages)
      return client.MakeRequests([
          rolling_action.CreateRequest(args, cleared_fields, client, resources,
                                       minimal_action, max_surge)
      ])


StartUpdate.detailed_help = {
    'brief':
        'Recreates instances in a managed instance group',
    'DESCRIPTION':
        """\
        *{command}* recreates instances in a managed instance group."""
}
