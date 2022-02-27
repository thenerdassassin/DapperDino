import unittest
from bs4 import BeautifulSoup  
from mock import patch, DEFAULT
from dino_app_scraper.dino_website.stat_page import getDinoStatWebPageUrl, getDinoStatWebpage, findAllForClass, parseStatDivForSpanElement, retrieveDenominatorFromSpan, retrieveNumeratorFromSpan


# String retrieved from https://app.dapperdinos.com/dino/dapper-1
webpageString = '<div class="wYp2H"><div class="bfoT1"><img src="/img/joseDesign/icons/shield.png"><span>70 / 100</span></div><div class="bfoT1"><img src="/img/joseDesign/icons/barbell.png"><span>48 / 100</span></div><div class="bfoT1"><img src="/img/joseDesign/icons/heart.png"><span>59 / 100</span></div><div class="bfoT1"><img src="/img/joseDesign/icons/sword.png"><span>65 / 100</span></div><div class="bfoT1"><img src="/img/joseDesign/icons/lightening.png"><span>46 / 100</span></div><div class="bfoT1"><img src="/img/joseDesign/icons/brain.png"><span>65 / 100</span></div></div>'      
webpage = BeautifulSoup(webpageString, 'lxml')

class TestStatPage(unittest.TestCase):
    def test_NonKarma(self):
        baseUrl = "http://www.dinotest.com"
        isKarma = False
        dinoNumber = 4
        expectedValue = "http://www.dinotest.com/dapper-4"
        self.assertEqual(getDinoStatWebPageUrl(baseUrl, dinoNumber, isKarma), expectedValue)

    @patch('dino_app_scraper.dino_website.stat_page.getWebpage')
    def test_get_webpage(self, mock_get_webpage):
        expectedValue = '<div><span>65 / 100</span></div>'
        mock_get_webpage.return_value = expectedValue
        
        dinoPageOne = getDinoStatWebpage(None, 1, False)
        self.assertEqual(dinoPageOne, expectedValue)
        mock_get_webpage.assert_called_once_with(None, 'https://app.dapperdinos.com/dino/dapper-1')

    def test_find_all_class(self):
        actualResults = findAllForClass(webpage, "bfoT1")
        self.assertEqual(len(actualResults), 6)
    
    def test_find_single_class(self):
        actualResults = findAllForClass(webpage, "wYp2H")
        self.assertEqual(len(actualResults), 1)
    
    def test_find_all_unexisting_class(self):
        actualResults = findAllForClass(webpage, "fake_value")
        self.assertEqual(len(actualResults), 0)
    
    def test_get_span_from_element(self):
        divElement = BeautifulSoup(
            '<div class="bfoT1"><img src="/img/joseDesign/icons/shield.png"/><span>70 / 100</span></div>', 'html.parser'
        ).find('div')
        actualResults = parseStatDivForSpanElement(divElement)
        self.assertEqual(str(actualResults), "<span>70 / 100</span>")
    
    def test_get_numerator(self):
        spanElement = BeautifulSoup('<span>70 / 100</span>', 'html.parser').find('span')
        actualResults = retrieveNumeratorFromSpan(spanElement)
        self.assertEqual(actualResults, '70')
    
    def test_get_denominator(self):
        spanElement = BeautifulSoup('<span>70 / 100</span>', 'html.parser').find('span')
        actualResults = retrieveDenominatorFromSpan(spanElement)
        self.assertEqual(actualResults, '100')

        
if __name__ == '__main__':
    unittest.main()