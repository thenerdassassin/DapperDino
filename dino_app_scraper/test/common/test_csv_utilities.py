import unittest
from dino_app_scraper.common.csv_utilities import generateFileName, generateFileNames

class TestCsvUtilities(unittest.TestCase):
    def test_generateFileName(self):
        expectedValue = "dino_stats_1.csv"
        actualValue = generateFileName(1)
        self.assertEqual(expectedValue, actualValue)
    def test_generateFileNames(self):
        expectedValue = ["dino_stats_1.csv", "dino_stats_2.csv", "dino_stats_3.csv"]
        actualValue = generateFileNames([1,2,3])
        self.assertEqual(expectedValue, actualValue)