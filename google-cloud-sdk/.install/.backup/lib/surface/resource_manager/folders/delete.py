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
"""Command to delete a folder."""

from googlecloudsdk.api_lib.resource_manager import folders
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.resource_manager import flags
from googlecloudsdk.core import log


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Delete(base.DeleteCommand):
  """Delete a folder.

  Delete a folder, given a valid folder ID.

  This command can fail for the following reasons:
      * There is no folder with the given ID.
      * The active account does not have permission to delete the given folder.
      * The folder to be deleted is not empty.

  ## EXAMPLES

  The following command deletes a folder with the ID `123456789`:

    $ {command} 123456789
  """

  @staticmethod
  def Args(parser):
    flags.FolderIdArg('you want to delete.').AddToParser(parser)

  def Run(self, args):
    service = folders.FoldersService()
    messages = folders.FoldersMessages()
    result = service.Delete(
        messages.CloudresourcemanagerFoldersDeleteRequest(foldersId=args.id))
    log.DeletedResource(result)
