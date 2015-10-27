# ChromeBookmarkDownloader
Python tool to download Google Chrome bookmarks for offline use on a Mac

The aim of this Python project is to traverse your Google Chrome bookmarks file and save each bookmark for offline use. The code uses a combination of the very useful urllib, requests and BeautifulSoup modules.

This is only an initial upload!!

The current flow of code is to do the following:
- Traverse the JSON bookmark file
- For each URL bookmark, scrape the web page
- Scrape all stylesheet links and combine them into a styles.css file for each bookmark
- Alter the web page stylesheet links to point to the new styles.css file
- Save the styles.css file and the web page .html file

Current limitations/To Do
- Recursive algorithm to traverse the bookmarks file needs to keep track of the file path tree so saved bookmarks appear on the filesystem exactly as they do in Chrome
- Save images
- Further tuning of CSS collection
- Parallelise the collector
- Log to file
- Allow changing of output location/bookmark file locations via a config option
- Allow it to be run as an executable
- Possibly enhance to include Firefox/Safari
- Possibly enhance to work with Windows/Linux Chrome installations
