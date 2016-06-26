## Pretty Parser 
## MIT License, 2016 Gurjot S. Sidhu 

from bs4 import BeautifulSoup as BS
#import urllib.request as urr
import webbrowser 
import random
import re
import requests
import os
import datetime 

home_dir = os.getcwd()
data = {}
feeds = {'thehindu': 'http://www.thehindu.com/news/?service=rss', 'theguardian_football': 'http://feeds.theguardian.com/theguardian/uk/sport/rss', 'wired': 'http://feeds.wired.com/wired/index', 'sci_am': 'http://rss.sciam.com/sciam/physics', 'xkcd_whatif': 'http://what-if.xkcd.com/feed.atom', 'mashable': 'http://feeds.mashable.com/Mashable', 'cnet': 'http://www.cnet.com/rss/news/', 'aljazeera': 'http://america.aljazeera.com/content/ajam/articles.rss', 'vox': 'http://www.vox.com/rss/index.xml', 'theguardian_world': 'http://www.theguardian.com/world/rss', 'empire_kop': 'http://www.empireofthekop.com/feed/', 'caravan': 'http://www.caravanmagazine.in/feed', 'new_yorker': 'http://www.newyorker.com/rss', 'newyork_times': 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalHome.xml', 'brain_pickings': 'https://www.brainpickings.org/feed/', 'tribune_ludhiana': 'http://www.tribuneindia.com/rss/feed.aspx?cat_id=15', 'tribune': 'http://www.tribuneindia.com/rss/feed.aspx?cat_id=7', 'bbc': 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'}
feed_tags = ['cnet', 'sci_am', 'theguardian_football', 'thehindu', 'wired', 'mashable', 'vox', 'empire_kop', 'caravan', 'new_yorker','newyork_times','brain_pickings','tribune','tribune_ludhiana', 'bbc']
# 'theguardian_world'
local_feed_tags = []

print("Yo, whaddup?\nWelcome to Pretty Parser - the slickest, bare-bones RSS feed aggregator, ever.\n")
print("Do you want browse through my default feeds? \nWarning: Contains a Liverpool FC fan page and some other local newspapers.")
stick2def = input("Press Enter for Yaas or 'N' for Nooo: ").lower()

if stick2def == 'n':
    feeds = {}
    feed_tags = []
    print("\nAll right. You can add your own RSS links in the next step. Press Enter when you're done.\n")
    while True:
        link = input("Input RSS URL: ")
        if link == '':
            break
        tag = input("Input a name tag for this feed: ")
        feeds[tag] = link
#        feed_tags.append(tag)

def fetch():
    newpath = str(home_dir + '/XML_storage')
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    
    global feeds
    global feed_tags

    print("\nFetching data from sources.")
    for tag in feed_tags:
        url_string = feeds[tag]
        file_name = str(tag+".xml")
        with open(file_name, 'wb') as f:
            resp = requests.get(url_string, verify=False)
            f.write(resp.content)
##        urr.urlretrieve(url_string, file_name)
            
def populate():
    newpath = str(home_dir + '/XML_storage')
    if os.path.exists(newpath):
        os.chdir(newpath)
    else:
        raise OSError("XML data not found.")
    
    global data
    global feeds
    global local_feed_tags
    
    xml_files = os.listdir(".")
    for names in xml_files:
        if names.endswith(".xml"):
            local_feed_tags.append(names)

    print("\nGenerating feed from the following sources:")
    for name in local_feed_tags:
        tag = name[:-4]
        print(tag)
        rss_file = open(name, encoding="utf8")
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
            ## Note to self: item.find looks for tags within the item,
            ## soup.find looks for global tags outside the items
            if pubdate == None:
                pubdate = item.find('pubDate')
            if pubdate == None:
                pubdate = soup.find('lastBuildDate')
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

def user_queries():
    how_old = input("\nHow old would you like your news to be? (Input 0 for today's news): ")
    no_rep = True
    if input("Do you want the articles to repeat after you've viewed them once? (Y/N) ").lower() == "Y":
        no_rep = False 
    num = input("How many articles do you want to see per page? Press Enter to use default (25): ")
    if num == '':
        num = 25
    num = int(num)
    return how_old,num,no_rep

def pparser(how_old,num,no_rep):
    os.chdir(home_dir)
    global data
    global feeds
    global local_feed_tags
    html_file = open('tmp.html', 'w+', encoding="utf8")
    html_content = '''
    <!DOCTYPE html>
    <html>
    <title>
        Pretty Parser
    </title>
    <head>
            <meta charset="utf-8"> 
            <link href='https://fonts.googleapis.com/css?family=Bad+Script' rel='stylesheet' type='text/css'>
            <link href='https://fonts.googleapis.com/css?family=Economica:700' rel='stylesheet' type='text/css'>
            <link href='https://fonts.googleapis.com/css?family=PT+Serif' rel='stylesheet' type='text/css'>
            <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
        <div id='topbar'>
                <h1><a href="https://github.com/gsidhu/Pretty_Parser">  Pretty Parser </a></h1>
        </div>
    '''
    counter = num
    while counter > 0:
        today = datetime.date.today()
        article_date = datetime.datetime.strptime("01 Jan 2001", '%d %b %Y').date()
        while today - article_date > datetime.timedelta(int(how_old)):
            tag_choice = random.choice(local_feed_tags)[:-4]
            while len(data[tag_choice]) < 2:
                tag_choice = random.choice(local_feed_tags)[:-4]
            article_choice = random.randint(0,len(data[tag_choice])-1)
            try:
                article_date = datetime.datetime.strptime(data[tag_choice][article_choice]["pubdate"], '%a, %d %b %Y %H:%M:%S %z').date()
            except:
                article_date = datetime.datetime.strptime(data[tag_choice][article_choice]["pubdate"], '%a, %d %b %Y %H:%M:%S %Z').date()

        content = '''
            <div class='item'>
                    <span id = 'title'>
                            <h2> ''' + str(str(num+1-counter)+". ") + ''' <a href= "''' + data[tag_choice][article_choice]["link"] + '''" target="_blank">''' + data[tag_choice][article_choice]["title"] + '''</a></h2>
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
        <hr>
        '''
        html_content += content
        content = ''
        counter -= 1

        if no_rep:
            data[tag_choice].remove(data[tag_choice][article_choice])

    html_content += '''
    <footer class="footer">
        <h3><a href="https://gsidhu.github.io">  That Gurjot </a></h3>
        <h4><a href="https://github.com/gsidhu/Pretty_Parser">  Source </a></h4>
        <p> &copy; 2016. Some rights reserved. Built with &#9829; and lots of chocolate. </p>
	</footer>
    </body>
    </html>
    '''

    html_file.write(html_content)
    html_file.close()

    webbrowser.open('tmp.html')

    again = input("More articles? Press Enter for Hell Yeah or any other key for Nuh-uh. : ").lower()
    if again == '':
        pparser(how_old,num,no_rep)
    elif again == 'n':
        return 0

if __name__ == "__main__":
    newpath = str(home_dir + '/XML_storage')
    if os.path.exists(newpath):
        if input("\nThe force senses some old XML data files.\nDo you want to generate a feed from this old data?\nEnter is yes, any other key is no: ") != '':
            fetch()
        populate()
        how_old,num,no_rep = user_queries()
        pparser(how_old,num,no_rep)
    else:
        fetch()
        populate()
        pparser(how_old,num,no_rep)
