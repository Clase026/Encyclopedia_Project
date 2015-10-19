__author__ = 'anthonyclasen'

from src.Database.EncyclopiaData import *

import wikipedia

class WikipediaSearch:

    def __init__(self, EncyclopediaData, searchstring = 'Wikipedia'):
        self.ED = EncyclopediaData
        self.searchstring = searchstring

    def createarticlefromfirstsearchresult(self):
        searchresults = wikipedia.search(self.searchstring)
        if searchresults != []:
            articletitle = searchresults[0].encode('ascii', 'ignore')
            articlesummary = wikipedia.summary(articletitle).encode('ascii', 'ignore')
            article = WikipediaArticle(articletitle,articlesummary,self.searchstring)
            return article
        else:
            return None

    def saveresult(self, article):
        self.ED.insertwikidata(article.articletitle, article.articlesummary, article.searchstring)

    def getrelatedsavedresults(self):
        savedresults = self.ED.getrelatedsavedwikiarticle(self.searchstring)
        articles = []
        for result in savedresults:
            article = WikipediaArticle(result[0],result[1],result[2])
            articles.append(article)
        return articles

class WikipediaArticle:

    def __init__(self, articletitle, articlesummary, searchstring):
        self.articletitle = articletitle
        self.articlesummary = articlesummary
        self.searchstring = searchstring

    def displayarticle(self):
        displaystring = self.articletitle + '\n' + self.articlesummary
        return displaystring

