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


from .services.cloud_deploy import CloudDeployClient
from .services.cloud_deploy import CloudDeployAsyncClient

from .types.cloud_deploy import AbandonReleaseRequest
from .types.cloud_deploy import AbandonReleaseResponse
from .types.cloud_deploy import AnthosCluster
from .types.cloud_deploy import ApproveRolloutRequest
from .types.cloud_deploy import ApproveRolloutResponse
from .types.cloud_deploy import BuildArtifact
from .types.cloud_deploy import CloudRunLocation
from .types.cloud_deploy import CloudRunMetadata
from .types.cloud_deploy import Config
from .types.cloud_deploy import CreateDeliveryPipelineRequest
from .types.cloud_deploy import CreateReleaseRequest
from .types.cloud_deploy import CreateRolloutRequest
from .types.cloud_deploy import CreateTargetRequest
from .types.cloud_deploy import DefaultPool
from .types.cloud_deploy import DeleteDeliveryPipelineRequest
from .types.cloud_deploy import DeleteTargetRequest
from .types.cloud_deploy import DeliveryPipeline
from .types.cloud_deploy import DeployJob
from .types.cloud_deploy import DeployJobRun
from .types.cloud_deploy import DeployJobRunMetadata
from .types.cloud_deploy import DeploymentJobs
from .types.cloud_deploy import ExecutionConfig
from .types.cloud_deploy import GetConfigRequest
from .types.cloud_deploy import GetDeliveryPipelineRequest
from .types.cloud_deploy import GetJobRunRequest
from .types.cloud_deploy import GetReleaseRequest
from .types.cloud_deploy import GetRolloutRequest
from .types.cloud_deploy import GetTargetRequest
from .types.cloud_deploy import GkeCluster
from .types.cloud_deploy import Job
from .types.cloud_deploy import JobRun
from .types.cloud_deploy import ListDeliveryPipelinesRequest
from .types.cloud_deploy import ListDeliveryPipelinesResponse
from .types.cloud_deploy import ListJobRunsRequest
from .types.cloud_deploy import ListJobRunsResponse
from .types.cloud_deploy import ListReleasesRequest
from .types.cloud_deploy import ListReleasesResponse
from .types.cloud_deploy import ListRolloutsRequest
from .types.cloud_deploy import ListRolloutsResponse
from .types.cloud_deploy import ListTargetsRequest
from .types.cloud_deploy import ListTargetsResponse
from .types.cloud_deploy import Metadata
from .types.cloud_deploy import OperationMetadata
from .types.cloud_deploy import Phase
from .types.cloud_deploy import PipelineCondition
from .types.cloud_deploy import PipelineReadyCondition
from .types.cloud_deploy import PrivatePool
from .types.cloud_deploy import Release
from .types.cloud_deploy import RetryJobRequest
from .types.cloud_deploy import RetryJobResponse
from .types.cloud_deploy import Rollout
from .types.cloud_deploy import SerialPipeline
from .types.cloud_deploy import SkaffoldVersion
from .types.cloud_deploy import Stage
from .types.cloud_deploy import Standard
from .types.cloud_deploy import Strategy
from .types.cloud_deploy import Target
from .types.cloud_deploy import TargetArtifact
from .types.cloud_deploy import TargetsPresentCondition
from .types.cloud_deploy import UpdateDeliveryPipelineRequest
from .types.cloud_deploy import UpdateTargetRequest
from .types.cloud_deploy import VerifyJob
from .types.cloud_deploy import VerifyJobRun
from .types.deliverypipeline_notification_payload import DeliveryPipelineNotificationEvent
from .types.jobrun_notification_payload import JobRunNotificationEvent
from .types.log_enums import Type
from .types.release_notification_payload import ReleaseNotificationEvent
from .types.release_render_payload import ReleaseRenderEvent
from .types.rollout_notification_payload import RolloutNotificationEvent
from .types.target_notification_payload import TargetNotificationEvent

__all__ = (
    'CloudDeployAsyncClient',
'AbandonReleaseRequest',
'AbandonReleaseResponse',
'AnthosCluster',
'ApproveRolloutRequest',
'ApproveRolloutResponse',
'BuildArtifact',
'CloudDeployClient',
'CloudRunLocation',
'CloudRunMetadata',
'Config',
'CreateDeliveryPipelineRequest',
'CreateReleaseRequest',
'CreateRolloutRequest',
'CreateTargetRequest',
'DefaultPool',
'DeleteDeliveryPipelineRequest',
'DeleteTargetRequest',
'DeliveryPipeline',
'DeliveryPipelineNotificationEvent',
'DeployJob',
'DeployJobRun',
'DeployJobRunMetadata',
'DeploymentJobs',
'ExecutionConfig',
'GetConfigRequest',
'GetDeliveryPipelineRequest',
'GetJobRunRequest',
'GetReleaseRequest',
'GetRolloutRequest',
'GetTargetRequest',
'GkeCluster',
'Job',
'JobRun',
'JobRunNotificationEvent',
'ListDeliveryPipelinesRequest',
'ListDeliveryPipelinesResponse',
'ListJobRunsRequest',
'ListJobRunsResponse',
'ListReleasesRequest',
'ListReleasesResponse',
'ListRolloutsRequest',
'ListRolloutsResponse',
'ListTargetsRequest',
'ListTargetsResponse',
'Metadata',
'OperationMetadata',
'Phase',
'PipelineCondition',
'PipelineReadyCondition',
'PrivatePool',
'Release',
'ReleaseNotificationEvent',
'ReleaseRenderEvent',
'RetryJobRequest',
'RetryJobResponse',
'Rollout',
'RolloutNotificationEvent',
'SerialPipeline',
'SkaffoldVersion',
'Stage',
'Standard',
'Strategy',
'Target',
'TargetArtifact',
'TargetNotificationEvent',
'TargetsPresentCondition',
'Type',
'UpdateDeliveryPipelineRequest',
'UpdateTargetRequest',
'VerifyJob',
'VerifyJobRun',
)