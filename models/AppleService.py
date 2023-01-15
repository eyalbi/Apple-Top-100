import asyncio

from models.ScrapeAppleApps import ScrapeAppleApps
from models.db import redisHandler
from multiprocessing import Process
import logging


class AppleService(object):
    """
    Apple service class responsible for the whole components of the service
    """
    def __init__(self):
        """
        1.dbHandler initialize db object (next version create loose coupling)
        2.scraper initialize scraper instance
        when initialized the service scrape the top 100 free apps and saves them in the redis db
        """
        self.dbHandler = redisHandler()
        self.scraper = ScrapeAppleApps()
        scrapingResults, self.scrapingErrors = self.scraper.scrape_apps_data()
        self.dbHandler.set_top_100_apps(scrapingResults)

    async def scrape_delta(self):
        """
        a method to scrape the apps from the top 100 free apps that currently not in the db
        :return:
        """
        deltaToScrape = []
        dbData = self.dbHandler.get_current_keys()
        for app_name, app_id in self.scraper.Top100FreeApps:
            if app_name not in dbData:
                deltaToScrape.append((app_name, app_id))
        scrapingResults, scrapingErrors = self.scraper.scrape_apps_data(deltaToScrape)
        self.dbHandler.set_top_100_apps(scrapingResults)

    def get_top_100_apps(self):
        """
        a method to get top 100 apps data .
        first check in the db for the results.
        if it less than 100 then create a task to gather the remaining apps data and in meanwhile send back the response
        :return: top 100 free apple apps data sorted by rating
        """
        top100Data = self.dbHandler.get_top_100_apps()
        if len(top100Data) < 100:
            top100Data.insert(0, {"message": " not all apps data was acquired try again later for the full list "})
            task = asyncio.create_task(self.scrape_delta())
            task = asyncio.shield(task)
        top100Data.sort(key=lambda x: x['rating'], reverse=True)
        return top100Data

    def get_app(self, app_name):
        """
        return specific app data.
        check db if exists return else scrape the app saves it to the db and returning the answer.
        :param app_name: app to return data for
        :return: app data or '{"message": "error Fetching Data"}' if appName doesnt exists
        """
        result = self.dbHandler.get_app_data(app_name)
        if result:
            return result
        else:
            result = []
            error = []
            app_id = self.scraper.get_app_id_by_name(app_name)
            self.scraper.scrape_app(app_name, app_id, result, error)
            self.dbHandler.set_app_data(app_name, result[0])
            if result:
                return result[0]
            else:
                return {"message": "error Fetching Data"}





