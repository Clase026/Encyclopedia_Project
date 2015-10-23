__author__ = 'anthonyclasen'

from src.Database.EncyclopiaData import *

import wikipedia

class WikipediaSearch:

    def __init__(self, EncyclopediaData, searchstring = 'Wikipedia'):
        self.ED = EncyclopediaData
        self.searchstring = searchstring

    def createarticlefromfirstsearchresult(self):
        """Takes the first search result for the searchstring, and returns a wikipediaarticle"""
        try:
            searchresults = wikipedia.search(self.searchstring)
            if searchresults != []:
                articletitle = searchresults[0].encode('ascii', 'ignore')
                articlesummary = wikipedia.summary(articletitle).encode('ascii', 'ignore')
                article = WikipediaArticle(articletitle,articlesummary,self.searchstring)
                return article
        except:
            article = WikipediaArticle("Disambiguation Error", "Please revise your request", "")
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
            article = self.createarticlefromfirstsearchresult()
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

