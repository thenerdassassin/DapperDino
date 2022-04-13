# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Implement an AWS Lambda function that handles input from direct
invocation.
"""

import logging
import pandas
from aws_handlers import readFileFromS3, readStringFromS3
from dapper_dino import DapperDino

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET = 'dapper-dinos-csv-files'
DINO_STATS_KEY = 'dino_stats_final.csv'
KARMA_TO_DINO_KEY = 'dapper_karma_to_dino.csv'

def getOriginalDinoNumber(karmaNumber):
    karmaToDinoCsv = readStringFromS3(BUCKET, KARMA_TO_DINO_KEY)
    for csvLine in karmaToDinoCsv.splitlines():
        if f'{karmaNumber},' in csvLine:
            return int(csvLine.split(",")[-1])

def getDinoStats():
    dinoStatCsv = readFileFromS3(BUCKET, DINO_STATS_KEY)
    return pandas.read_csv(dinoStatCsv, index_col=0)

# For example code see: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/lambda/lambda_handler_basic.py
def lambda_handler(event, context):
    print(event)
    dino = event.get('pathParameters').get('dinoNumber')

    isKarma = None
    queryParams = event.get('queryStringParameters')
    if queryParams is not None:
        isKarmaString = queryParams.get('isKarma')
        trueValues = ['true', '1', 't', 'y', 'yes']
        isKarma = isKarmaString.lower() in trueValues
    else:
        isKarma = False

    originalDinoNumber = int(dino)
    if isKarma:
        originalDinoNumber = getOriginalDinoNumber(dino)
    
    dapperDino = DapperDino(dino, isKarma, originalDinoNumber)
    dinoStats = getDinoStats()
    dapperDino.setStats(
        int(dinoStats.loc[originalDinoNumber].at['Acceleration']),
        int(dinoStats.loc[originalDinoNumber].at['Agility']),
        int(dinoStats.loc[originalDinoNumber].at['Attack']),
        int(dinoStats.loc[originalDinoNumber].at['Defense']),
        int(dinoStats.loc[originalDinoNumber].at['Health']),
        int(dinoStats.loc[originalDinoNumber].at['Speed']),
    )
    
    return dapperDino.toJson()