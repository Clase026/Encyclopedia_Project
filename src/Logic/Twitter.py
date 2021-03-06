__author__ = '?'

import tweepy
import ConfigParser
import src.Database.EncyclopiaData

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
        for status in self.api.search(q=self.searchstring, count=20):
            if not (hasattr(status, 'retweeted_status') or hasattr(status, 'quoted_status')):
                asciitweet = TwitterStatus(status.user.name.encode('ascii', 'ignore'), status.text.encode('ascii', 'ignore'),self.searchstring)
                tweets.append(asciitweet)
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
