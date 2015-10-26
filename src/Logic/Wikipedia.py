__author__ = 'anthonyclasen'

from src.Database.EncyclopiaData import *

import wikipedia

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
        print title
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

