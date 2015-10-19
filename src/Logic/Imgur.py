__author__ = '?'

import ConfigParser
from imgurpython import *
import posixpath
import requests
from urllib2 import parse_http_list


class ImgurSearch:

    def __init__(self, EncyclopediaData, searchstring):
        self.ED = EncyclopediaData
        self.searchstring = searchstring
        self.client = self.setupclient()

    def setupclient(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        APIKey = config.get('ImgurKeys','APIKey')
        APISecret = config.get('ImgurKeys','APISecret')
        client = ImgurClient(APIKey, APISecret)
        return client

    def dosearch(self):
        items = self.client.gallery_search(q=self.searchstring)
        for item in items:
            print item.link
            url = item.link
            #TODO: Learn how to deal with JSON
            #http://stackoverflow.com/questions/12903938/downloading-file-from-imgur-using-python-directly-via-url
            r = requests.get(url)
            img_url = r.json["image"]["links"]["original"]
            #fn = posixpath.basename(urllib2.parse.urlsplit(img_url).path)

            r = requests.get(img_url)
            with open(img_url, "wb") as f:
                f.write(r.content)

