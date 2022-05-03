# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Implement an AWS Lambda function that handles input from direct
invocation.
"""

import json
import logging
import pandas
from aws_handlers import readFileFromS3, readStringFromS3
from dapper_dino import DapperDino

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET = 'dapper-dinos-csv-files'
DINO_STATS_KEY = 'dino_stats_final.csv'
KARMA_TO_DINO_KEY = 'dapper_karma_to_dino.csv'
DINO_TRAITS_KEY = 'dapper_dino_traits.csv'
TRAIT_TO_STAT_KEY = 'traitToStatMap.csv'
MAX_VALUE_COLUMN = 'MaxCap'

# TODO: Refactor to use pandas
def getOriginalDinoNumber(karmaNumber):
    karmaToDinoCsv = readStringFromS3(BUCKET, KARMA_TO_DINO_KEY)
    for csvLine in karmaToDinoCsv.splitlines():
        if f'{karmaNumber},' in csvLine:
            return int(csvLine.split(",")[-1])

def getAndSetStats(dapperDino):
    dinoStats = getDinoStats()
    originalDinoNumber = int(dapperDino.originalDinoNumber)

    # TODO: Refactor...This is ugly.
    dapperDino.setStats(
        int(dinoStats.loc[originalDinoNumber].at['Acceleration']),
        int(dinoStats.loc[originalDinoNumber].at['Agility']),
        int(dinoStats.loc[originalDinoNumber].at['Attack']),
        int(dinoStats.loc[originalDinoNumber].at['Defense']),
        int(dinoStats.loc[originalDinoNumber].at['Health']),
        int(dinoStats.loc[originalDinoNumber].at['Speed']),
    )

def getDinoStats():
    dinoStatCsv = readFileFromS3(BUCKET, DINO_STATS_KEY)
    return pandas.read_csv(dinoStatCsv, index_col=0)

def getAndSetTraits(dapperDino):
    dinoTraits = getDinoTraits()
    originalDinoNumber = int(dapperDino.originalDinoNumber)

    # TODO: Refactor...This is ugly.
    dapperDino.setTraits(
        image = str(dinoTraits.loc[originalDinoNumber].at['Image']),
        background = str(dinoTraits.loc[originalDinoNumber].at['Background']),
        body = str(dinoTraits.loc[originalDinoNumber].at['Body']),
        face = str(dinoTraits.loc[originalDinoNumber].at['Face']),
        headwear = str(dinoTraits.loc[originalDinoNumber].at['Headwear']),
        eyes = str(dinoTraits.loc[originalDinoNumber].at['Eyes']),
        clothes = str(dinoTraits.loc[originalDinoNumber].at['Clothes']),
        accessory = str(dinoTraits.loc[originalDinoNumber].at['Accessory']),
    )

# TODO: Repetitive code...refactor.
def getDinoTraits():
    dinoTraitsCsv = readFileFromS3(BUCKET, DINO_TRAITS_KEY)
    return pandas.read_csv(dinoTraitsCsv, index_col=0)

def getMaxStatFromMap(traitToStatMap, traitValue, trait):
    if (traitValue == "<none>"):
        traitValue = f'NONE_{trait}'
    if (trait == "background"):
        if (traitValue.find("Rich Tu") != -1):
            traitValue = "Rich Tu"
        elif (traitValue.find("Hatch")):
            traitValue = "Hatch"
        elif (traitValue.find("Bakeroner Yellow")):
            traitValue = "Bakeroner Yellow"
        elif (traitValue.find("Bakeroner Green")):
            traitValue = "Bakeroner Green"
    traitValue = traitValue.upper()
    print(f'Getting trait: {traitValue}')
    return int(traitToStatMap.loc[traitValue].at[MAX_VALUE_COLUMN])

def getAndSetMaxStats(dapperDino):
    traitToStatCsv = readFileFromS3(BUCKET, TRAIT_TO_STAT_KEY)
    traitToStatMap = pandas.read_csv(traitToStatCsv, index_col=0)

    dapperDino.setMaxStats(
        maxAcceleration = getMaxStatFromMap(traitToStatMap, dapperDino.traits.eyes, "eyes"),
        maxAgility = getMaxStatFromMap(traitToStatMap, dapperDino.traits.face, "face"),
        maxAttack = getMaxStatFromMap(traitToStatMap, dapperDino.traits.clothes, "clothes"),
        maxDefense = getMaxStatFromMap(traitToStatMap, dapperDino.traits.headwear, "headwear"),
        maxHealth = getMaxStatFromMap(traitToStatMap, dapperDino.traits.background, "background"),
        maxSpeed = getMaxStatFromMap(traitToStatMap, dapperDino.traits.body, "body"),
        bonusPoints = getMaxStatFromMap(traitToStatMap, dapperDino.traits.accessory, "accessory")
    )

# For example code see: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/lambda/lambda_handler_basic.py
def lambda_handler(event, context):
    print(event)
    dino = event.get('pathParameters').get('dinoNumber')

    isKarma = False
    queryParams = event.get('queryStringParameters')
    if queryParams is not None and queryParams.get('isKarma') is not None:
        isKarmaString = queryParams.get('isKarma')
        trueValues = ['true', '1', 't', 'y', 'yes']
        isKarma = isKarmaString.lower() in trueValues

    originalDinoNumber = int(dino)
    if isKarma:
        originalDinoNumber = getOriginalDinoNumber(dino)
    
    print(f'Getting stats. Dino: {dino}, isKarma:{isKarma}, ogDinoNum: {originalDinoNumber}')
    
    dapperDino = DapperDino(dino, isKarma, originalDinoNumber)

    getAndSetStats(dapperDino)
    getAndSetTraits(dapperDino)
    getAndSetMaxStats(dapperDino)
    
    results = dapperDino.toJson()
    print(results)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps(results)
    }