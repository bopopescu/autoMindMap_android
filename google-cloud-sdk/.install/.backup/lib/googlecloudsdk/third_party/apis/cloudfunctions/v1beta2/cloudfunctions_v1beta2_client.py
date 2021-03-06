"""Generated client library for cloudfunctions version v1beta2."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.cloudfunctions.v1beta2 import cloudfunctions_v1beta2_messages as messages


class CloudfunctionsV1beta2(base_api.BaseApiClient):
  """Generated client library for service cloudfunctions version v1beta2."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://cloudfunctions.googleapis.com/'

  _PACKAGE = u'cloudfunctions'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform']
  _VERSION = u'v1beta2'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'CloudfunctionsV1beta2'
  _URL_VERSION = u'v1beta2'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new cloudfunctions handle."""
    url = url or self.BASE_URL
    super(CloudfunctionsV1beta2, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.operations = self.OperationsService(self)
    self.projects_locations_functions = self.ProjectsLocationsFunctionsService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class OperationsService(base_api.BaseApiService):
    """Service class for the operations resource."""

    _NAME = u'operations'

    def __init__(self, client):
      super(CloudfunctionsV1beta2.OperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      """Gets the latest state of a long-running operation.  Clients can use this.
method to poll the operation result at intervals as recommended by the API
service.

      Args:
        request: (CloudfunctionsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/operations/{operationsId}',
        http_method=u'GET',
        method_id=u'cloudfunctions.operations.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}',
        request_field='',
        request_type_name=u'CloudfunctionsOperationsGetRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """Lists operations that match the specified filter in the request. If the.
server doesn't support this method, it returns `UNIMPLEMENTED`.

NOTE: the `name` binding allows API services to override the binding
to use different resource name schemes, such as `users/*/operations`. To
override the binding, API services can add a binding such as
`"/v1/{name=users/*}/operations"` to their service configuration.
For backwards compatibility, the default name includes the operations
collection id, however overriding users must ensure the name binding
is the parent resource, without the operations collection id.

      Args:
        request: (CloudfunctionsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'cloudfunctions.operations.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'filter', u'name', u'pageSize', u'pageToken'],
        relative_path=u'v1beta2/operations',
        request_field='',
        request_type_name=u'CloudfunctionsOperationsListRequest',
        response_type_name=u'ListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsFunctionsService(base_api.BaseApiService):
    """Service class for the projects_locations_functions resource."""

    _NAME = u'projects_locations_functions'

    def __init__(self, client):
      super(CloudfunctionsV1beta2.ProjectsLocationsFunctionsService, self).__init__(client)
      self._upload_configs = {
          }

    def Call(self, request, global_params=None):
      """Invokes synchronously deployed function. To be used for testing, very.
limited traffic allowed.

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsCallRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (CallFunctionResponse) The response message.
      """
      config = self.GetMethodConfig('Call')
      return self._RunMethod(
          config, request, global_params=global_params)

    Call.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions/{functionsId}:call',
        http_method=u'POST',
        method_id=u'cloudfunctions.projects.locations.functions.call',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}:call',
        request_field=u'callFunctionRequest',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsCallRequest',
        response_type_name=u'CallFunctionResponse',
        supports_download=False,
    )

    def Create(self, request, global_params=None):
      """Creates a new function. If a function with the given name already exists in.
the specified project, the long running operation will return
`ALREADY_EXISTS` error.

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions',
        http_method=u'POST',
        method_id=u'cloudfunctions.projects.locations.functions.create',
        ordered_params=[u'location'],
        path_params=[u'location'],
        query_params=[],
        relative_path=u'v1beta2/{+location}/functions',
        request_field=u'cloudFunction',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsCreateRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      """Deletes a function with the given name from the specified project. If the.
