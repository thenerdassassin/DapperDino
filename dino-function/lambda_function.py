# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Implement an AWS Lambda function that handles input from direct
invocation.
"""

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# For example code see: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/lambda/lambda_handler_basic.py
def lambda_handler(event, context):
    print(event)
    dino = event.get('pathParameters').get('dinoNumber')
    return dino