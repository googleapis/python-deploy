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
# Generated code. DO NOT EDIT!
#
# Snippet for UpdateDeliveryPipeline
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-deploy


# [START clouddeploy_v1_generated_CloudDeploy_UpdateDeliveryPipeline_sync]
from google.cloud import deploy_v1


def sample_update_delivery_pipeline():
    # Create a client
    client = deploy_v1.CloudDeployClient()

    # Initialize request argument(s)
    request = deploy_v1.UpdateDeliveryPipelineRequest(
    )

    # Make the request
    operation = client.update_delivery_pipeline(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END clouddeploy_v1_generated_CloudDeploy_UpdateDeliveryPipeline_sync]
