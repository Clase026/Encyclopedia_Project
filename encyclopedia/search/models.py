from django.db import models

import ConfigParser
import imgurpython
import posixpath
import requests
from urllib2 import parse_http_list


#
#   Search
#   Referenced by images, tweets, and articles.
#
class Search(models.Model):
    search_string = models.CharField(max_length=255)
    date = models.DateField()


#
#   Image
#   A result from Imgur.
#
class Image(models.Model):
    url = models.CharField(max_length=255)
    search = models.ForeignKey(Search)


#
#   Tweet
#   A result from Twitter.
#
class Tweet(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=255)
    search = models.ForeignKey(Search)


#
#   Article
#   A result from Wikipedia.
#
class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    search = models.ForeignKey(Search)
