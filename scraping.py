#!/usr/bin/env python
# coding: utf-8

# In[1]:

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Import pandas for using data

# In[2]:


install("pandas")


# Install requests for interacting with web sever

# In[3]:


install("requests")

# Install beautifulsoup4 and html5lib for parsing html

# In[5]:


install("BeautifulSoup4")
install("html5lib")


# Install peewee and pymysql for connecting to DB

# In[ ]:


install("peewee")
install("pymysql")


# Test requests

# In[4]:


import requests as rq
url = "https://vnexpress.net/tin-tuc/giao-duc"
response = rq.get(url)
if response:
    print('Success!')
else:
    print('An error has occurred.')


# In[6]:


from bs4 import BeautifulSoup
import re


# In[9]:


#Getting content
def getContent(url):
    result = ""
    response = rq.get(url)
    if(response):
        resHtml = BeautifulSoup(response.content, 'html5lib') 
        content = resHtml.find_all('section', class_ = 'sidebar_1')
        if(len(content) == 0):
            return "No content"
        paragr = content[0].find_all('p', class_ = re.compile("Normal|description"))
        for cktext in paragr:
            result += cktext.text
        return result
    else:
        return "Fail to connect"


# In[11]:


import peewee
from peewee import *


# In[101]:


mysql_db = MySQLDatabase('news', user='root', password='25012000',
                         host='localhost', port=3306)


# In[102]:


#Creating table and connection 
class MySQLModel(peewee.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db
class eduNew(MySQLModel):
    news_title = CharField()
    news_content = TextField()
    class Meta:
        db_table = 'edunew'
mysql_db.connect(reuse_if_open = True)
eduNew.create_table()


# Main function

# In[103]:


soup = BeautifulSoup(response.content, 'html5lib') 
soup = soup.find('body')
soup_new = soup.find_all('a', href = re.compile("vnexpress\.net\/giao-duc"), title = re.compile("\w"))
for i in range (len(soup_new)):
    #Checking duplicate by using title
    title = soup_new[i]['title']
    query = eduNew.select().where(eduNew.news_title == title)
    if query.exists():
        continue
        
    content = getContent(soup_new[i]['href'])
    #Checking content
    if content in ["No content", "Fail to connect"]:
        continue
        
    #Adding to database
    objAdd = eduNew.create(news_title = title, news_content = content)
    objAdd.save()
    print(title)#for debugging
print("Finished")
if mysql_db.close():
    print("Closed connection with DB")





