# -*- coding: utf-8 -*-

import requests
import urllib
import logging
import lxml.etree
from bs4 import BeautifulSoup


class WebScrapeError(Exception):
    pass


logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, url):
        self.url = url
        self._get_main_content()

    def _get_main_content(self):
        '''
        Method to retrieve web page content from URL
        '''
        try:
            self.main_content = requests.get(self.url, timeout=5.0).text.encode('utf-8')
            return self.main_content
        except Exception as e:
            raise WebScrapeError(e)

    @staticmethod
    def get_resource_content(url):
        '''
        Static method to retrieve resource content e.g. css/js
        '''
        try:
            response = requests.get(url, timeout=5.0).text
            return response
        except Exception as e:
            raise WebScrapeError(e)

    def get_css(self):
        '''
        Get css data from web page. This includes internal and external
        css styles.
        '''
        # some code here was adapted from a useful article at
        # http://www.thelinuxdaily.com/2011/05/python-script-to-grab-all-css-for-given-urls/
        self.css_style = ''

        self.main_content = self._get_main_content()
        soup = BeautifulSoup(self.main_content, 'lxml')
        response = None

        # find external css styles
        css_links = soup.findAll('link', rel='stylesheet')

        # get external styles
        if len(css_links) > 0:
            for link in css_links:
                css_link = link.get('href')
                if 'http' not in css_link and '///' not in css_link:
                    parsed_uri = urllib.parse.urlparse(self.url)
                    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    css_link = domain + '/' + css_link

                response = self.get_resource_content(css_link)
                if response is not None:
                    self.css_style += response

        # encode as utf-8
        if self.css_style != '':
            # remove new line and carriage return
            self.css_style = self.css_style.replace('\r\n', '\n')

        self.css_style = self.css_style.encode('utf-8')

        return self.css_style

    def alter_resource_links(self):
        '''
        Alter the css links in a web page to ensure that they now point
        to a local directory where the data will be stored
        '''
        root = lxml.etree.HTML(self.main_content)
        for link in root.iter('link'):
            css_link = None
            css_link = link.get('href', None)
            if css_link is not None:
                link.attrib['href'] = './resources/styles.css'
        self.altered_html = lxml.etree.tostring(root)

        return self.altered_html

    def get_web_page(self):
        '''
        Return web page. The css links are altered to ensure
        they point to a local location
        '''
        return self.alter_resource_links()

