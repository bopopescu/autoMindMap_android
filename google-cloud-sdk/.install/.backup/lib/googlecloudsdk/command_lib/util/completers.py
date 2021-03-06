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

"""Completer extensions for the core.cache.completion_cache module."""

import abc

from googlecloudsdk.api_lib.util import resource_search
from googlecloudsdk.command_lib.util import parameter_info_lib
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources
from googlecloudsdk.core.cache import completion_cache
from googlecloudsdk.core.cache import resource_cache


_PSEUDO_COLLECTION_PREFIX = 'cloud.sdk'


def PseudoCollectionName(name):
  """Returns the pseudo collection name for name.

  Pseudo collection completion entities have no resource parser and/or URI.

  Args:
    name: The pseudo collection entity name.

  Returns:
    The pseudo collection name for name.
  """
  return '.'.join([_PSEUDO_COLLECTION_PREFIX, name])


class Converter(completion_cache.Completer):
  """Converter mixin, based on core/resource_completion_style at instantiation.

  Attributes:
      _additional_params: A list of additional parameter names not int the
        parsed resource.
      qualified_parameter_names: The list of parameter names that must be fully
        qualified.  Use the name 'collection' to qualify collections.
  """

  def __init__(self, additional_params=None, qualified_parameter_names=None,
               style=None, **kwargs):
    super(Converter, self).__init__(**kwargs)
    self._additional_params = additional_params
    self.qualified_parameter_names = set(qualified_parameter_names or [])
    if style is None:
      style = properties.VALUES.core.resource_completion_style.Get()

    if style == 'gri' or properties.VALUES.core.enable_gri.GetBool():
      self._string_to_row = self._GRI_StringToRow
    else:
      self._string_to_row = self._StringToRow

    if style == 'gri':
      self._row_to_string = self._GRI_RowToString
    else:
      self._row_to_string = self._FLAGS_RowToString

  def StringToRow(self, string):
    """Returns the row representation of string."""
    return self._string_to_row(string)

  def RowToString(self, row, parameter_info=None):
    """Returns the string representation of row."""
    return self._row_to_string(row, parameter_info=parameter_info)

  def AddQualifiedParameterNames(self, qualified_parameter_names):
    """Adds qualified_parameter_names to the set of qualified parameters."""
    self.qualified_parameter_names |= qualified_parameter_names

  def ParameterInfo(self, parsed_args, argument):
    """Returns the parameter info object.

    This is the default method that returns the parameter info by name
    convention object.  Resource argument completers should override this
    method to provide the exact object, not the "best guess" of the default.

    Args:
      parsed_args: The command line parsed args object.
      argument: The argparse argument object attached to this completer.

    Returns:
      The parameter info object.
    """
    return parameter_info_lib.ParameterInfoByConvention(
        parsed_args, argument, self.collection)

  def _GRI_StringToRow(self, string):
    try:
      # '' is not parsable so treat it like None to match all.
      return self.parse(string or None)
    except resources.RequiredFieldOmittedException:
      fields = resources.GRI.FromString(string, self.collection).path_fields
      if len(fields) < self.columns:
        fields += [''] * (self.columns - len(fields))
      return list(reversed(fields))

  def _StringToRow(self, string):
    if string and (string.startswith('https://') or
                   string.startswith('http://')):
      try:
        row = self.parse(string or None)
        return row
      except resources.RequiredFieldOmittedException:
        pass
    return [''] * (self.columns - 1) + [string]

  def _GRI_RowToString(self, row, parameter_info=None):
    # Clear out parameters that are the same as the corresponding
    # flag/property value, in highest to lowest significance order, stopping
    # at the first parameter that can't be cleared.
    parts = list(row)
    for column, parameter in enumerate(self.parameters):
      if parameter.name in self.qualified_parameter_names:
        continue
      value = parameter_info.GetValue(parameter.name)
      if parts[column] != value:
        break
      parts[column] = ''
    if 'collection' in self.qualified_parameter_names:
      collection = self.collection
      is_fully_qualified = True
    else:
      collection = None
      is_fully_qualified = True
    return str(resources.GRI(reversed(parts),
                             collection=collection,
                             is_fully_qualified=is_fully_qualified))

  def _FLAGS_RowToString(self, row, parameter_info=None):
    parts = [row[self.columns - 1]]
    parameters = self.parameters
    name = 'collection'
    if name in self.qualified_parameter_names:
      # Treat 'collection' like a parameter.
      collection_parameter = resource_cache.Parameter(name=name)
      parameters = list(parameters) + [collection_parameter]
    for parameter in parameters:
      if parameter.column == self.columns - 1:
        continue
      check_properties = parameter.name not in self.qualified_parameter_names
      flag = parameter_info.GetFlag(
          parameter.name,
          row[parameter.column],
          check_properties=check_properties)
      if flag:
        parts.append(flag)
    for flag_name in set(self._additional_params or [] +
                         parameter_info.GetAdditionalParams() or []):
      flag = parameter_info.GetFlag(flag_name, True)
      if flag:
        parts.append(flag)
    return ' '.join(parts)


