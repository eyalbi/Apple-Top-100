import json
import unittest
import sys

sys.path.append('..')
from models.AppleApp import AppleApp

"""
Test AppleApp is class to test the initialization of an AppleApp module .
"""


class TestAppleApp(unittest.TestCase):

    def test_init(self):
        """
        test_init method initialize AppleApp object with data to check the init method of the object.
        1.check KidFriendly - if data['age'] is <= 11 it should be true, otherwise False
        2.check  type - in accordance to the logic if the app is a tv app i should be mark as tv
        (no matter if it music or a game) and if it not tv app i should be marked as Music,Game or Other
        """
        self.appleApp = AppleApp({'appName': 'Facebook', 'appId': 284882215,
                                  'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                  'appSeller': 'Meta Platforms, Inc.', 'appRating': '2.3',
                                  'appCategories': 'Social Networking',
                                  'appSize': '314.6 MB', 'appMinAge': '12',
                                  'appCompatibility': ['iPhone', 'iPad', 'iPod touch', 'Apple TV']})
        self.assertEqual(self.appleApp.kidFriendly, False)
        self.assertEqual(self.appleApp.type, 'tv app')

        self.appleApp = AppleApp({'appName': 'Facebook', 'appId': 284882215,
                                  'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                  'appSeller': 'Meta Platforms, Inc.', 'appRating': '2.3',
                                  'appCategories': 'Games',
                                  'appSize': '314.6 MB', 'appMinAge': '7',
                                  'appCompatibility': ['iPhone', 'iPad', 'iPod touch']})
        self.assertEqual(self.appleApp.kidFriendly, True)
        self.assertEqual(self.appleApp.type, 'Game')

        self.appleApp = AppleApp({'appName': 'Facebook', 'appId': 284882215,
                                  'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                  'appSeller': 'Meta Platforms, Inc.', 'appRating': '2.3',
                                  'appCategories': 'Music',
                                  'appSize': '314.6 MB', 'appMinAge': '12',
                                  'appCompatibility': ['iPhone', 'iPad', 'iPod touch', 'Apple TV']})
        self.assertEqual(self.appleApp.type, 'tv app')

        self.appleApp = AppleApp({'appName': 'Facebook', 'appId': 284882215,
                                  'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                  'appSeller': 'Meta Platforms, Inc.', 'appRating': '2.3',
                                  'appCategories': 'Peer39',
                                  'appSize': '314.6 MB', 'appMinAge': '12',
                                  'appCompatibility': ['iPhone', 'iPad', 'iPod touch']})
        self.assertEqual(self.appleApp.type, 'Other')

