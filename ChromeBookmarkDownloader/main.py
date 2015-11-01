# -*- coding: utf-8 -*-
import logging
import logging.config
from logger import get_logger_dict
from browser import ChromeBrowser

def main():
    # Setup logging    
    logger_dict = get_logger_dict()
    logging.config.dictConfig(logger_dict)
    
    # Set requests to warning as minimum level or it gets very noisy
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # Save Chrome bookmarks
    chrome = ChromeBrowser()
    chrome.save_bookmarks()


if __name__ == '__main__':
    main()