Pretty Parser
=============

**A personalized RSS feed aggregator.**

## How to use
#### Run the applet
1. **Windows:** Download the `Pretty Parser for Windows` directory. Run `PrettyParser.exe`. Enjoy.
2. **Linux:** The Windows applet works perfectly via Wine. You can install `Wine` from the Ubuntu Software Center or [get it here](https://www.winehq.org/).
3. **macOS:** No luck for you guys, *yet*.

#### Run natively in Python
This works on any OS, obviously.  
You'll need Python 3.x installed on your system along with the `Beautiful Soup` and `Requests` modules, and probably `LXML` as well. (All available via `pip` and `easy install`)

## How it works
1. The `fetch()` function downloads the XML files from the website's server.
2. The `populate()` function creates a local database from all the available XML feeds.
3. The `user_queries()` function takes in user preference.
3. The `pparser()` function assembles 25 random articles (by default) from all the sources and displays them in your system's default browser.
4. The `style.css` file is to make things look Pretty.

Of course you can edit the `feeds` dictionary and the corresponding `feed_tags` list to whichever feeds you want to follow.

## Features
Listed newest first -
* User can choose how many articles to view per page.
* User can decide whether articles should repeat or not.
* User can choose how old the articles should be. (0 for today's, 1 for since yesterday, 2 for since day before...)
* PrettyParser can detect old XML files.
* XML files are neatly stacked in a local folder.
* WINDOWS APPLET BIIITTCCHHEEESSSS!

### Known Issues
* The Windows applet quits automatically after fetching sources. Works fine if you run it again.
