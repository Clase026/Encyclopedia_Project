__author__ = 'anthonyclasen'

import sqlite3

class EncyclopediaData:
    """Holds stored data from wikipedia, tumblr, and twitter"""

    def __init__(self):
        self.connection = None
        self.connection = sqlite3.connect('EncyclopediaData')
        self.cursor = self.connection.cursor()

    def recreatetables(self):
        with self.connection:
            self.cursor.execute('DROP TABLE IF EXISTS WikiData')
            self.cursor.execute('CREATE TABLE WikiData(ArticleTitle TEXT, SummaryText TEXT, SearchString TEXT)')
            self.cursor.execute('DROP TABLE IF EXISTS TwitterData')
            self.cursor.execute('CREATE TABLE TwitterData(UserName TEXT, TweetText TEXT, LinkData BLOB)')
            self.cursor.execute('DROP TABLE IF EXISTS TumblrData')
            self.cursor.execute('CREATE TABLE TumblrData(ImageTitle TEXT, Image BLOB, SearchString TEXT)')

    def insertwikidata(self, articletitle, summarytext, searchstring):
        with self.connection:
            insertstring = str.format('INSERT INTO WikiData VALUES("{0}","{1}","{2}")',articletitle,summarytext,searchstring)
            self.cursor.execute(insertstring)

    def getallwikidata(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM WikiData')
            wikidata = self.cursor.fetchall()
            return wikidata

    def getspecificwikiarticle(self, searchstring):
        with self.connection:
            selectstring = str.format('SELECT * FROM WikiData WHERE ArticleTitle = "{0}" OR SearchString = "{0}"', searchstring)
            self.cursor.execute(selectstring)
            wikidata = self.cursor.fetchall()
            for article in wikidata:
                print article[0]
            return wikidata

#Testing
#ED = EncyclopediaData()
#ED.recreatetables()
#ED.insertwikidata('Article Title','The text of an article','The Search string used to find this article')
#ED.insertwikidata('Second Article','The text of the second article','The Search string used to find this article')
#ED.insertwikidata('Third Article','The text of the third article','The Search string used to find this article')
#ED.getallwikidata()
#ED.getspecificwikiarticle('Second Article')