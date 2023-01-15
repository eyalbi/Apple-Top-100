class AppleApp(object):
    """
    Apple app module with all the args that correspond to the data that is to be scraped:
    1.name -App AppStore name
    2.id - App AppStore id
    3.url - App AppStore url
    4.seller - App seller
    5.rating - App Appstore Rating
    6.categories App categories in the Appstore
    7.size - App download size
    8.age - Min age to use the App
    9.compatibility - Apple devices That operate the App

    Special args:
    1.kidFriendly - true if under 11 else False
    2.type - tv app, music, game, other
    """
    def __init__(self, appData):
        self.name = appData['appName']
        self.id = appData['appId']
        self.url = appData['url']
        self.seller = appData['appSeller']
        self.rating = appData['appRating']
        self.categories = appData['appCategories']
        self.size = appData['appSize']
        self.age = appData['appMinAge']
        self.compatibility = appData['appCompatibility']
        try:
            self.kidFriendly = True if int(self.age) <= 11 else False
        except Exception as e:
            print(self.name)
        if "Apple TV" in self.compatibility:
            self.type = "tv app"
        elif self.categories == "Games":
            self.type = "Game"
        elif self.categories == "Music":
            self.type = "Music"
        else:
            self.type = "Other"
