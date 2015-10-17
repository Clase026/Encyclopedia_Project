__author__ = 'anthonyclasen'

from src.Database.EncyclopiaData import *

import wikipedia

class Wikipedia:

    def __init__(self):
        self.ED = EncyclopediaData()

    def getsearchresults(self,searchstring):
        searchresults = wikipedia.search(searchstring)
        return searchresults

    def getfirstresultsummary(self,searchresults):
        firstresult = searchresults[0]
        summary = wikipedia.summary(firstresult)
        return summary

    def saveresult(self,articletitle,searchstring):
        articlesummary = wikipedia.summary(articletitle)
        self.ED.insertwikidata(articletitle,articlesummary,searchstring)

    def getrelatedsavedresults(self,searchstring):
        return self.ED.getspecificwikiarticle(searchstring)

    def getsearchhistory(self):
        allwikidata = self.ED.getallwikidata()
        searchhistory = []
        for articledata in allwikidata:
            searchhistory.append(articledata[2])
        print searchhistory
        return searchhistory

#Wiki = Wikipedia()
#Wiki.ED.recreatetables()
#firstresult = Wiki.getsearchresults("Freedom")[0]
#Wiki.saveresult(firstresult,"Freedom")
#Wiki.getsearchhistory()
