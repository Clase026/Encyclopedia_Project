__author__ = '?'

from src.Logic.Wikipedia import *
from src.Logic.Twitter import *

def main():

    DB = EncyclopediaData()
    DB.recreatetables()
    WikiSearch = WikipediaSearch(DB,"Wikipedia")
    articles = None
    if WikiSearch.getrelatedsavedresults() == []:
        article = WikiSearch.createarticlefromfirstsearchresult()
        WikiSearch.saveresult(article)
        articles = [article]
    else:
        articles = WikiSearch.getrelatedsavedresults()
    for article in articles:
        print article.displayarticle()
    CatSearch = TwitterSearch(DB,"@Cat")
    statuses = None
    if CatSearch.getrelatedsavedtweets() == []:
        statuses = CatSearch.dosearch()
    else:
        statuses = CatSearch.getrelatedsavedtweets()
    for status in statuses:
        print status.displaytweet()


main()