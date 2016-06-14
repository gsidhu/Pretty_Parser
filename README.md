Pretty Parser
=============

**A personalized RSS reader.**

You'll need Python 3.x installed on your system along with the Beautiful Soup library.

1. Run the `.py` file. 
2. Call the `fetch()` function to download all the XML files.
3. Call the `pparser()` function to read your feed in your system's default browser.
4. The Terminal window should say `More articles?` (shows 25 articles by default). Press enter to load a new list of articles. Press 'n' to exit.

Of course you can edit the `feeds` dictionary and the corresponding `feed_tags` list to whichever feeds you want to follow.

*Note to self: Someday I will turn this into a browser add-on.*
