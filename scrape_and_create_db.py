import csv
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pymongo
import sys
from settings import MONGODB_HOST, MONGODB_PORT, DBS_NAME, COLLECTION_NAME, CSV_FILE_NAME

'''
Creates a MongoDb database with collection name
scrape for data, connecto to MongoDB, create db, create collection, and
insert to collection.
'''

# open csv file and return the row in a list
def readCsvFile(filename):
    try:
        with open(filename) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                return row
    #handle error when no file found
    except IOError as error:
        print 'Error reading file: %s' % error
        print 'Check if file present and filename matches: %s' %CSV_FILE_NAME
        print 'exiting program...'
        sys.exit()

#Connect to MongoDB
def mongo_connect():
    try:
        conn = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
        print "Mongo is connected!"
        return conn
    except pymongo.errors.ConnectionFailure as error:
        print "Could not connect to MongoDB: %s" % error

# Parse html of webpage and find title and description and store in a dictionary
def scrape_data(urls):
    data_array = []
    for url in urls:
        html_text = urlopen(url).read() # how to narrow the read down to only <head> tag? (make more efficient?)
        soup = BeautifulSoup(html_text, "lxml")
        # scrape title and description from each url
        site_title = soup.title.string
        site_description = soup.html.head.find("meta", attrs={"name":"description"})
        # need to create new dicionary for each new item/iteration to be able to append to list later
        data = {
            'url': url,
            'description': site_description['content'] if site_description else "No description given",
            'title': site_title if site_title else "No title given"
        }
        # append screped data to a list
        data_array.append(data)
    return data_array


print "This program will scrape title and description of each url included in the csv file,"
print "and write the results to a MongoDB database. (make sure you're connected to MongoDB)"
print "\nWARNING: This will create a database named: '%s', and a collection named: '%s'" % (DBS_NAME, COLLECTION_NAME)
print "WARNING: The collection will be overwritten if one already exists within the same db"
print "NOTE: edit settings.py to change db and collection names as well as connection settings\n"

user_input = raw_input("Press Enter to proceed... (or type 'quit' or 'exit' to cancel): ")

# check user wants to proceed before doing any work
if user_input == 'quit' or user_input == 'exit':
    print 'exiting program...'
    sys.exit()
else:
    # get a list of url from a csv file
    my_urls = readCsvFile(CSV_FILE_NAME)
    scraped_data = scrape_data(my_urls)
    # Insert data to MongoDB
    conn = mongo_connect() #connect to MongoDB
    try:  
        db = conn[DBS_NAME] # db name
        coll = db[COLLECTION_NAME] # db collectinon name
        coll.drop()  # remove the collection to avoid duplicates when testing
        coll.insert(scraped_data) # insert scraped data to db
        print "Added documents to MongoDB successfully!"
    except:
        print "Unable to add record to database due to unrecognized error."
