__author__ = 'anthonyclasen'

import sqlite3

class EncyclopediaData:
    """Holds stored data from wikipedia, tumblr, and twitter"""

    def __init__(self):
        self.connection = None
        self.connection = sqlite3.connect('EncyclopediaData')
        self.cursor = self.connection.cursor()

    def createtables(self):
        with self.connection:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS WikiData(ArticleTitle TEXT, SummaryText TEXT, SearchString TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS TwitterData(UserName TEXT, TweetText TEXT, SearchString TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS TumblrData(ImageTitle TEXT, Image BLOB, SearchString TEXT)')

    def recreatetables(self):
        with self.connection:
            self.cursor.execute('DROP TABLE IF EXISTS WikiData')
            self.cursor.execute('CREATE TABLE WikiData(ArticleTitle TEXT, SummaryText TEXT, SearchString TEXT)')
            self.cursor.execute('DROP TABLE IF EXISTS TwitterData')
            self.cursor.execute('CREATE TABLE TwitterData(UserName TEXT, TweetText TEXT, SearchString TEXT)')
            self.cursor.execute('DROP TABLE IF EXISTS TumblrData')
            self.cursor.execute('CREATE TABLE TumblrData(ImageTitle TEXT, Image BLOB, SearchString TEXT)')

    def insertwikidata(self, articletitle, summarytext, searchstring):
        with self.connection:
            #insertstring = str.format()
            self.cursor.execute("INSERT INTO WikiData VALUES(?,?,?)",(articletitle,summarytext,searchstring))

    def getrelatedsavedwikiarticle(self, searchstring):
        with self.connection:
            selectstring = str.format('SELECT * FROM WikiData WHERE ArticleTitle = "{0}" OR SearchString = "{0}"', searchstring)
            self.cursor.execute(selectstring)
            wikidata = self.cursor.fetchall()
            return wikidata

    def inserttwitterdata(self, username, tweettext, searchstring):
        with self.connection:
            self.cursor.execute("INSERT INTO TwitterData VALUES(?,?,?)",(username,tweettext,searchstring))

    def getsearchedtweets(self, searchstring):
        with self.connection:
            selectstring = str.format('SELECT * FROM TwitterData WHERE SearchString = "{0}"', searchstring)
            self.cursor.execute(selectstring)
            twitterdata = self.cursor.fetchall()
            return twitterdata