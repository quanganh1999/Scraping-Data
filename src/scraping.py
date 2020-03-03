# Main function
import requests
from bs4 import BeautifulSoup
import re
import GetData
import DataBase


# Initilize:
#DB:
print('Start to create DB')
DataBase.make_connect()
DataBase.createEduNewTab()
limit_record = 100 #Max number of inserted records 

#Scraping Data
temUrl = 'https://vnexpress.net/giao-duc-p'  # template url
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
    setUrls = GetData.getUrlsVnExpress(res)
    for link in setUrls:
        try:
            data = GetData.vnexpress(link)
        except Exception as err:
            print("Missing data at " + link)
            print("Type Error: " + str(err.args))
        finally:
            dataSource.append(data)
    #Check limit records to insert:
    if(len(dataSource) >= limit_record):
        DataBase.insertMultiRecords(dataSource)
        dataSource.clear()
    id += 1

#Check again if it still has datas
if len(dataSource) != 0:
    DataBase.insertMultiRecords(dataSource)

# Close DB:
DataBase.closeDB()