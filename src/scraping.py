# Main function
import requests
from bs4 import BeautifulSoup
import re
import GetData
import DataBase


temUrl = 'https://vnexpress.net/giao-duc-p' #template url
dataSource = [] #Saving data
id = 1
firstPage = '' #URL of first page
ses = requests.Session() # create session
while id > 0:
    print(id)# for debugging
    url = temUrl + str(id) #actual URL
    res = ses.get(url)
    
    #Check the limit of page
    if(res.url == firstPage):
        break

    #Get the url of first page
    if id == 1:
        firstPage = res.url
    
    #Get data from all news in this page
    setUrls = GetData.getUrlsVnExpress(res) 
    for link in setUrls:
        try:
            data = GetData.vnexpress(link, ses)
        except Exception as err:
            print("Missing data at " + link)
            print("Type Error: " + str(err.args) )
        finally:
            dataSource.append(data)        
    id += 1

print("number of news: "+ str(len(dataSource)))
#Transfer data to DB
#Initilize:
print('Start to create DB')
DataBase.make_connect()
DataBase.createEduNewTab()

#Bulk Inserts:
DataBase.insertMultiRecords(dataSource)

#Close DB:
DataBase.closeDB()




