__author__ = '?'

import ConfigParser
from imgurpython import *
import posixpath
import requests
from urllib2 import parse_http_list


class ImgurSearch:

    # def __init__(self, EncyclopediaData, searchstring):
    def __init__(self, searchstring):
        # self.ED = EncyclopediaData
        self.client = self.setupclient()
        self.searchstring = searchstring

    def setupclient(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        APIKey = config.get('ImgurKeys','APIKey')
        APISecret = config.get('ImgurKeys','APISecret')
        client = ImgurClient(APIKey, APISecret)
        return client

    def dosearch(self):
        links = []
        pics = self.client.gallery_search(self.searchstring, advanced=None, sort='top', window='all', page=0)
        for p in pics:
            if len(links) < 10:
                if not ".gif" in p.link:
                    links.append(p.link)
            else:
                break
        return links