given function is used by some trigger, the trigger will be updated to
remove this function.

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions/{functionsId}',
        http_method=u'DELETE',
        method_id=u'cloudfunctions.projects.locations.functions.delete',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}',
        request_field='',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsDeleteRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def GenerateDownloadUrl(self, request, global_params=None):
      """Returns a signed URL for downloading deployed function source code.
The URL is only valid for a limited period and should be used within
minutes after generation.
For more information about the signed URL usage see:
https://cloud.google.com/storage/docs/access-control/signed-urls

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsGenerateDownloadUrlRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GenerateDownloadUrlResponse) The response message.
      """
      config = self.GetMethodConfig('GenerateDownloadUrl')
      return self._RunMethod(
          config, request, global_params=global_params)

    GenerateDownloadUrl.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions/{functionsId}:generateDownloadUrl',
        http_method=u'POST',
        method_id=u'cloudfunctions.projects.locations.functions.generateDownloadUrl',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}:generateDownloadUrl',
        request_field=u'generateDownloadUrlRequest',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsGenerateDownloadUrlRequest',
        response_type_name=u'GenerateDownloadUrlResponse',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      """Returns a function with the given name from the requested project.

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (CloudFunction) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions/{functionsId}',
        http_method=u'GET',
        method_id=u'cloudfunctions.projects.locations.functions.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}',
        request_field='',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsGetRequest',
        response_type_name=u'CloudFunction',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """Returns a list of functions that belong to the requested project.

      Args:
        request: (CloudfunctionsProjectsLocationsFunctionsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListFunctionsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions',
        http_method=u'GET',
        method_id=u'cloudfunctions.projects.locations.functions.list',
        ordered_params=[u'location'],
        path_params=[u'location'],
        query_params=[u'pageSize', u'pageToken'],
        relative_path=u'v1beta2/{+location}/functions',
        request_field='',
        request_type_name=u'CloudfunctionsProjectsLocationsFunctionsListRequest',
        response_type_name=u'ListFunctionsResponse',
        supports_download=False,
    )

    def Update(self, request, global_params=None):
      """Updates existing function.

      Args:
        request: (CloudFunction) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Update')
      return self._RunMethod(
          config, request, global_params=global_params)

    Update.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}/functions/{functionsId}',
        http_method=u'PUT',
        method_id=u'cloudfunctions.projects.locations.functions.update',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1beta2/{+name}',
        request_field='<request>',
        request_type_name=u'CloudFunction',
        response_type_name=u'Operation',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = u'projects_locations'

    def __init__(self, client):
      super(CloudfunctionsV1beta2.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def GenerateUploadUrl(self, request, global_params=None):
      """Returns a signed URL for uploading a function source code.
For more information about the signed URL usage see:
https://cloud.google.com/storage/docs/access-control/signed-urls
Once the function source code upload is complete, the used signed
URL should be provided in CreateFunction or UpdateFunction request
as a reference to the function source code.

      Args:
        request: (CloudfunctionsProjectsLocationsGenerateUploadUrlRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GenerateUploadUrlResponse) The response message.
      """
      config = self.GetMethodConfig('GenerateUploadUrl')
      return self._RunMethod(
          config, request, global_params=global_params)

    GenerateUploadUrl.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations/{locationsId}:generateUploadUrl',
        http_method=u'POST',
        method_id=u'cloudfunctions.projects.locations.generateUploadUrl',
        ordered_params=[u'location'],
        path_params=[u'location'],
        query_params=[],
        relative_path=u'v1beta2/{+location}:generateUploadUrl',
        request_field=u'generateUploadUrlRequest',
        request_type_name=u'CloudfunctionsProjectsLocationsGenerateUploadUrlRequest',
        response_type_name=u'GenerateUploadUrlResponse',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """Lists information about the supported locations for this service.

      Args:
        request: (CloudfunctionsProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1beta2/projects/{projectsId}/locations',
        http_method=u'GET',
        method_id=u'cloudfunctions.projects.locations.list',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'filter', u'pageSize', u'pageToken'],
        relative_path=u'v1beta2/{+name}/locations',
        request_field='',
        request_type_name=u'CloudfunctionsProjectsLocationsListRequest',
        response_type_name=u'ListLocationsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(CloudfunctionsV1beta2.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }
