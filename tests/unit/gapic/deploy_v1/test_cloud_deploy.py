# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import math
import os

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
import mock
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.deploy_v1.services.cloud_deploy import (
    CloudDeployAsyncClient,
    CloudDeployClient,
    pagers,
    transports,
)
from google.cloud.deploy_v1.types import cloud_deploy


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudDeployClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudDeployClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudDeployClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudDeployClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudDeployClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudDeployClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudDeployClient, "grpc"),
        (CloudDeployAsyncClient, "grpc_asyncio"),
    ],
)
def test_cloud_deploy_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("clouddeploy.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudDeployGrpcTransport, "grpc"),
        (transports.CloudDeployGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_cloud_deploy_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudDeployClient, "grpc"),
        (CloudDeployAsyncClient, "grpc_asyncio"),
    ],
)
def test_cloud_deploy_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("clouddeploy.googleapis.com:443")


def test_cloud_deploy_client_get_transport_class():
    transport = CloudDeployClient.get_transport_class()
    available_transports = [
        transports.CloudDeployGrpcTransport,
    ]
    assert transport in available_transports

    transport = CloudDeployClient.get_transport_class("grpc")
    assert transport == transports.CloudDeployGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc"),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CloudDeployClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudDeployClient)
)
@mock.patch.object(
    CloudDeployAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudDeployAsyncClient),
)
def test_cloud_deploy_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudDeployClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudDeployClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc", "true"),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc", "false"),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudDeployClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudDeployClient)
)
@mock.patch.object(
    CloudDeployAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudDeployAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_deploy_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize("client_class", [CloudDeployClient, CloudDeployAsyncClient])
@mock.patch.object(
    CloudDeployClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudDeployClient)
)
@mock.patch.object(
    CloudDeployAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudDeployAsyncClient),
)
def test_cloud_deploy_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc"),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_deploy_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc", grpc_helpers),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_deploy_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_cloud_deploy_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.deploy_v1.services.cloud_deploy.transports.CloudDeployGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudDeployClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport, "grpc", grpc_helpers),
        (
            CloudDeployAsyncClient,
            transports.CloudDeployGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_deploy_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "clouddeploy.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="clouddeploy.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.ListDeliveryPipelinesRequest,
        dict,
    ],
)
def test_list_delivery_pipelines(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListDeliveryPipelinesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_delivery_pipelines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListDeliveryPipelinesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeliveryPipelinesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_delivery_pipelines_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        client.list_delivery_pipelines()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListDeliveryPipelinesRequest()


@pytest.mark.asyncio
async def test_list_delivery_pipelines_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_deploy.ListDeliveryPipelinesRequest,
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListDeliveryPipelinesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_delivery_pipelines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListDeliveryPipelinesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeliveryPipelinesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_delivery_pipelines_async_from_dict():
    await test_list_delivery_pipelines_async(request_type=dict)


def test_list_delivery_pipelines_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListDeliveryPipelinesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        call.return_value = cloud_deploy.ListDeliveryPipelinesResponse()
        client.list_delivery_pipelines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_delivery_pipelines_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListDeliveryPipelinesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListDeliveryPipelinesResponse()
        )
        await client.list_delivery_pipelines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_delivery_pipelines_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListDeliveryPipelinesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_delivery_pipelines(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_delivery_pipelines_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_delivery_pipelines(
            cloud_deploy.ListDeliveryPipelinesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_delivery_pipelines_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListDeliveryPipelinesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListDeliveryPipelinesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_delivery_pipelines(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_delivery_pipelines_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_delivery_pipelines(
            cloud_deploy.ListDeliveryPipelinesRequest(),
            parent="parent_value",
        )


def test_list_delivery_pipelines_pager(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[],
                next_page_token="def",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_delivery_pipelines(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_deploy.DeliveryPipeline) for i in results)


def test_list_delivery_pipelines_pages(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[],
                next_page_token="def",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_delivery_pipelines(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_delivery_pipelines_async_pager():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[],
                next_page_token="def",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_delivery_pipelines(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_deploy.DeliveryPipeline) for i in responses)


@pytest.mark.asyncio
async def test_list_delivery_pipelines_async_pages():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_delivery_pipelines),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[],
                next_page_token="def",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListDeliveryPipelinesResponse(
                delivery_pipelines=[
                    cloud_deploy.DeliveryPipeline(),
                    cloud_deploy.DeliveryPipeline(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_delivery_pipelines(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.GetDeliveryPipelineRequest,
        dict,
    ],
)
def test_get_delivery_pipeline(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.DeliveryPipeline(
            name="name_value",
            uid="uid_value",
            description="description_value",
            etag="etag_value",
            serial_pipeline=cloud_deploy.SerialPipeline(
                stages=[cloud_deploy.Stage(target_id="target_id_value")]
            ),
        )
        response = client.get_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.DeliveryPipeline)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


def test_get_delivery_pipeline_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        client.get_delivery_pipeline()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetDeliveryPipelineRequest()


@pytest.mark.asyncio
async def test_get_delivery_pipeline_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_deploy.GetDeliveryPipelineRequest,
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.DeliveryPipeline(
                name="name_value",
                uid="uid_value",
                description="description_value",
                etag="etag_value",
            )
        )
        response = await client.get_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.DeliveryPipeline)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_delivery_pipeline_async_from_dict():
    await test_get_delivery_pipeline_async(request_type=dict)


def test_get_delivery_pipeline_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetDeliveryPipelineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = cloud_deploy.DeliveryPipeline()
        client.get_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_delivery_pipeline_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetDeliveryPipelineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.DeliveryPipeline()
        )
        await client.get_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_delivery_pipeline_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.DeliveryPipeline()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_delivery_pipeline(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_delivery_pipeline_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_delivery_pipeline(
            cloud_deploy.GetDeliveryPipelineRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_delivery_pipeline_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.DeliveryPipeline()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.DeliveryPipeline()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_delivery_pipeline(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_delivery_pipeline_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_delivery_pipeline(
            cloud_deploy.GetDeliveryPipelineRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.CreateDeliveryPipelineRequest,
        dict,
    ],
)
def test_create_delivery_pipeline(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_delivery_pipeline_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        client.create_delivery_pipeline()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateDeliveryPipelineRequest()


@pytest.mark.asyncio
async def test_create_delivery_pipeline_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_deploy.CreateDeliveryPipelineRequest,
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_delivery_pipeline_async_from_dict():
    await test_create_delivery_pipeline_async(request_type=dict)


def test_create_delivery_pipeline_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateDeliveryPipelineRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_delivery_pipeline_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateDeliveryPipelineRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_delivery_pipeline_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_delivery_pipeline(
            parent="parent_value",
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            delivery_pipeline_id="delivery_pipeline_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].delivery_pipeline
        mock_val = cloud_deploy.DeliveryPipeline(name="name_value")
        assert arg == mock_val
        arg = args[0].delivery_pipeline_id
        mock_val = "delivery_pipeline_id_value"
        assert arg == mock_val


def test_create_delivery_pipeline_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_delivery_pipeline(
            cloud_deploy.CreateDeliveryPipelineRequest(),
            parent="parent_value",
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            delivery_pipeline_id="delivery_pipeline_id_value",
        )


@pytest.mark.asyncio
async def test_create_delivery_pipeline_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_delivery_pipeline(
            parent="parent_value",
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            delivery_pipeline_id="delivery_pipeline_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].delivery_pipeline
        mock_val = cloud_deploy.DeliveryPipeline(name="name_value")
        assert arg == mock_val
        arg = args[0].delivery_pipeline_id
        mock_val = "delivery_pipeline_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_delivery_pipeline_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_delivery_pipeline(
            cloud_deploy.CreateDeliveryPipelineRequest(),
            parent="parent_value",
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            delivery_pipeline_id="delivery_pipeline_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.UpdateDeliveryPipelineRequest,
        dict,
    ],
)
def test_update_delivery_pipeline(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_delivery_pipeline_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        client.update_delivery_pipeline()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateDeliveryPipelineRequest()


@pytest.mark.asyncio
async def test_update_delivery_pipeline_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_deploy.UpdateDeliveryPipelineRequest,
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_delivery_pipeline_async_from_dict():
    await test_update_delivery_pipeline_async(request_type=dict)


def test_update_delivery_pipeline_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.UpdateDeliveryPipelineRequest()

    request.delivery_pipeline.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "delivery_pipeline.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_delivery_pipeline_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.UpdateDeliveryPipelineRequest()

    request.delivery_pipeline.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "delivery_pipeline.name=name_value",
    ) in kw["metadata"]


def test_update_delivery_pipeline_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_delivery_pipeline(
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].delivery_pipeline
        mock_val = cloud_deploy.DeliveryPipeline(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_delivery_pipeline_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_delivery_pipeline(
            cloud_deploy.UpdateDeliveryPipelineRequest(),
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_delivery_pipeline_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_delivery_pipeline(
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].delivery_pipeline
        mock_val = cloud_deploy.DeliveryPipeline(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_delivery_pipeline_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_delivery_pipeline(
            cloud_deploy.UpdateDeliveryPipelineRequest(),
            delivery_pipeline=cloud_deploy.DeliveryPipeline(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.DeleteDeliveryPipelineRequest,
        dict,
    ],
)
def test_delete_delivery_pipeline(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_delivery_pipeline_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        client.delete_delivery_pipeline()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteDeliveryPipelineRequest()


@pytest.mark.asyncio
async def test_delete_delivery_pipeline_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_deploy.DeleteDeliveryPipelineRequest,
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteDeliveryPipelineRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_delivery_pipeline_async_from_dict():
    await test_delete_delivery_pipeline_async(request_type=dict)


def test_delete_delivery_pipeline_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.DeleteDeliveryPipelineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_delivery_pipeline_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.DeleteDeliveryPipelineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_delivery_pipeline(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_delivery_pipeline_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_delivery_pipeline(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_delivery_pipeline_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_delivery_pipeline(
            cloud_deploy.DeleteDeliveryPipelineRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_delivery_pipeline_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_delivery_pipeline), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_delivery_pipeline(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_delivery_pipeline_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_delivery_pipeline(
            cloud_deploy.DeleteDeliveryPipelineRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.ListTargetsRequest,
        dict,
    ],
)
def test_list_targets(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListTargetsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_targets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListTargetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTargetsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_targets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        client.list_targets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListTargetsRequest()


@pytest.mark.asyncio
async def test_list_targets_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.ListTargetsRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListTargetsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_targets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListTargetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTargetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_targets_async_from_dict():
    await test_list_targets_async(request_type=dict)


def test_list_targets_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListTargetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        call.return_value = cloud_deploy.ListTargetsResponse()
        client.list_targets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_targets_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListTargetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListTargetsResponse()
        )
        await client.list_targets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_targets_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListTargetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_targets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_targets_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_targets(
            cloud_deploy.ListTargetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_targets_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListTargetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListTargetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_targets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_targets_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_targets(
            cloud_deploy.ListTargetsRequest(),
            parent="parent_value",
        )


def test_list_targets_pager(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[],
                next_page_token="def",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_targets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_deploy.Target) for i in results)


def test_list_targets_pages(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_targets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[],
                next_page_token="def",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_targets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_targets_async_pager():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_targets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[],
                next_page_token="def",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_targets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_deploy.Target) for i in responses)


@pytest.mark.asyncio
async def test_list_targets_async_pages():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_targets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[],
                next_page_token="def",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListTargetsResponse(
                targets=[
                    cloud_deploy.Target(),
                    cloud_deploy.Target(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_targets(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.GetTargetRequest,
        dict,
    ],
)
def test_get_target(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Target(
            name="name_value",
            target_id="target_id_value",
            uid="uid_value",
            description="description_value",
            require_approval=True,
            etag="etag_value",
            gke=cloud_deploy.GkeCluster(cluster="cluster_value"),
        )
        response = client.get_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Target)
    assert response.name == "name_value"
    assert response.target_id == "target_id_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.require_approval is True
    assert response.etag == "etag_value"


def test_get_target_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        client.get_target()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetTargetRequest()


@pytest.mark.asyncio
async def test_get_target_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.GetTargetRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Target(
                name="name_value",
                target_id="target_id_value",
                uid="uid_value",
                description="description_value",
                require_approval=True,
                etag="etag_value",
            )
        )
        response = await client.get_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Target)
    assert response.name == "name_value"
    assert response.target_id == "target_id_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.require_approval is True
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_target_async_from_dict():
    await test_get_target_async(request_type=dict)


def test_get_target_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetTargetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        call.return_value = cloud_deploy.Target()
        client.get_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_target_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetTargetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_deploy.Target())
        await client.get_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_target_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Target()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_target(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_target_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_target(
            cloud_deploy.GetTargetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_target_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Target()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_deploy.Target())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_target(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_target_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_target(
            cloud_deploy.GetTargetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.CreateTargetRequest,
        dict,
    ],
)
def test_create_target(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_target_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        client.create_target()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateTargetRequest()


@pytest.mark.asyncio
async def test_create_target_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.CreateTargetRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_target_async_from_dict():
    await test_create_target_async(request_type=dict)


def test_create_target_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateTargetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_target_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateTargetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_target_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_target(
            parent="parent_value",
            target=cloud_deploy.Target(name="name_value"),
            target_id="target_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].target
        mock_val = cloud_deploy.Target(name="name_value")
        assert arg == mock_val
        arg = args[0].target_id
        mock_val = "target_id_value"
        assert arg == mock_val


def test_create_target_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_target(
            cloud_deploy.CreateTargetRequest(),
            parent="parent_value",
            target=cloud_deploy.Target(name="name_value"),
            target_id="target_id_value",
        )


@pytest.mark.asyncio
async def test_create_target_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_target(
            parent="parent_value",
            target=cloud_deploy.Target(name="name_value"),
            target_id="target_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].target
        mock_val = cloud_deploy.Target(name="name_value")
        assert arg == mock_val
        arg = args[0].target_id
        mock_val = "target_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_target_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_target(
            cloud_deploy.CreateTargetRequest(),
            parent="parent_value",
            target=cloud_deploy.Target(name="name_value"),
            target_id="target_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.UpdateTargetRequest,
        dict,
    ],
)
def test_update_target(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_target_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        client.update_target()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateTargetRequest()


@pytest.mark.asyncio
async def test_update_target_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.UpdateTargetRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.UpdateTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_target_async_from_dict():
    await test_update_target_async(request_type=dict)


def test_update_target_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.UpdateTargetRequest()

    request.target.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "target.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_target_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.UpdateTargetRequest()

    request.target.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "target.name=name_value",
    ) in kw["metadata"]


def test_update_target_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_target(
            target=cloud_deploy.Target(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].target
        mock_val = cloud_deploy.Target(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_target_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_target(
            cloud_deploy.UpdateTargetRequest(),
            target=cloud_deploy.Target(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_target_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_target(
            target=cloud_deploy.Target(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].target
        mock_val = cloud_deploy.Target(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_target_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_target(
            cloud_deploy.UpdateTargetRequest(),
            target=cloud_deploy.Target(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.DeleteTargetRequest,
        dict,
    ],
)
def test_delete_target(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_target_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        client.delete_target()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteTargetRequest()


@pytest.mark.asyncio
async def test_delete_target_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.DeleteTargetRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.DeleteTargetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_target_async_from_dict():
    await test_delete_target_async(request_type=dict)


def test_delete_target_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.DeleteTargetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_target_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.DeleteTargetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_target(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_target_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_target(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_target_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_target(
            cloud_deploy.DeleteTargetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_target_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_target), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_target(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_target_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_target(
            cloud_deploy.DeleteTargetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.ListReleasesRequest,
        dict,
    ],
)
def test_list_releases(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListReleasesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_releases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListReleasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReleasesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_releases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        client.list_releases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListReleasesRequest()


@pytest.mark.asyncio
async def test_list_releases_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.ListReleasesRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListReleasesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_releases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListReleasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReleasesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_releases_async_from_dict():
    await test_list_releases_async(request_type=dict)


def test_list_releases_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListReleasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        call.return_value = cloud_deploy.ListReleasesResponse()
        client.list_releases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_releases_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListReleasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListReleasesResponse()
        )
        await client.list_releases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_releases_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListReleasesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_releases(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_releases_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_releases(
            cloud_deploy.ListReleasesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_releases_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListReleasesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListReleasesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_releases(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_releases_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_releases(
            cloud_deploy.ListReleasesRequest(),
            parent="parent_value",
        )


def test_list_releases_pager(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[],
                next_page_token="def",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_releases(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_deploy.Release) for i in results)


def test_list_releases_pages(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_releases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[],
                next_page_token="def",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_releases(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_releases_async_pager():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_releases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[],
                next_page_token="def",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_releases(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_deploy.Release) for i in responses)


@pytest.mark.asyncio
async def test_list_releases_async_pages():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_releases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[],
                next_page_token="def",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListReleasesResponse(
                releases=[
                    cloud_deploy.Release(),
                    cloud_deploy.Release(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_releases(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.GetReleaseRequest,
        dict,
    ],
)
def test_get_release(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Release(
            name="name_value",
            uid="uid_value",
            description="description_value",
            skaffold_config_uri="skaffold_config_uri_value",
            skaffold_config_path="skaffold_config_path_value",
            render_state=cloud_deploy.Release.RenderState.SUCCEEDED,
            etag="etag_value",
            skaffold_version="skaffold_version_value",
        )
        response = client.get_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetReleaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Release)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.skaffold_config_uri == "skaffold_config_uri_value"
    assert response.skaffold_config_path == "skaffold_config_path_value"
    assert response.render_state == cloud_deploy.Release.RenderState.SUCCEEDED
    assert response.etag == "etag_value"
    assert response.skaffold_version == "skaffold_version_value"


def test_get_release_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        client.get_release()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetReleaseRequest()


@pytest.mark.asyncio
async def test_get_release_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.GetReleaseRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Release(
                name="name_value",
                uid="uid_value",
                description="description_value",
                skaffold_config_uri="skaffold_config_uri_value",
                skaffold_config_path="skaffold_config_path_value",
                render_state=cloud_deploy.Release.RenderState.SUCCEEDED,
                etag="etag_value",
                skaffold_version="skaffold_version_value",
            )
        )
        response = await client.get_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetReleaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Release)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.skaffold_config_uri == "skaffold_config_uri_value"
    assert response.skaffold_config_path == "skaffold_config_path_value"
    assert response.render_state == cloud_deploy.Release.RenderState.SUCCEEDED
    assert response.etag == "etag_value"
    assert response.skaffold_version == "skaffold_version_value"


@pytest.mark.asyncio
async def test_get_release_async_from_dict():
    await test_get_release_async(request_type=dict)


def test_get_release_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetReleaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        call.return_value = cloud_deploy.Release()
        client.get_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_release_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetReleaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Release()
        )
        await client.get_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_release_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Release()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_release(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_release_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_release(
            cloud_deploy.GetReleaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_release_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Release()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Release()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_release(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_release_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_release(
            cloud_deploy.GetReleaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.CreateReleaseRequest,
        dict,
    ],
)
def test_create_release(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateReleaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_release_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        client.create_release()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateReleaseRequest()


@pytest.mark.asyncio
async def test_create_release_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.CreateReleaseRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateReleaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_release_async_from_dict():
    await test_create_release_async(request_type=dict)


def test_create_release_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateReleaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_release_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateReleaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_release(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_release_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_release(
            parent="parent_value",
            release=cloud_deploy.Release(name="name_value"),
            release_id="release_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].release
        mock_val = cloud_deploy.Release(name="name_value")
        assert arg == mock_val
        arg = args[0].release_id
        mock_val = "release_id_value"
        assert arg == mock_val


def test_create_release_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_release(
            cloud_deploy.CreateReleaseRequest(),
            parent="parent_value",
            release=cloud_deploy.Release(name="name_value"),
            release_id="release_id_value",
        )


@pytest.mark.asyncio
async def test_create_release_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_release), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_release(
            parent="parent_value",
            release=cloud_deploy.Release(name="name_value"),
            release_id="release_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].release
        mock_val = cloud_deploy.Release(name="name_value")
        assert arg == mock_val
        arg = args[0].release_id
        mock_val = "release_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_release_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_release(
            cloud_deploy.CreateReleaseRequest(),
            parent="parent_value",
            release=cloud_deploy.Release(name="name_value"),
            release_id="release_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.ApproveRolloutRequest,
        dict,
    ],
)
def test_approve_rollout(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ApproveRolloutResponse()
        response = client.approve_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ApproveRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.ApproveRolloutResponse)


def test_approve_rollout_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        client.approve_rollout()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ApproveRolloutRequest()


@pytest.mark.asyncio
async def test_approve_rollout_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.ApproveRolloutRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ApproveRolloutResponse()
        )
        response = await client.approve_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ApproveRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.ApproveRolloutResponse)


@pytest.mark.asyncio
async def test_approve_rollout_async_from_dict():
    await test_approve_rollout_async(request_type=dict)


def test_approve_rollout_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ApproveRolloutRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        call.return_value = cloud_deploy.ApproveRolloutResponse()
        client.approve_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_approve_rollout_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ApproveRolloutRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ApproveRolloutResponse()
        )
        await client.approve_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_approve_rollout_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ApproveRolloutResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.approve_rollout(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_approve_rollout_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_rollout(
            cloud_deploy.ApproveRolloutRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_approve_rollout_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ApproveRolloutResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ApproveRolloutResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.approve_rollout(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_approve_rollout_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.approve_rollout(
            cloud_deploy.ApproveRolloutRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.ListRolloutsRequest,
        dict,
    ],
)
def test_list_rollouts(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListRolloutsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListRolloutsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRolloutsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_rollouts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        client.list_rollouts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListRolloutsRequest()


@pytest.mark.asyncio
async def test_list_rollouts_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.ListRolloutsRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListRolloutsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.ListRolloutsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRolloutsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_rollouts_async_from_dict():
    await test_list_rollouts_async(request_type=dict)


def test_list_rollouts_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListRolloutsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        call.return_value = cloud_deploy.ListRolloutsResponse()
        client.list_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_rollouts_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.ListRolloutsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListRolloutsResponse()
        )
        await client.list_rollouts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_rollouts_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListRolloutsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_rollouts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_rollouts_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rollouts(
            cloud_deploy.ListRolloutsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_rollouts_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.ListRolloutsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.ListRolloutsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_rollouts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_rollouts_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_rollouts(
            cloud_deploy.ListRolloutsRequest(),
            parent="parent_value",
        )


def test_list_rollouts_pager(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[],
                next_page_token="def",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_rollouts(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloud_deploy.Rollout) for i in results)


def test_list_rollouts_pages(transport_name: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rollouts), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[],
                next_page_token="def",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_rollouts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_rollouts_async_pager():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rollouts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[],
                next_page_token="def",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_rollouts(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_deploy.Rollout) for i in responses)


@pytest.mark.asyncio
async def test_list_rollouts_async_pages():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rollouts), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
                next_page_token="abc",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[],
                next_page_token="def",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                ],
                next_page_token="ghi",
            ),
            cloud_deploy.ListRolloutsResponse(
                rollouts=[
                    cloud_deploy.Rollout(),
                    cloud_deploy.Rollout(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_rollouts(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.GetRolloutRequest,
        dict,
    ],
)
def test_get_rollout(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Rollout(
            name="name_value",
            uid="uid_value",
            description="description_value",
            target_id="target_id_value",
            approval_state=cloud_deploy.Rollout.ApprovalState.NEEDS_APPROVAL,
            state=cloud_deploy.Rollout.State.SUCCEEDED,
            failure_reason="failure_reason_value",
            deploying_build="deploying_build_value",
            etag="etag_value",
            deploy_failure_cause=cloud_deploy.Rollout.FailureCause.CLOUD_BUILD_UNAVAILABLE,
        )
        response = client.get_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Rollout)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.target_id == "target_id_value"
    assert response.approval_state == cloud_deploy.Rollout.ApprovalState.NEEDS_APPROVAL
    assert response.state == cloud_deploy.Rollout.State.SUCCEEDED
    assert response.failure_reason == "failure_reason_value"
    assert response.deploying_build == "deploying_build_value"
    assert response.etag == "etag_value"
    assert (
        response.deploy_failure_cause
        == cloud_deploy.Rollout.FailureCause.CLOUD_BUILD_UNAVAILABLE
    )


def test_get_rollout_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        client.get_rollout()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetRolloutRequest()


@pytest.mark.asyncio
async def test_get_rollout_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.GetRolloutRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Rollout(
                name="name_value",
                uid="uid_value",
                description="description_value",
                target_id="target_id_value",
                approval_state=cloud_deploy.Rollout.ApprovalState.NEEDS_APPROVAL,
                state=cloud_deploy.Rollout.State.SUCCEEDED,
                failure_reason="failure_reason_value",
                deploying_build="deploying_build_value",
                etag="etag_value",
                deploy_failure_cause=cloud_deploy.Rollout.FailureCause.CLOUD_BUILD_UNAVAILABLE,
            )
        )
        response = await client.get_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Rollout)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.target_id == "target_id_value"
    assert response.approval_state == cloud_deploy.Rollout.ApprovalState.NEEDS_APPROVAL
    assert response.state == cloud_deploy.Rollout.State.SUCCEEDED
    assert response.failure_reason == "failure_reason_value"
    assert response.deploying_build == "deploying_build_value"
    assert response.etag == "etag_value"
    assert (
        response.deploy_failure_cause
        == cloud_deploy.Rollout.FailureCause.CLOUD_BUILD_UNAVAILABLE
    )


@pytest.mark.asyncio
async def test_get_rollout_async_from_dict():
    await test_get_rollout_async(request_type=dict)


def test_get_rollout_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetRolloutRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        call.return_value = cloud_deploy.Rollout()
        client.get_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_rollout_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetRolloutRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Rollout()
        )
        await client.get_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_rollout_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Rollout()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_rollout(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_rollout_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rollout(
            cloud_deploy.GetRolloutRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_rollout_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Rollout()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Rollout()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_rollout(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_rollout_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_rollout(
            cloud_deploy.GetRolloutRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.CreateRolloutRequest,
        dict,
    ],
)
def test_create_rollout(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_rollout_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        client.create_rollout()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateRolloutRequest()


@pytest.mark.asyncio
async def test_create_rollout_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.CreateRolloutRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.CreateRolloutRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_rollout_async_from_dict():
    await test_create_rollout_async(request_type=dict)


def test_create_rollout_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateRolloutRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_rollout_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.CreateRolloutRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_rollout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_rollout_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_rollout(
            parent="parent_value",
            rollout=cloud_deploy.Rollout(name="name_value"),
            rollout_id="rollout_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rollout
        mock_val = cloud_deploy.Rollout(name="name_value")
        assert arg == mock_val
        arg = args[0].rollout_id
        mock_val = "rollout_id_value"
        assert arg == mock_val


def test_create_rollout_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_rollout(
            cloud_deploy.CreateRolloutRequest(),
            parent="parent_value",
            rollout=cloud_deploy.Rollout(name="name_value"),
            rollout_id="rollout_id_value",
        )


@pytest.mark.asyncio
async def test_create_rollout_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rollout), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_rollout(
            parent="parent_value",
            rollout=cloud_deploy.Rollout(name="name_value"),
            rollout_id="rollout_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rollout
        mock_val = cloud_deploy.Rollout(name="name_value")
        assert arg == mock_val
        arg = args[0].rollout_id
        mock_val = "rollout_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_rollout_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_rollout(
            cloud_deploy.CreateRolloutRequest(),
            parent="parent_value",
            rollout=cloud_deploy.Rollout(name="name_value"),
            rollout_id="rollout_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloud_deploy.GetConfigRequest,
        dict,
    ],
)
def test_get_config(request_type, transport: str = "grpc"):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Config(
            name="name_value",
            default_skaffold_version="default_skaffold_version_value",
        )
        response = client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Config)
    assert response.name == "name_value"
    assert response.default_skaffold_version == "default_skaffold_version_value"


def test_get_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        client.get_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetConfigRequest()


@pytest.mark.asyncio
async def test_get_config_async(
    transport: str = "grpc_asyncio", request_type=cloud_deploy.GetConfigRequest
):
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_deploy.Config(
                name="name_value",
                default_skaffold_version="default_skaffold_version_value",
            )
        )
        response = await client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_deploy.GetConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_deploy.Config)
    assert response.name == "name_value"
    assert response.default_skaffold_version == "default_skaffold_version_value"


@pytest.mark.asyncio
async def test_get_config_async_from_dict():
    await test_get_config_async(request_type=dict)


def test_get_config_field_headers():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        call.return_value = cloud_deploy.Config()
        client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_config_field_headers_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_deploy.GetConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_deploy.Config())
        await client.get_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_config_flattened():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Config()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_config_flattened_error():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_config(
            cloud_deploy.GetConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_config_flattened_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_deploy.Config()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_deploy.Config())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_config_flattened_error_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_config(
            cloud_deploy.GetConfigRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudDeployClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudDeployClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudDeployClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudDeployClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudDeployClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudDeployClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudDeployGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudDeployGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudDeployGrpcTransport,
        transports.CloudDeployGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = CloudDeployClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudDeployGrpcTransport,
    )


def test_cloud_deploy_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudDeployTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_deploy_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.deploy_v1.services.cloud_deploy.transports.CloudDeployTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudDeployTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_delivery_pipelines",
        "get_delivery_pipeline",
        "create_delivery_pipeline",
        "update_delivery_pipeline",
        "delete_delivery_pipeline",
        "list_targets",
        "get_target",
        "create_target",
        "update_target",
        "delete_target",
        "list_releases",
        "get_release",
        "create_release",
        "approve_rollout",
        "list_rollouts",
        "get_rollout",
        "create_rollout",
        "get_config",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_cloud_deploy_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.deploy_v1.services.cloud_deploy.transports.CloudDeployTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudDeployTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_deploy_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.deploy_v1.services.cloud_deploy.transports.CloudDeployTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudDeployTransport()
        adc.assert_called_once()


def test_cloud_deploy_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudDeployClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudDeployGrpcTransport,
        transports.CloudDeployGrpcAsyncIOTransport,
    ],
)
def test_cloud_deploy_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CloudDeployGrpcTransport, grpc_helpers),
        (transports.CloudDeployGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_deploy_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "clouddeploy.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="clouddeploy.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudDeployGrpcTransport, transports.CloudDeployGrpcAsyncIOTransport],
)
def test_cloud_deploy_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cloud_deploy_host_no_port(transport_name):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="clouddeploy.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("clouddeploy.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cloud_deploy_host_with_port(transport_name):
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="clouddeploy.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("clouddeploy.googleapis.com:8000")


def test_cloud_deploy_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudDeployGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_deploy_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudDeployGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudDeployGrpcTransport, transports.CloudDeployGrpcAsyncIOTransport],
)
def test_cloud_deploy_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudDeployGrpcTransport, transports.CloudDeployGrpcAsyncIOTransport],
)
def test_cloud_deploy_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_cloud_deploy_grpc_lro_client():
    client = CloudDeployClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cloud_deploy_grpc_lro_async_client():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_build_path():
    project = "squid"
    location = "clam"
    build = "whelk"
    expected = "projects/{project}/locations/{location}/builds/{build}".format(
        project=project,
        location=location,
        build=build,
    )
    actual = CloudDeployClient.build_path(project, location, build)
    assert expected == actual


def test_parse_build_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "build": "nudibranch",
    }
    path = CloudDeployClient.build_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_build_path(path)
    assert expected == actual


def test_cluster_path():
    project = "cuttlefish"
    location = "mussel"
    cluster = "winkle"
    expected = "projects/{project}/locations/{location}/clusters/{cluster}".format(
        project=project,
        location=location,
        cluster=cluster,
    )
    actual = CloudDeployClient.cluster_path(project, location, cluster)
    assert expected == actual


def test_parse_cluster_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "cluster": "abalone",
    }
    path = CloudDeployClient.cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_cluster_path(path)
    assert expected == actual


def test_config_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}/config".format(
        project=project,
        location=location,
    )
    actual = CloudDeployClient.config_path(project, location)
    assert expected == actual


def test_parse_config_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = CloudDeployClient.config_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_config_path(path)
    assert expected == actual


def test_delivery_pipeline_path():
    project = "oyster"
    location = "nudibranch"
    delivery_pipeline = "cuttlefish"
    expected = "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}".format(
        project=project,
        location=location,
        delivery_pipeline=delivery_pipeline,
    )
    actual = CloudDeployClient.delivery_pipeline_path(
        project, location, delivery_pipeline
    )
    assert expected == actual


def test_parse_delivery_pipeline_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "delivery_pipeline": "nautilus",
    }
    path = CloudDeployClient.delivery_pipeline_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_delivery_pipeline_path(path)
    assert expected == actual


def test_membership_path():
    project = "scallop"
    location = "abalone"
    membership = "squid"
    expected = (
        "projects/{project}/locations/{location}/memberships/{membership}".format(
            project=project,
            location=location,
            membership=membership,
        )
    )
    actual = CloudDeployClient.membership_path(project, location, membership)
    assert expected == actual


def test_parse_membership_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "membership": "octopus",
    }
    path = CloudDeployClient.membership_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_membership_path(path)
    assert expected == actual


def test_release_path():
    project = "oyster"
    location = "nudibranch"
    delivery_pipeline = "cuttlefish"
    release = "mussel"
    expected = "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}/releases/{release}".format(
        project=project,
        location=location,
        delivery_pipeline=delivery_pipeline,
        release=release,
    )
    actual = CloudDeployClient.release_path(
        project, location, delivery_pipeline, release
    )
    assert expected == actual


def test_parse_release_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "delivery_pipeline": "scallop",
        "release": "abalone",
    }
    path = CloudDeployClient.release_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_release_path(path)
    assert expected == actual


def test_rollout_path():
    project = "squid"
    location = "clam"
    delivery_pipeline = "whelk"
    release = "octopus"
    rollout = "oyster"
    expected = "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}/releases/{release}/rollouts/{rollout}".format(
        project=project,
        location=location,
        delivery_pipeline=delivery_pipeline,
        release=release,
        rollout=rollout,
    )
    actual = CloudDeployClient.rollout_path(
        project, location, delivery_pipeline, release, rollout
    )
    assert expected == actual


def test_parse_rollout_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "delivery_pipeline": "mussel",
        "release": "winkle",
        "rollout": "nautilus",
    }
    path = CloudDeployClient.rollout_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_rollout_path(path)
    assert expected == actual


def test_target_path():
    project = "scallop"
    location = "abalone"
    target = "squid"
    expected = "projects/{project}/locations/{location}/targets/{target}".format(
        project=project,
        location=location,
        target=target,
    )
    actual = CloudDeployClient.target_path(project, location, target)
    assert expected == actual


def test_parse_target_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "target": "octopus",
    }
    path = CloudDeployClient.target_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_target_path(path)
    assert expected == actual


def test_worker_pool_path():
    project = "oyster"
    location = "nudibranch"
    worker_pool = "cuttlefish"
    expected = (
        "projects/{project}/locations/{location}/workerPools/{worker_pool}".format(
            project=project,
            location=location,
            worker_pool=worker_pool,
        )
    )
    actual = CloudDeployClient.worker_pool_path(project, location, worker_pool)
    assert expected == actual


def test_parse_worker_pool_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "worker_pool": "nautilus",
    }
    path = CloudDeployClient.worker_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_worker_pool_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudDeployClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = CloudDeployClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudDeployClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = CloudDeployClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudDeployClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = CloudDeployClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudDeployClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = CloudDeployClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudDeployClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = CloudDeployClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudDeployClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudDeployTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudDeployClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudDeployTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudDeployClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudDeployAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CloudDeployClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = CloudDeployClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (CloudDeployClient, transports.CloudDeployGrpcTransport),
        (CloudDeployAsyncClient, transports.CloudDeployGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )
