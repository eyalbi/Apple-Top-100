import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from models.AppleApp import AppleApp
import configparser
from queue import Queue
from multiprocessing.pool import ThreadPool


class ScrapeAppleApps(object):
    """
    scraper class responsible for scraping top 100 apple apps of 2022
    """
    def __init__(self, config=None):
        """
        initialize scrape with :
        0.pool - ThreadPool to increase Request Rate and data gathering
        1.config object - holds the keys of the JS Selectors to the app data.
        also user agents to replace in every request
        2.Selectors - js selectors for bs4(beautiful soup)
        3.userAgents - user agent values
        4.Top100FreeApps - list containing top 100 Free Apple Apps of 2022 (app_name,app_id) saved in memory for
        runtime performance improvement)
        5.userAgentQueue - a queue to manage the user agents.
        in each request to apple an user agent is pull out of the queue and added to the request headers
         and in advance get added again to the end of the queue.

        :param config: dependecy injection of config file object to create loose coupling
        """
        self.pool = ThreadPool(10)
        if config:
            configObject = config
        else:
            configObject = configparser.ConfigParser()
            configObject.read('config.ini')
        self.selectors = configObject['Selectors']
        self.userAgents = configObject['UserAgent']
        self.Top100FreeApps = [("Temu: Team Up, Price Down", 1641486558),
                               ("TikTok", 835599320),
                               ("Google", 284815942),
                               ("CapCut - Video Editor", 1500855883),
                               ("Instagram", 389801252),
                               ("YouTube: Watch, Listen, Stream", 544007664),
                               ("Gmail - Email by Google", 422689480),
                               ("WhatsApp Messenger", 310633997),
                               ("Facebook", 284882215),
                               ("Snapchat", 447188370),
                               ("Nextdoor: Neighborhood Network", 640360962),
                               ("Google Chrome", 535886823),
                               ("Microsoft Edge: Web Browser", 1288723196),
                               ("Telegram Messenger", 686449807),
                               ("Microsoft Teams", 1113153706),
                               ("Planet Fitness Workouts", 399857015),
                               ("Messenger", 454638411),
                               ("Google Maps", 585027354),
                               ("Spotify - Music and Podcasts", 324684580),
                               ("Cash App", 711923939),
                               ("Amazon Shopping", 297606951),
                               ("SHEIN - Online Fashion", 878577184),
                               ("Zoom - One Platform to Connect", 546505307),
                               ("Google Meet", 1096918571),
                               ("Twitter", 333903271),
                               ("Microsoft Outlook", 951937596),
                               ("PayPal - Send, Shop, Manage", 283646709),
                               ("Netflix", 363590051),
                               ("Microsoft Authenticator", 983156458),
                               ("Gardenscapes", 1105855019),
                               ("Tap Away 3D", 1568058543),
                               ("Discord - Chat, Talk & Hangout", 985746746),
                               ("Vrbo Vacation Rentals", 1245772818),
                               ("McDonald's", 922103212),
                               ("Google Drive", 507874739),
                               ("Walmart - Shopping & Grocery", 338137227),
                               ("Photomath", 919087726),
                               ("Chess - Play & Learn", 329218549),
                               ("DoorDash - Food Delivery", 719972451),
                               ("Pinterest", 429047995),
                               ("Royal Match", 1482155847),
                               ("Shop: All your favorite brands", 1223471316),
                               ("Uber - Request a ride", 368677368),
                               ("Google Docs: Sync, Edit, Share", 842842640),
                               ("Peacock TV: Stream TV & Movies", 1508186374),
                               ("Duolingo - Language Lessons", 570060128),
                               ("Reddit", 1064216828),
                               ("Jackpocket Lottery App", 663046683),
                               ("Venmo", 351727428),
                               ("Makeover Studio: Makeup Games", 1627184882),
                               ("Hopper: Flights, Hotels & Cars", 904052407),
                               ("Disney+", 1446075923),
                               ("Nike: Shoes, Apparel, Stories", 1095459556),
                               ("Paramount+", 530168168),
                               ("Impulse - Brain Training", 1451295827),
                               ("Mob Control", 1562817072),
                               ("Fetch: Have Fun, Save Money", 1182474649),
                               ("Parking Jam 3D", 1498229533),
                               ("Life360: Find Family & Friends", 384830320),
                               ("Ticketmaster－Buy, Sell Tickets", 500003565),
                               ("HBO Max: Stream TV & Movies", 971265422),
                               ("Amazon Prime Video", 545519333),
                               ("Google Photos", 962194608),
                               ("Legend of Slime: Idle RPG", 1618701110),
                               ("The Roku App (Official)", 482066631),
                               ("ADP Mobile Solutions", 444553167),
                               ("Survivor!.io", 1528941310),
                               ("Starbucks", 331177714),
                               ("Indeed Job Search", 309735670),
                               ("Top War: Battle Game", 1479198816),
                               ("Zelle", 1260755201),
                               ("Draw Action!", 6444147536),
                               ("Roblox", 431946152),
                               ("Hulu: Stream TV & movies", 376510438),
                               ("Etsy: Custom & Creative Goods", 477128284),
                               ("VPN - Super Unlimited Proxy", 1370293473),
                               ("Capital One Mobile", 407558537),
                               ("LinkedIn: Network & Job Finder", 288429040),
                               ("Google Sheets", 842849113),
                               ("Expedia: Hotels, Flights & Car", 427916203),
                               ("JustFit: Lazy Workout & Fit", 1574460221),
                               ("Uber Eats: Food Delivery", 1058959277),
                               ("Audible: Audio Entertainment", 379693831),
                               ("Breeze: Mental Health", 1450365119),
                               ("Township", 638689075),
                               ("Crowd Evolution!", 1613908087),
                               ("Poshmark: Buy & Sell Fashion", 470412147),
                               ("American Airlines", 382698565),
                               ("Google Translate", 414706506),
                               ("BeReal. Your friends for real.", 1459645446),
                               ("Airbnb", 401626263),
                               ("Call of Duty®: Mobile", 1287282214),
                               ("DoorDash - Dasher", 1451754591),
                               ("Wizz - Make new friends", 1452906710),
                               ("Canva: Design, Photo & Video", 897446215),
                               ("Chase Mobile®: Bank & Invest", 298867247),
                               ("Google Calendar: Get Organized", 909319292),
                               ("Waze Navigation & Live Traffic", 323229106),
                               ("Rocket Money - Bills & Budgets", 1130616675),
                               ("Amazon Alexa", 944011620)]
        self.userAgentsQueue = Queue()
        for userAgent in self.userAgents.values():
            self.userAgentsQueue.put(userAgent)

    def initialize_pool(self):
        """
        method that closes the pool and initialize it again
        :return:
        """
        self.pool.close()
        self.pool.join()
        self.pool = ThreadPool(10)

    @staticmethod
    def extract_app_compatibility(compatibilities):
        """
        a static method that responsble for parsing the compatibilities data of an Appleapp
        :param compatibilities: list of compatibilities to extract
        :return: compatibilities parsed List
        """
        compatibilitiesList = []
        for compatibility in compatibilities:
            compatibilityText = compatibility.text.strip()
            if '\u00a0' in compatibilityText:
                compatibilityText = ' '.join(compatibilityText.split())
            compatibilitiesList.append(compatibilityText)
        return compatibilitiesList

    def get_user_agent(self):
        """
        method to get a user agent for a new request .
        user agent pulled out of the queue and than enter in the back of the queue.
        :return: user agent string
        """
        userAgent = self.userAgentsQueue.get()
        self.userAgentsQueue.put(userAgent)
        return userAgent

    def create_request(self, url):
        """
        prepare the request with custom headers and send it to apple
        :param url: app Apple store url
        :return: Response from Apple
        """
        headers = {'Connection': 'close',
                   'User-Agent': self.get_user_agent(),
                   'authority': 'apps.apple.com',
                   'accept-language': 'en-US,en-IL;q=0.9,en;q=0.8,he-IL;q=0.7,he;q=0.6,it;q=0.5',
                   'cache-control': 'no-cache'
                   }
        return requests.get(url, headers=headers)

    def scrape_apps_data(self, apps_to_scrape=None):
        """
        main scrapper method to scrape apps data.
        if no apps_to_scrape is specified than the scrapper will scrape all the top 100 Apps of 2022.
        if it does specified it will scrape only the requested apps.
        :param apps_to_scrape: tuple of (appName,AppId)
        :return: results of the scraping (apps scraped data), Errors of the scraping(tuple (appName,appId))
        """
        results = []
        errors = []
        if apps_to_scrape:
            self.scrape_apps(apps_to_scrape, results, errors)
        else:
            self.scrape_apps(self.Top100FreeApps, results, errors)
        return results, errors

    def scrape_apps(self, apps, results, errors):
        """
        method to scrape a list of apps:
        initialize the Thread pool with the job to scrape each app.
        :param apps: apps to scrape (appName,appID)
        :param results: results List to save the Scraped Data
        :param errors: error list to save the app name and id of the apps that cant be scraped at the moment
        """
        self.pool.starmap(self.scrape_app, [(app[0], app[1], results, errors) for app in apps])
        self.initialize_pool()
        logging.debug(f'scraped {len(results)} apps - failed to scrape {len(errors)} ')
        logging.info(f'scraped {len(results)} apps retrying to scrape {len(errors)} apps that failed ')
        self.pool.starmap(self.scrape_app, [(app[0], app[1], results, errors) for app in errors])
        self.initialize_pool()
        logging.info(f'finished scraping successfully scraped {len(results)} Apps')

    def scrape_app(self, app_name, app_id, results, errors):
        """
        scrape a specific app method and add it to result or error lists
        :param app_name: app apple store name
        :param app_id: app apple store id
        :param results: results list (app data)
        :param errors: error list (app that can be scraped)
        """
        url = f'https://apps.apple.com/us/app/{app_name}/id{app_id}'
        time.sleep(5)
        response = self.create_request(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            appSeller = soup.select_one(self.selectors['Seller']).text.strip()
            appRating = soup.find('span', {'class': self.selectors['Rating']}).text.strip()
            appCategories = soup.select_one(self.selectors['Categories']).text.strip()
            appSize = soup.select_one(self.selectors['Size']).text.strip()
            appMinAge = soup.select_one(self.selectors['Age']).text.split("+")[0].strip()
            if not appMinAge.isnumeric():
                appMinAge = soup.select_one(self.selectors['Age2']).text.split("+")[0].strip()
            appCompatibility = ScrapeAppleApps.extract_app_compatibility(soup.select_one(
                self.selectors['CompatibilitiesList']).select(self.selectors['Compatibility']))
            appleApp = AppleApp({'url': url, 'appName': app_name, 'appId': app_id, 'appSeller': appSeller,
                                 'appRating': appRating, 'appCategories': appCategories,
                                 'appSize': appSize, 'appMinAge': appMinAge,
                                 'appCompatibility': appCompatibility})
            AppJsonStr = json.dumps(appleApp.__dict__)
            logging.info(f'scraped - {app_name} : {AppleApp}')
            results.append((app_name, AppJsonStr))
        else:
            logging.warning(f'error scraping {app_name} -> response code {response.status_code}')
            errors.append((app_name, app_id))

    def get_app_id_by_name(self, app_name):
        """
        get apple id from the top 100 lists with given app name
        :param app_name: apple app name to get id for
        :return: app id if found or none if not
        """
        for app in self.Top100FreeApps:
            if app[0] == app_name:
                return app[1]
        return None
