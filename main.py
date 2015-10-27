# -*- coding: utf-8 -*-

from browser import ChromeBrowser
from utilities import setup_logging


def main():
    setup_logging('main')
    chrome = ChromeBrowser()
    chrome.save_bookmarks()


if __name__ == '__main__':
    main()