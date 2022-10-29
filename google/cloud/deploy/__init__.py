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
from google.cloud.deploy import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.deploy_v1.services.cloud_deploy.async_client import (
    CloudDeployAsyncClient,
)
from google.cloud.deploy_v1.services.cloud_deploy.client import CloudDeployClient
from google.cloud.deploy_v1.types.cloud_deploy import (
    AbandonReleaseRequest,
    AbandonReleaseResponse,
    AnthosCluster,
    ApproveRolloutRequest,
    ApproveRolloutResponse,
    BuildArtifact,
    CloudRunLocation,
    CloudRunMetadata,
    Config,
    CreateDeliveryPipelineRequest,
    CreateReleaseRequest,
    CreateRolloutRequest,
    CreateTargetRequest,
    DefaultPool,
    DeleteDeliveryPipelineRequest,
    DeleteTargetRequest,
    DeliveryPipeline,
    DeployJob,
    DeployJobRun,
    DeployJobRunMetadata,
    DeploymentJobs,
    ExecutionConfig,
    GetConfigRequest,
    GetDeliveryPipelineRequest,
    GetJobRunRequest,
    GetReleaseRequest,
    GetRolloutRequest,
    GetTargetRequest,
    GkeCluster,
    Job,
    JobRun,
    ListDeliveryPipelinesRequest,
    ListDeliveryPipelinesResponse,
    ListJobRunsRequest,
    ListJobRunsResponse,
    ListReleasesRequest,
    ListReleasesResponse,
    ListRolloutsRequest,
    ListRolloutsResponse,
    ListTargetsRequest,
    ListTargetsResponse,
    Metadata,
    OperationMetadata,
    Phase,
    PipelineCondition,
    PipelineReadyCondition,
    PrivatePool,
    Release,
    RetryJobRequest,
    RetryJobResponse,
    Rollout,
    SerialPipeline,
    SkaffoldVersion,
    Stage,
    Standard,
    Strategy,
    Target,
    TargetArtifact,
    TargetsPresentCondition,
    UpdateDeliveryPipelineRequest,
    UpdateTargetRequest,
    VerifyJob,
    VerifyJobRun,
)
from google.cloud.deploy_v1.types.deliverypipeline_notification_payload import (
    DeliveryPipelineNotificationEvent,
)
from google.cloud.deploy_v1.types.jobrun_notification_payload import (
    JobRunNotificationEvent,
)
from google.cloud.deploy_v1.types.log_enums import Type
from google.cloud.deploy_v1.types.release_notification_payload import (
    ReleaseNotificationEvent,
)
from google.cloud.deploy_v1.types.release_render_payload import ReleaseRenderEvent
from google.cloud.deploy_v1.types.rollout_notification_payload import (
    RolloutNotificationEvent,
)
from google.cloud.deploy_v1.types.target_notification_payload import (
    TargetNotificationEvent,
)

__all__ = (
    "CloudDeployClient",
    "CloudDeployAsyncClient",
    "AbandonReleaseRequest",
    "AbandonReleaseResponse",
    "AnthosCluster",
    "ApproveRolloutRequest",
    "ApproveRolloutResponse",
    "BuildArtifact",
    "CloudRunLocation",
    "CloudRunMetadata",
    "Config",
    "CreateDeliveryPipelineRequest",
    "CreateReleaseRequest",
    "CreateRolloutRequest",
    "CreateTargetRequest",
    "DefaultPool",
    "DeleteDeliveryPipelineRequest",
    "DeleteTargetRequest",
    "DeliveryPipeline",
    "DeployJob",
    "DeployJobRun",
    "DeployJobRunMetadata",
    "DeploymentJobs",
    "ExecutionConfig",
    "GetConfigRequest",
    "GetDeliveryPipelineRequest",
    "GetJobRunRequest",
    "GetReleaseRequest",
    "GetRolloutRequest",
    "GetTargetRequest",
    "GkeCluster",
    "Job",
    "JobRun",
    "ListDeliveryPipelinesRequest",
    "ListDeliveryPipelinesResponse",
    "ListJobRunsRequest",
    "ListJobRunsResponse",
    "ListReleasesRequest",
    "ListReleasesResponse",
    "ListRolloutsRequest",
    "ListRolloutsResponse",
    "ListTargetsRequest",
    "ListTargetsResponse",
    "Metadata",
    "OperationMetadata",
    "Phase",
    "PipelineCondition",
    "PipelineReadyCondition",
    "PrivatePool",
    "Release",
    "RetryJobRequest",
    "RetryJobResponse",
    "Rollout",
    "SerialPipeline",
    "SkaffoldVersion",
    "Stage",
    "Standard",
    "Strategy",
    "Target",
    "TargetArtifact",
    "TargetsPresentCondition",
    "UpdateDeliveryPipelineRequest",
    "UpdateTargetRequest",
    "VerifyJob",
    "VerifyJobRun",
    "DeliveryPipelineNotificationEvent",
    "JobRunNotificationEvent",
    "Type",
    "ReleaseNotificationEvent",
    "ReleaseRenderEvent",
    "RolloutNotificationEvent",
    "TargetNotificationEvent",
)
