import requests as rq
from bs4 import BeautifulSoup
import re
from newspaper import Article

# Getting all url from page


def getUrlsVnExpress(response):
    setUrl = []  # set of url

    # parse html
    soup = BeautifulSoup(response.content, 'lxml')

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


def vnexpress(url):
    content = ""
    title = ""
    response = rq.get(url)
    pageUrl = response.url  # get url
    if(response):

        # Parse Html
        resHtml = BeautifulSoup(response.content, 'lxml')

        # init title:
        title = resHtml.find('h1', class_='title_news_detail')

        # init content:
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
        title = title.text.strip()#remove \n and white space
        paragr = contentHtml.find_all('p', class_=re.compile(
            "Normal|description"))  # get every paragraph
        for cktext in paragr:
            content += cktext.text
        content = content.strip() #remove \n and white space
        return (pageUrl, title, content)
    else:
        raise Exception('Fail to connect')
