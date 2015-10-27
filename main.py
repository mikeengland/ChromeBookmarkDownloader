# -*- coding: utf-8 -*-

from browser import ChromeBrowser
from utilities import setup_logging
import logging

def main():
    # set basic logging
    format = '%(asctime)s - %(threadName)s - %(name)s - line %(lineno)d - %(levelname)s - %(message)s'
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO, format=format)
    
    # save Chrome bookmarks
    chrome = ChromeBrowser()
    chrome.save_bookmarks()


if __name__ == '__main__':
    main()