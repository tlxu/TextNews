#!/usr/bin/python3

import urllib.request
import sys

from bs4 import BeautifulSoup


"""
Read text news from ctvnews.ca
"""

weburl = "http://toronto.ctvnews.ca/more/local-news"


### get article list
req = urllib.request.Request(weburl)
response = urllib.request.urlopen(req)
the_page = response.read()
type = sys.getfilesystemencoding()
 
soup = BeautifulSoup(the_page.decode(type))
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



count = 1
for news in newsList:
    print(count)
    print(news["title"])
    print(news["href"])
    count += 1
    print("\n")
print(count)



"""
<div class="articleBody">
    bla...bla...bla...
</div>
"""
### get article body

