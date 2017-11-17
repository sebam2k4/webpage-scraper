## Webpage Scraper

This small python app scrapes webpages from a list of urls in a csv file for their titles and descriptions and stores the values, including the url, in a MondoDB database.

The app can easily be modified to scrape other parts of a webpage

### Tech Used:
* Python
* Beautiful Soup 4
* Lxml parser
* MongoDB

### how to run it on your local machine:
1. set up your virtualenv, activate it, and install all requirements from requirements.txt
2. edit settings.py to change db, collection, csv names and db connection settings. (or use the defaults)
3. make sure you have mongoDB (mongod) running locally. run `python scrape_and_scrape_db.py` command in your terminal
4. look at your MongoDB collection full od documents with all that scraped data and enjoy!