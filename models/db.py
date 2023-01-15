from redis import Redis, ConnectionPool
import json

class redisHandler(object):

    """
    redis db HAndler class in charge of communicate with the in memory redis DB.
    """
    def __init__(self, host='localhost', port=6379, db=0, max_connections=10):
        """

        :param host: redis db host domain - Default: localhost
        :param port: redis db port - Default: 6379 redis Default
        :param db: redis db index - Default: 0 redis Default
        :param max_connections: number of max open connection possible at a time.
        """
        self.pool = ConnectionPool(host=host, port=port, db=db, max_connections=max_connections)
        self.r = Redis(connection_pool=self.pool)

    def get_top_100_apps(self):
        """
        get top 100 Apple Apps of 2022 Data
        :return:
        all the values currently stored in the DB
        """
        top100Data = []
        keys = self.r.keys()
        for key in keys:
            value = json.loads(self.r.get(key))
            top100Data.append(value)
        return top100Data

    def set_top_100_apps(self, results):
        """
        a method that save all scraping results to the redis db with appName as key and appData Json dictionary as value
        :param results: scraping results to save in the Db
        """
        for result in results:
            self.set_app_data(result[0], result[1])

    def get_app_data(self, app_name):
        """
        method to get specific app from the db
        :param app_name: app to retrieve
        :return: app data if exists or none if not .
        """
        value = self.r.get(app_name)
        if value:
            return json.loads(value)
        return value

    def set_app_data(self, app_name, app_data):
        """
        a method to set one app in the db
        :param app_name: app unique name
        :param app_data: app Json dict Data
        :return:
        """
        self.r.set(app_name, app_data, ex=3600)

    def get_current_keys(self):
        """
            a method to retrieve all the current available apps name in the db
        :return: db.keys
        """
        return [key.decode('UTF-8') for key in self.r.keys()]

