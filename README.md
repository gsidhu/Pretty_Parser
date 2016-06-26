Pretty Parser
=============

**A personalized RSS feed aggregator.**

## Windows users
Download the `Pretty Parser for Windows` directory. Run `PrettyParser.exe`. Enjoy. (Follow the directions for more fun)

## UNIX
You'll need Python 3.x installed on your system along with the `Beautiful Soup` and `Requests` modules (and probably `LXML` as well).

#### How it works
1. The `fetch()` function downloads the XML files from the website's server.
2. The `populate()` function creates a local database from all the available XML feeds.
3. The `user_queries()` function takes in user preference.
3. The `pparser()` function assembles 25 random articles (by default) from all the sources and displays them in your system's default browser.
4. The `style.css` file is to make things look Pretty.

Terminal window should say `More articles?` (shows 25 articles by default). Press enter to load a new list of articles. Press 'n' to exit.  
Of course you can edit the `feeds` dictionary and the corresponding `feed_tags` list to whichever feeds you want to follow.

**Special shoutout to the devs behind `cx_Freeze` for helping port this applet to Windows.**

*Notes to self:*  
* Someday I will turn this into a browser add-on. And maybe port to macOS if I feel like it.
* Allow users to pick and choose feeds from defaults. 
* Add more sources to defaults (subreddits?).

#### Features
Listed newest first -
* User can choose how many articles to view per page
* User can decide whether articles should repeat or not
* User can choose how old the articles should be (0 for today's, 1 for since yesterday, 2 for since day before...)
* PrettyParser can detect old XML files
* XML files are neatly stacked in a local folder
* WINDOWS APPLET BIIITTCCHHEEESSSS!
