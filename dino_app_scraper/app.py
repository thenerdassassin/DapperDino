import math

from dino_app_scraper.common.browser import getBrowserInstance
from dino_app_scraper.common.csv_utilities import generateFileNames, mergeCsvFiles
from dino_app_scraper.common.thread_executor import getExecutor
from dino_app_scraper.dino_website.stat_page import writeStatsToFile, getDinoStatNames

NUM_THREADS = 10
MAX_DINO = 9973
STEP = math.ceil(MAX_DINO/NUM_THREADS)
dinoStartIndices = range(1, MAX_DINO+1, STEP)

class DinoAppScraper:
    @staticmethod
    def run():
        print("Scraping Gen 0 Dino Stats.")
        # Create Browser Instance for each thread
        browserList = map(lambda x: getBrowserInstance(), dinoStartIndices)
        # Create File for each thread
        tempFiles = generateFileNames(dinoStartIndices)
        stepList = [STEP] * len(dinoStartIndices)
        # Get stats for each dino in parallel and write to temporary files
        with getExecutor(NUM_THREADS) as executor:
            executor.map(writeStatsToFile, browserList, dinoStartIndices, tempFiles, stepList)
        # Merge temporary files to final csv
        mergeCsvFiles(tempFiles, getDinoStatNames(), True)



