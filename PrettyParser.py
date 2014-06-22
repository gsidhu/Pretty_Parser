## Pretty Parser 
## MIT License, 2014 Gurjot S. Sidhu 

from bs4 import BeautifulSoup as BS
import urllib.request as urr
import webbrowser 
import random
import re

data = {}
feeds = {'thehindu': 'http://www.thehindu.com/news/?service=rss',  'theguardian_football': 'http://feeds.theguardian.com/theguardian/uk/sport/rss', 'wired': 'http://feeds.wired.com/wired/index', 'sci_am': 'http://rss.sciam.com/sciam/physics', 'xkcd_whatif': 'http://what-if.xkcd.com/feed.atom', 'mashable': 'http://feeds.mashable.com/Mashable', 'cnet': 'http://www.cnet.com/rss/news/', 'aljazeera': 'http://america.aljazeera.com/content/ajam/articles.rss', 'cgpgrey': 'http://gdata.youtube.com/feeds/base/users/CGPGrey/uploads?alt=rss&orderby=published', 'kanangill': 'http://gdata.youtube.com/feeds/base/users/knngill/uploads?alt=rss&orderby=published',  'minutephysics': 'http://gdata.youtube.com/feeds/base/users/minutephysics/uploads?alt=rss&orderby=published', 'abishmathew': 'http://gdata.youtube.com/feeds/base/users/UCtWoDeegvTPfuuNm_ilJntg/uploads?alt=rss&orderby=published', 'lastweektonight': 'http://gdata.youtube.com/feeds/base/users/lastweektonight/uploads?alt=rss&orderby=published', 'jusreign': 'http://gdata.youtube.com/feeds/base/users/jusreign/uploads?alt=rss&orderby=published', 'alltime10s': 'http://gdata.youtube.com/feeds/base/users/Alltime10s/uploads?alt=rss&orderby=published', 'itsokaytobesmart': 'http://gdata.youtube.com/feeds/base/users/itsokaytobesmart/uploads?alt=rss&orderby=published', 'TED': 'http://gdata.youtube.com/feeds/base/users/tedtalksdirector/uploads?alt=rss&orderby=published', 'numberphile': 'http://gdata.youtube.com/feeds/base/users/numberphile/uploads?alt=rss&orderby=published', 'vsauce': 'http://gdata.youtube.com/feeds/base/users/vsauce/uploads?alt=rss&orderby=published', 'cokestudio': 'http://gdata.youtube.com/feeds/base/users/cokestudio/uploads?alt=rss&orderby=published', 'asapscience': 'http://gdata.youtube.com/feeds/base/users/AsapSCIENCE/uploads?alt=rss&orderby=published', 'AIB': 'http://gdata.youtube.com/feeds/base/users/UCzUYuC_9XdUUdrnyLii8WYg/uploads?alt=rss&orderby=published', 'smarter_every_day': 'http://gdata.youtube.com/feeds/base/users/destinws2/uploads?alt=rss&orderby=published'}
feed_tags = ['cnet', 'sci_am', 'aljazeera', 'theguardian_football', 'thehindu', 'wired', 'mashable']
youtube = ['alltime10s', 'AIB', 'abishmathew', 'asapscience', 'cgpgrey', 'cokestudio', 'itsokaytobesmart', 'jusreign', 'kanangill', 'lastweektonight', 'minutephysics', 'numberphile', 'TED', 'smarter_every_day', 'vsauce']
##feeds = {}
##feed_tags = []
##while True:
##    link = input("RSS URL: ")
##    if link == '':
##        break
##    tag = input("Tag for this feed: ")
##    feeds[tag] = link
##    feed_tags.append(tag)

def fetch():
    global data
    global feeds
    global feed_tags
    global youtube
    for tag in feed_tags+youtube:
##        fetch = urr.urlretrieve(feeds[tag], tag + '.xml')
        rss_file = open(tag+'.xml')
        soup = BS(rss_file, 'xml')
        local_data = []
        #parsing xml item-wise
        items = soup.find_all('item')
        count = 0
        for item in items:
            count += 1
            #tags = [x.name for x in i.find_all(True, recursive=False)]
            title = item.find('title')
            pubdate = item.find('pubdate')
            description = item.find('description')
            author = item.find('dc:creator')
            links = item.find('link')
            
            if pubdate == None:
                pubdate = item.find('pubDate')
            if author == None:
                author = soup.find('author')
            if author == None:
                author = soup.find('title')
            if tag in feed_tags:
                p = re.compile(r'<a.*?>')
                description = p.sub('',description.text)
                p = re.compile(r'<img.*?>')
                description = p.sub('',description)
                p = re.compile(r'<div.*?>')
                description = p.sub('',description)
                p = re.compile(r'</.*?>')
                description = p.sub('',description)
                p = re.compile(r'<.*?>')
                description = p.sub('',description)
                if len(description) > 300:
                    description = description[:300] + " ..."
            
            if type(description) != str:
                description = description.text
            local_data.append({"title": title.text, "pubdate":pubdate.text,"author":author.text,"description":description,"link":links.text})
            if count > 10:
                break
        data[tag] = (local_data)
        rss_file.close()

no_rep = True
##    if input("Do you want the articles to repeat after you've viewed them once? (Y/N) ") == "Y":
##        no_rep = False 

def pparser():
    global data
    global feeds
    global feed_tags
    global youtube
    html_file = open('tmp.html', 'w+')    
    html_content = '''
    <!DOCTYPE html>
    <html>
    <title>
        Pretty Parser
    </title>
    <head>
            <meta charset="utf-8"> 
            <link href='http://fonts.googleapis.com/css?family=Overlock' rel='stylesheet' type='text/css'>
            <link href='http://fonts.googleapis.com/css?family=Bad+Script' rel='stylesheet' type='text/css'>
            <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
        <div id='topbar'>
                <h1> Pretty Parser </h1>
                    <h5> Built with love and lots of chocolates </h5>
        </div>
    '''

    num = 25

    while num > 0:
        tag_choice = random.choice(feed_tags)
        while len(data[tag_choice]) < 2:
            tag_choice = random.choice(feed_tags + youtube)
        if num < 6:
            tag_choice = random.choice(youtube)
        article_choice = random.randint(0,len(data[tag_choice])-1)
        
        content = '''
            <div class='item'>
                    <span id = 'title'>
                            <h2> <a href= "''' + data[tag_choice][article_choice]["link"] + '''" target="_blank">''' + data[tag_choice][article_choice]["title"] + '''</a></h2>
                    </span>
                    <span id ='pubdate'> 
                            <h5>''' + data[tag_choice][article_choice]["pubdate"] + '''</h5>
                    </span>
                    <span id ='author'>
                            <h5>''' + data[tag_choice][article_choice]["author"] + '''</h5>
                    </span>
                    <span id ='description'>
                            <p>''' + data[tag_choice][article_choice]["description"] + '''</p>
                    </span>
        </div>
        '''
        html_content += content
        content = ''
        num -= 1

        if no_rep == True:
            data[tag_choice].remove(data[tag_choice][article_choice])

    html_content += '''
    </body>
    </html>
    '''

    html_file.write(html_content)
    html_file.close()

    webbrowser.open('tmp.html')

    again = input("More articles? ")
    if again == '':
        pparser()
