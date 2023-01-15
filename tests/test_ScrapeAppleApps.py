import configparser
import unittest
import sys
import configparser

import requests

sys.path.append('..')
print(sys.path)

from models.ScrapeAppleApps import ScrapeAppleApps

"""
Test AppleApp is class to test the initialization of an AppleApp module .
"""


class TestScrapeAppleApps(unittest.TestCase):
    """
    this class is a test class for the scraping service
    """
    configObject = configparser.ConfigParser()
    configObject.read("C:\\Users\\eyalb\\PycharmProjects\\Peer39task\\config.ini")

    Scraper = ScrapeAppleApps(config=configObject)

    def test_create_request(self):
        """
            test the creation of the request filled with custom correct headers.
        """
        response = self.Scraper.create_request(url='https://apps.apple.com/us/app/Facebook/id284882215')
        self.assertDictContainsSubset({'Connection': 'close',
                                       'authority': 'apps.apple.com',
                                       'accept-language': 'en-US,en-IL;q=0.9,en;q=0.8,'
                                                          'he-IL;q=0.7,he;q=0.6,it;q=0.5',
                                       'cache-control': 'no-cache'
                                       }, response.request.headers)
