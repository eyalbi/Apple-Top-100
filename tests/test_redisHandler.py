import json
import unittest
import sys
sys.path.append('..')
from models.db import redisHandler

class TestRedisHandler(unittest.TestCase):
    redisHandler = redisHandler(db=1)

    def test_get_app(self):
        self.redisHandler.set_app_data('Facebook',
                                       json.dumps({'name': 'Facebook', 'id': 284882215,
                                                   'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                                   'seller': 'Meta Platforms, Inc.', 'rating': '2.3',
                                                   'categories': 'Social Networking',
                                                   'size': '314.6 MB', 'age': '12',
                                                   'compatibility': ['iPhone', 'iPad', 'iPod touch', 'Apple TV'],
                                                   'kidFriendly': False, 'type': 'tv app'}))
        self.assertEqual(self.redisHandler.get_app_data('Facebook')["id"], 284882215)
        self.assertEqual(self.redisHandler.get_app_data('peer39'), None)
    def test_set_app_data(self):
        self.redisHandler.r.delete('Facebook')
        self.redisHandler.set_app_data('Facebook',
                                       json.dumps({'name': 'Facebook', 'id': 284882215,
                                                   'url': 'https://apps.apple.com/us/app/Facebook/id284882215',
                                                   'seller': 'Meta Platforms, Inc.', 'rating': '2.3',
                                                   'categories': 'Social Networking',
                                                   'size': '314.6 MB', 'age': '12',
                                                   'compatibility': ['iPhone', 'iPad', 'iPod touch', 'Apple TV'],
                                                   'kidFriendly': False, 'type': 'tv app'}))
        self.assertTrue(self.redisHandler.get_app_data('Facebook'))


