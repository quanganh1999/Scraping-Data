# Main function
import requests
from bs4 import BeautifulSoup
import re
import get_data
import database


# Initilize:
def init_db():
    print('Start to create DB')
    database.make_connect()
    database.create_tables()    

# Scraping Data
# limit_record is max number of inserted records based on buffer size
def scraping(temUrl='https://vnexpress.net/giao-duc-p', limit_record=1):
    dataSource = []  # Saving data
    id = 1
    firstPage = ''  # URL of first page
    while id > 0:
        print(id)  # for debugging
        url = temUrl + str(id)  # actual URL
        res = requests.get(url)

        # Check the limit of page
        if res.url == firstPage:
            break

        # Get the url of first page
        if id == 1:
            firstPage = res.url

        # Get data from all news in this page
        setUrls = get_data.get_urls_vnexpress(res)
        for link in setUrls:
            try:
                data = get_data.get_vnexpress(link)                        
            except Exception as err:
                print("Missing data at " + link)
                print("Type Error: " + str(err.args))
            finally:
                dataSource.append(data)
        # Check limit records to insert:    
        if(len(dataSource) >= limit_record):
            database.insert_multi_rec(dataSource)
            dataSource.clear()
        id += 1

    # Check again if it still has datas
    if len(dataSource) != 0:
        database.insert_multi_rec(dataSource)
    
    # Close DB:
    database.close_db()

if(__name__ =='__main__'):
    init_db()
    scraping()