## Pretty Parser 
## MIT License, 2016 Gurjot S. Sidhu 

from bs4 import BeautifulSoup as BS
import urllib.request as urr
import webbrowser 
import random
import re
import requests
import os

home_dir = os.getcwd()
data = {}
feeds = {'thehindu': 'http://www.thehindu.com/news/?service=rss', 'theguardian_football': 'http://feeds.theguardian.com/theguardian/uk/sport/rss', 'wired': 'http://feeds.wired.com/wired/index', 'sci_am': 'http://rss.sciam.com/sciam/physics', 'xkcd_whatif': 'http://what-if.xkcd.com/feed.atom', 'mashable': 'http://feeds.mashable.com/Mashable', 'cnet': 'http://www.cnet.com/rss/news/', 'aljazeera': 'http://america.aljazeera.com/content/ajam/articles.rss', 'vox': 'http://www.vox.com/rss/index.xml', 'theguardian_world': 'http://www.theguardian.com/world/rss', 'empire_kop': 'http://www.empireofthekop.com/feed/', 'caravan': 'http://www.caravanmagazine.in/feed', 'new_yorker': 'http://www.newyorker.com/rss', 'brain_pickings': 'https://www.brainpickings.org/feed/'}
feed_tags = ['cnet', 'sci_am', 'aljazeera', 'theguardian_football', 'thehindu', 'wired', 'mashable', 'vox', 'empire_kop', 'caravan', 'new_yorker','brain_pickings']
# 'theguardian_world'

print("Yo. Welcome to Pretty Parser - the slickest, bare-bones RSS feed aggregator, ever.\n")
print("Do you want browse through my default feeds? Warning: Contains a Liverpool FC fan page.")
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
        feed_tags.append(tag)

print("Enjoy.\n")
def fetch():
    newpath = str(home_dir + '/XML_storage')
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    
    global data
    global feeds
    global feed_tags
    for tag in feed_tags:
        print(tag)
        url_string = feeds[tag]
        file_name = str(tag + '.xml')
        with open(file_name, 'wb') as f:
            resp = requests.get(url_string, verify=False)
            f.write(resp.content)
##        urr.urlretrieve(url_string, file_name)
        rss_file = open(tag+'.xml', encoding="utf8")
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

no_rep = True
##    if input("Do you want the articles to repeat after you've viewed them once? (Y/N) ") == "Y":
##        no_rep = False 

def pparser():
    os.chdir(home_dir)
    global data
    global feeds
    global feed_tags
    html_file = open('tmp.html', 'w+', encoding="utf8")
    html_content = '''
    <!DOCTYPE html>
    <html>
    <title>
        Pretty Parser
    </title>
    <head>
            <meta charset="utf-8"> 
            <link href='https://fonts.googleapis.com/css?family=Overlock' rel='stylesheet' type='text/css'>
            <link href='https://fonts.googleapis.com/css?family=Bad+Script' rel='stylesheet' type='text/css'>
            <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
        <div id='topbar'>
                <a href="https://github.com/gsidhu/Pretty_Parser"> <h1> Pretty Parser </h1></a>
        </div>
    '''

    num = 25

    while num > 0:
        tag_choice = random.choice(feed_tags)
        while len(data[tag_choice]) < 2:
            tag_choice = random.choice(feed_tags)
        article_choice = random.randint(0,len(data[tag_choice])-1)
        
        content = '''
            <div class='item'>
                    <span id = 'title'>
                            <h2> ''' + str(str(26-num)+". ") + ''' <a href= "''' + data[tag_choice][article_choice]["link"] + '''" target="_blank">''' + data[tag_choice][article_choice]["title"] + '''</a></h2>
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
    <footer class="footer">
	<hr>
	<h4> &copy; 2016. Some rights reserved. Built with &#9829; and lots of chocolate. </h4>
	</footer>
    </body>
    </html>
    '''

    html_file.write(html_content)
    html_file.close()

    webbrowser.open('tmp.html')

    again = input("More articles? Press Enter for Hell Yeah or any other key for Nuh-uh. : ").lower()
    if again == '':
        pparser()
    elif again == 'n':
        return 0

if __name__ == "__main__":
    fetch()
    pparser()
