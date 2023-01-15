Apple top 100 free apps of 2022 scraper Project:
this project create a fast Api and an Apple Service module to scrape the top 100 free Apple apps of 2022.

modules:

1.AppleApp - module that define the data that is to be scraped
2.redisHandler - module to manage redis db service functionality
3.ScrapeAppleApps - module to scrape the top 100 free Apple apps
4.AppleService - module to manage all the service Functionality from db to scraping.

this project using async threading functionalities and custom Http requests handaling 
to improve scraping time and results.

this project also includes DockerFile.


stack:python

dependecies: requirements.txt

db: redis db
