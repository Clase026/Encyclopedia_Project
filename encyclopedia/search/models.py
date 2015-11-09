from django.db import models

import ConfigParser
from imgurpython import *
import posixpath
import requests
from urllib2 import parse_http_list


#
#   Imgur API integration
#
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


#
#   Twitter API integration
#
class TwitterSearch:

    def __init__(self, EncyclopediaData, searchstring):
        self.EncyclopediaData = EncyclopediaData
        self.searchstring = searchstring
        self.auth = self.setupauthentication()
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def setupauthentication(self):
        """Only authenticates for an app, since it only searches for tweets"""
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        APIKey = config.get('TwitterKeys','APIKey')
        APISecret = config.get('TwitterKeys','APISecret')
        auth = tweepy.AppAuthHandler(APIKey,APISecret)
        return auth

    def dosearch(self):
        """Searches for tweets matching the searchstring"""
        tweets = []
        indexOftweets = self.api.search(q=self.searchstring)
        print len(indexOftweets)
        for i in range(len(indexOftweets)):
            if len(tweets) < 10 and i < len(indexOftweets):
                twt = indexOftweets[i]
                if not (hasattr(twt, 'retweeted_status') or hasattr(twt, 'quoted_status')):
                    asciitweet = TwitterStatus(twt.user.name.encode('ascii', 'ignore'), twt.text.encode('ascii', 'ignore'),self.searchstring)
                    tweets.append(asciitweet)
            else:
                break
        self.savesearchresults(tweets)
        return tweets

    def savesearchresults(self, tweets):
        for tweet in tweets:
            self.EncyclopediaData.inserttwitterdata(tweet.username, tweet.text, tweet.searchstring)

    def getrelatedsavedtweets(self):
        """Gets tweets matching the searchstring from the database"""
        savedtweets = self.EncyclopediaData.getsearchedtweets(self.searchstring)
        tweets = []
        for savedtweet in savedtweets:
            tweet = TwitterStatus(savedtweet[0],savedtweet[1],savedtweet[2])
            tweets.append(tweet)
        return tweets

    def searchorloadtweets(self):
        """Gets data from the database matching the searchstring, and hits the API if it can't find anything"""
        tweets = None
        if self.getrelatedsavedtweets() == []:
            tweets = self.dosearch()
        else:
            tweets = self.getrelatedsavedtweets()
        return tweets


class TwitterStatus:
    """A single twitter status, containing the username, the tweet text, and the string used to find it"""
    def __init__(self, username, text, searchstring):
        self.searchstring = searchstring
        self.text = text
        self.username = username

    def displaytweet(self):
        return self.text


#
#   Wikipedia API integration
#
class WikipediaSearch:

    def __init__(self, EncyclopediaData, searchstring = 'Wikipedia'):
        self.ED = EncyclopediaData
        self.searchstring = searchstring

    def getarticletitleoptions(self):
        searchresults = []
        try:
            searchresults = [wikipedia.WikipediaPage(self.searchstring).title]
        except wikipedia.exceptions.DisambiguationError as e:
            searchresults = e.options
        return searchresults

    def disambiguatetitle(self,title):
        try:
            disambiguatedtitle = wikipedia.WikipediaPage(title).title
        except wikipedia.exceptions.DisambiguationError as e:
            disambiguatedtitle = self.disambiguatetitle(e.options[0])
        return disambiguatedtitle

    def getarticlefromtitle(self,title):
        """Takes the first search result for the searchstring, and returns a wikipediaarticle"""
        # print title
        disambiguatedtitle = self.disambiguatetitle(title)
        article = wikipedia.WikipediaPage(disambiguatedtitle)
        articletitle = article.title #.encode('ascii', 'ignore')
        articlesummary = article.summary #.encode('ascii', 'ignore')
        article = WikipediaArticle(articletitle,articlesummary,self.searchstring)
        return article


    def saveresult(self, article):
        self.ED.insertwikidata(article.articletitle, article.articlesummary, article.searchstring)

    def getrelatedsavedresults(self):
        """Gets saved wikipedia articles matching the search string"""
        savedresults = self.ED.getrelatedsavedwikiarticle(self.searchstring)
        articles = []
        for result in savedresults:
            article = WikipediaArticle(result[0],result[1],result[2])
            articles.append(article)
        return articles

    def searchorloadarticle(self):
        """Checks the database for related articles, and only hits the api if it doesn't find anything"""
        articles = None
        if self.getrelatedsavedresults() == []:
            articletitle = self.getarticletitleoptions()[0]
            article = self.getarticlefromtitle(articletitle)
            self.saveresult(article)
            articles = [article]
        else:
            articles = self.getrelatedsavedresults()
        return articles

class WikipediaArticle:
    """The summary, title, and string used to find a wikipedia article"""
    def __init__(self, articletitle, articlesummary, searchstring):
        self.articletitle = articletitle
        self.articlesummary = articlesummary
        self.searchstring = searchstring

    def displayarticle(self):
        displaystring = self.articletitle + '\n' + self.articlesummary
        return displaystring

