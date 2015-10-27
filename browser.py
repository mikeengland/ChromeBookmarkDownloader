# -*- coding: utf-8 -*-

import json
import os
import codecs
import logging
from web import WebScraper
from utilities import mkdir_p

logger = logging.getLogger(__name__)


class Browser:
    """High-level class to set the required browser properties"""

    def __init__(self, bookmark_location=None, output_location=None):
        self.bookmark_location = bookmark_location
        self.output_location = output_location
        self.logger = logger

    def load_browser_bookmarks(self):
        """ Abstract method for retrieving the browser bookmarks"""
        raise NotImplementedError()

    def process_bookmarks(self):
        """Abstract method for processing bookmarks and returning a dict"""
        raise NotImplementedError()


class ChromeBrowser(Browser):
    """Class to download Chrome bookmarks"""

    def __init__(self):
        super().__init__()
        self.folders = {}

        if self.output_location is None:
            self.output_location = '/Users/{}/bookmarks/{}'.format(os.environ['LOGNAME'], self.__class__.__name__)

        if self.bookmark_location is None:
            self.bookmark_location = '/Users/{}/Library/Application Support/Google/Chrome/Default/Bookmarks'.format(os.environ['LOGNAME'])

    def load_browser_bookmarks(self):
        """Load chrome bookmarks from file"""

        with codecs.open(self.bookmark_location, 'r', 'utf-8') as file:
            content = file.read()

        bookmark_data = json.loads(content)

        return bookmark_data

    def get_bookmarks(self, bookmark_data):
        """Return cleansed bookmark data as a dictionary"""
        self.bookmark_data = self._process_bookmarks(bookmark_data)
        return self.bookmark_data

    def _process_bookmarks(self, bookmark_data, folder=None):
        """Recursive function used internally to process the 
           JSON data and return a cleansed dict"""

        if isinstance(bookmark_data, dict):
            if 'type' in bookmark_data.keys():
                if bookmark_data['type'] == 'url':
                    if folder is not None and folder not in self.folders:
                        self.folders[folder] = []
                    self.folders[folder].append({'url': bookmark_data['url'], 
                                                 'name': bookmark_data['name']})
                    return
                elif bookmark_data['type'] == 'folder':
                    if 'children' in bookmark_data.keys() and len(bookmark_data['children']) > 0:
                        for item in bookmark_data['children']:
                            self._process_bookmarks(item, folder=bookmark_data['name'])
                    else:
                        return
            else:
                for item in bookmark_data:
                    if 'name' not in bookmark_data.keys():
                        name = 'root'
                    else:
                        name = bookmark_data['name']

                    self._process_bookmarks(bookmark_data[item], folder=name)

    def save_bookmarks(self):
        """Save bookmarks to file structure"""

        data = self.load_browser_bookmarks()
        self._process_bookmarks(data)

        for folder in self.folders.keys():
            # strip forward slashes from folder names
            folder = folder.replace('/', '')
            folder = folder.replace('\\', '')

            # create Chrome directories
            path = self.output_location + '/' + folder + '/'
            mkdir_p(path)

            for item in self.folders[folder]:

                # create new directory for web page
                web_page_path = path + '/' + item['name']
                mkdir_p(web_page_path)

                # create new directory for web page resources directory
                web_page_resources = web_page_path + '/resources'
                mkdir_p(web_page_resources)

                # strip slashes from web page names
                name = item['name']
                name = name.replace('/', '')
                name = name.replace('\\', '')

                # Skip URLs with PDF extension
                if '.pdf' in name[-4:]:
                    continue

                # save files
                try:
                    self.logger.info('Getting URL {}'.format(item['url']))
                    web_object = WebScraper(item['url'])

                    # get web page css
                    css = web_object.get_css()

                    # get web page content
                    content = web_object.get_web_page()

                    # save main web page
                    with open(web_page_path + '/bookmark.html', 'wb') as f:
                        f.write(content)

                    # save css files
                    if css is not None:
                        with open(web_page_resources + '/styles.css', 'wb') as f:
                            f.write(css)

                    self.logger.info('Successfully saved URL {}'.format(item['url']))
                except Exception as e:
                    self.logger.error('Web page not saved - {} - {}'.format(item['url'], e))
                    pass


if __name__ == '__main__':
    pass