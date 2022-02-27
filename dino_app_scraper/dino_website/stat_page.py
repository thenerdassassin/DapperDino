from time import sleep
from dino_app_scraper.common.browser import getWebpage
from dino_app_scraper.common.csv_utilities import writeDinoFile
BASE_URL = 'https://app.dapperdinos.com/dino'

#TODO: Add Tests
def writeStatsToFile(browser, dinoStartIndex, fileName, step):
    statRows = []
    for i in range(dinoStartIndex, dinoStartIndex+step):
        statRows.append(getStatsForDino(browser, i))
    writeDinoFile(fileName, statRows)

#TODO: Add Tests
def getStatsForDino(browser, dinoNumber, isKarma=False, attempt = 0):
    print(f'Getting stats for Dino {dinoNumber}')
    try:
        dinoPage = getDinoStatWebpage(browser, dinoNumber, isKarma)
        return [dinoNumber] + getStatsFromPage(dinoPage)
    except ValueError as e:
        if attempt < 3:
            print(f'Failed to get Dino {dinoNumber}. Will retry.')
            return getStatsForDino(browser, dinoNumber, isKarma, attempt + 1)
        else:
            print(f'Failed to get Dino ${dinoNumber} and can not retry.')
            return [dinoNumber]

def getDinoStatNames():
    return ['Dino Number', 'Defense', 'Speed', 'Health', 'Attack', 'Acceleration', 'Agility']
    
def getDinoStatWebpage(browser, dinoNumber, isKarma):
    dinoStatPageUrl = getDinoStatWebPageUrl(BASE_URL, dinoNumber, isKarma)
    return getWebpage(browser, dinoStatPageUrl, 'bfoT1')

def getStatsFromPage(webpage):
    stats = findAllForClass(webpage, 'bfoT1')
    if len(stats) == 6:
        return list(map(lambda idx: getNumeratorFromDivElement(stats[idx]), range(0,6)))
    else:
        raise ValueError('The stats page did not have six values.')

def getNumeratorFromDivElement(divElement):
    statDiv = parseStatDivForSpanElement(divElement)
    return retrieveNumeratorFromSpan(statDiv)

def findAllForClass(webpage, className):
    return webpage.findAll('div', { "class" : className})

def parseStatDivForSpanElement(statClass):
    return statClass.contents[1] 

def retrieveNumeratorFromSpan(spanElement):
    return str(spanElement.contents)[2:4]

def retrieveDenominatorFromSpan(spanElement):
    return str(spanElement.contents)[7:10]
    
def getDinoStatWebPageUrl(baseUrl, dinoNumber, isKarma):
    if isKarma == True:
        return baseUrl + '/karma-' + str(dinoNumber)
    else:
        return baseUrl + '/dapper-' + str(dinoNumber)
    