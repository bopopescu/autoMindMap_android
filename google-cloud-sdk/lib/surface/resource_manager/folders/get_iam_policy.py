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
"""Command to get IAM policy for a folder."""

from googlecloudsdk.api_lib.resource_manager import folders
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.resource_manager import flags


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class GetIamPolicy(base.Command):
  """Get IAM policy for a folder.

  Gets the IAM policy for a folder, given a folder ID.

  ## EXAMPLES

  The following command prints the IAM policy for a folder with the ID
  `3589215982`:

    $ {command} 3589215982
  """

  @staticmethod
  def Args(parser):
    flags.FolderIdArg('whose policy you want to get.').AddToParser(parser)

  def Run(self, args):
    return folders.GetIamPolicy(args.id)
