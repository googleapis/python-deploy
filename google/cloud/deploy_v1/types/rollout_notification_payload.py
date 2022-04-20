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
import proto  # type: ignore

from google.cloud.deploy_v1.types import log_enums

__protobuf__ = proto.module(
    package="google.cloud.deploy.v1",
    manifest={
        "RolloutNotificationEvent",
    },
)


class RolloutNotificationEvent(proto.Message):
    r"""Payload proto for "clouddeploy.googleapis.com/rollout_notification"
    Platform Log event that describes the failure to send rollout status
    change Pub/Sub notification.

    Attributes:
        message (str):
            Debug message for when a notification fails
            to send.
        pipeline_uid (str):
            Unique identifier of the ``DeliveryPipeline``.
        release_uid (str):
            Unique identifier of the ``Release``.
        rollout (str):
            The name of the ``Rollout``.
        type_ (google.cloud.deploy_v1.types.Type):
            Type of this notification, e.g. for a Pub/Sub
            failure.
        target_id (str):
            ID of the ``Target`` that the rollout is deployed to.
    """

    message = proto.Field(
        proto.STRING,
        number=1,
    )
    pipeline_uid = proto.Field(
        proto.STRING,
        number=2,
    )
    release_uid = proto.Field(
        proto.STRING,
        number=3,
    )
    rollout = proto.Field(
        proto.STRING,
        number=4,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=5,
        enum=log_enums.Type,
    )
    target_id = proto.Field(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
