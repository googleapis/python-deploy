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

__protobuf__ = proto.module(
    package="google.cloud.deploy.v1",
    manifest={
        "ReleaseRenderEvent",
    },
)


class ReleaseRenderEvent(proto.Message):
    r"""Payload proto for "clouddeploy.googleapis.com/release_render"
    Platform Log event that describes the render status change.

    Attributes:
        message (str):
            Debug message for when a render transition
            occurs. Provides further details as rendering
            progresses through render states.
        release (str):
            The name of the ``Release``.
    """

    message = proto.Field(
        proto.STRING,
        number=1,
    )
    release = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
