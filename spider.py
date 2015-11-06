#!/usr/bin/python3

import urllib.request
import sys
import os.path
from bs4 import BeautifulSoup


"""
Read text news from ctvnews.ca
"""

weburl = "http://toronto.ctvnews.ca/more/local-news"
savedir = "./news/"


def getPageSourceFromURL(weburl):
    req = urllib.request.Request(weburl)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    type = sys.getfilesystemencoding()
    return the_page.decode(type)


def writeToFile(filename, lines):
    f = open(filename, "w");
    for line in lines:
        if line.string != None:        
            f.write(line.string)
    f.close()
    
### get article list
pageSource = getPageSourceFromURL(weburl)
soup = BeautifulSoup(pageSource)
news_div = soup.find("div", class_="element list topStoryPromo ")
news_li = news_div.find_all("li", class_="dc")


newsList = []
for news in news_li:
    """
        <h2 class="teaserTitle">
            <a  href="/trial-underway-for-two-men-accused-in-2011-port-lands-murder-1.2644539"   >Trial underway for
            two men accused in 2011 Port Lands murder</a>
        </h2>
    """
    teaserTitle = news.find("h2", class_="teaserTitle")
    tag = teaserTitle.a
    news_href = weburl + tag["href"]
    news_title =tag.string

    newsDict = {}
    newsDict["title"] = news_title
    newsDict["href"] = news_href

    newsList.append(newsDict)

"""
<div class="articleBody">
    <p> bla...bla...bla... </p>
    <p> bla...bla...bla... </p>
    <p> bla...bla...bla... </p>
    ...
</div>

Only care about <p>bla...</p>
"""
### get article body
count = 1

# reverse the newslist to make sure that older news will be saved first
newsList.reverse()
for news in newsList:
    print("{}: {}".format(count, news["title"]))
    count += 1

    fileName = savedir + news["href"].split("/")[-1] #get the last element in url    
    if  os.path.exists(fileName) == True:
        print("already exists")
        continue

    pageSource = getPageSourceFromURL(news["href"])
    soup = BeautifulSoup(pageSource)
    articleBody = soup.find("div", class_="articleBody")
    articleLines = articleBody.find_all("p")

    print("write to file")
    writeToFile(fileName, articleLines)

    print("\n")






