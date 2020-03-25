import requests as rq
from bs4 import BeautifulSoup
import re
from newspaper import Article
import unicodedata

# Getting all url from page


def get_urls_vnexpress(response):
    setUrl = []  # set of url
    
    soup = BeautifulSoup(response.content, 'lxml') # parsing html

    # Get url from main containers
    soup_new = soup.find_all('section', class_=(
        'featured container clearfix', 'sidebar_1'))
    for sec in soup_new:
        sec = sec.find_all(class_='title_news')
        for val in sec:
            link = val.a['href'].strip()
            if link is not '':
                setUrl.append(link)
    return setUrl

# Getting data of vnexpress

def get_vnexpress(url):
    content = ""
    title = ""
    response = rq.get(url)
    pageUrl = response.url  # get url
    if(response):

        resHtml = BeautifulSoup(response.content, 'lxml')        
        title = resHtml.find('h1', class_='title_news_detail')        
        contentHtml = resHtml.find('section', class_='sidebar_1')

        # Error if this new has no content
        if(title is None or contentHtml is None):            
            # The web may change the format of html.
            # So it should use newspaper3k for this situation
            article = Article(url, language='vi')
            article.download()
            article.parse()
            if article.text.strip() == '':
                raise Exception('No content')
            else:
                return (pageUrl, article.title, article.meta_description + ' ' + article.text)

        #The format of html is the same as the config 
        title = title.text.strip()
        title = title.replace(u'\xa0', ' ')
        paragr = contentHtml.find_all('p', class_=re.compile(
            "Normal|description"))  # get every paragraph
        for cktext in paragr:
            content += cktext.text
        content = content.strip() 
        content = content.replace(u'\xa0', ' ')
        return (pageUrl, title, content)
    else:
        raise Exception('Fail to connect')