class ResourceCompleter(Converter):
  """A parsed resource parameter initializer.

  Attributes:
    collection_info: The resource registry collection info.
    parse: The resource URI parse function. Converts a URI string into a list
      of parsed parameters.
  """

  def __init__(self, collection=None, api_version=None, param=None, timeout=60,
               **kwargs):
    """Constructor.

    Args:
      collection: The resource collection name.
      api_version: The API version for collection, None for the default version.
      param: The updated parameter column name.
      timeout: The persistent cache timeout in seconds.
      **kwargs: Base class kwargs.
    """
    self.api_version = api_version
    self.collection_info = resources.REGISTRY.GetCollectionInfo(
        collection, api_version=api_version)
    params = self.collection_info.params
    log.info(u'cache collection=%s api_version=%s params=%s' % (
        collection, self.collection_info.api_version, params))
    parameters = [resource_cache.Parameter(name=name, column=column)
                  for column, name in enumerate(params)]
    parse = resources.REGISTRY.Parse

    def _Parse(string):
      return parse(string, collection=collection,
                   enforce_collection=False, validate=False).AsList()

    self.parse = _Parse

    super(ResourceCompleter, self).__init__(
        collection=collection,
        columns=len(params),
        column=params.index(param) if param else 0,
        parameters=parameters,
        timeout=timeout,
        **kwargs)


class ListCommandCompleter(ResourceCompleter):
  """A parameterized completer that uses a gcloud list command for updates.

  Attributes:
    list_command: The gcloud list command that returns the list of current
      resource URIs.
  """

  def __init__(self, list_command=None, **kwargs):
    self.list_command = list_command
    super(ListCommandCompleter, self).__init__(**kwargs)

  def GetListCommand(self, parameter_info):
    """Returns the list command argv given parameter_info."""
    del parameter_info
    return self.list_command.split() + ['--quiet', '--format=disable']

  def Update(self, parameter_info, aggregations):
    """Returns the current list of parsed resources from list_command."""
    command = self.GetListCommand(parameter_info)
    for parameter in aggregations:
      flag = parameter_info.GetFlag(parameter.name, parameter.value)
      if flag:
        command.append(flag)
    log.info(u'cache update command: %s' % ' '.join(command))
    try:
      items = list(parameter_info.Execute(command))
    except (Exception, SystemExit) as e:  # pylint: disable=broad-except
      log.info(unicode(e).rstrip())
      raise (type(e))(u'Update command [{}]: {}'.format(
          ' '.join(command), unicode(e).rstrip()))
    return [self.StringToRow(item) for item in items]


class ResourceSearchCompleter(ResourceCompleter):
  """A parameterized completer that uses Cloud Resource Search for updates."""

  def Update(self, parameter_info, aggregations):
    """Returns the current list of parsed resources."""
    query = '@type:{}'.format(self.collection)
    log.info('cloud resource search query: %s' % query)
    try:
      items = resource_search.List(query=query, uri=True)
    except Exception as e:  # pylint: disable=broad-except
      log.info(unicode(e).rstrip())
      raise (type(e))(u'Update resource query [{}]: {}'.format(
          query, unicode(e).rstrip()))
    return [self.StringToRow(item) for item in items]


class ResourceParamCompleter(ListCommandCompleter):
  """A completer that produces a resource list for one resource param."""

  def __init__(self, collection=None, param=None, timeout=60, **kwargs):
    super(ResourceParamCompleter, self).__init__(
        collection=collection,
        param=param,
        timeout=timeout,
        **kwargs)

  def RowToString(self, row, parameter_info=None):
    """Returns the string representation of row."""
    return row[self.column]


class MultiResourceCompleter(Converter):
  """A completer that composes multiple resource completers.

  Attributes:
    completers: The list of completers.
  """

  def __init__(self, completers=None, qualified_parameter_names=None, **kwargs):
    """Constructor.

    Args:
      completers: The list of completers.
      qualified_parameter_names: The set of parameter names that must be
        qualified.
      **kwargs: Base class kwargs.
    """
    self.completers = [completer_class(**kwargs)
                       for completer_class in completers]
    name_count = {}
    if qualified_parameter_names:
      for name in qualified_parameter_names:
        name_count[name] = 1
    for completer in self.completers:
      if completer.parameters:
        for parameter in completer.parameters:
          if parameter.name in name_count:
            name_count[parameter.name] += 1
          else:
            name_count[parameter.name] = 1
    qualified_parameter_names = {
        name for name, count in name_count.iteritems()
        if count != len(self.completers)}

    # The "collection" for a multi resource completer is the common api (first
    # dotted part of the collection) of the sub-completer collections.  It names
    # the property section used to determine default values in the flag
    # completion style.  If there are multiple apis then the combined collection
    # is None which disables property lookup.
    apis = set()
    for completer in self.completers:
      completer.AddQualifiedParameterNames(qualified_parameter_names)
      apis.add(completer.collection.split('.')[0])
    collection = apis.pop() if len(apis) == 1 else None
    super(MultiResourceCompleter, self).__init__(
        collection=collection, **kwargs)

  def Complete(self, prefix, parameter_info):
    """Returns the union of completions from all completers."""
    return sorted(
        {completions
         for completer in self.completers
         for completions in completer.Complete(prefix, parameter_info)})

  def Update(self, parameter_info, aggregations):
    """Update handled by self.completers."""
    del parameter_info
    del aggregations


class NoCacheCompleter(Converter):
  """A completer that does not cache completions."""

  __metaclass__ = abc.ABCMeta

  def __init__(self, cache=None, **kwargs):
    del cache
    super(NoCacheCompleter, self).__init__(**kwargs)

  @abc.abstractmethod
  def Complete(self, prefix, parameter_info):
    """Returns the list of strings matching prefix.

    This method is normally provided by the cache, but must be specified here
    in order to bypass the cache.

    Args:
      prefix: The resource prefix string to match.
      parameter_info: A ParamaterInfo object for accessing parameter values in
        the program state.

    Returns:
      The list of strings matching prefix.
    """
    del prefix
    del parameter_info

  def Update(self, parameter_info=None, aggregations=None):
    """Satisfies abc resolution and will never be called."""
    del parameter_info, aggregations
