__author__ = '?'
#http://effbot.org/tkinterbook/tkinter-index.htm
#http://stackoverflow.com/que# stions/6129899/python-multiple-frames-with-grid-manager
from Tkinter import *
from src.Logic.Wikipedia import *
from src.Logic.Twitter import *
from src.Database.EncyclopiaData import *
from thread import *

class Interface(Frame):
    """A one screen Tkinter GUI used to interact with the encyclopedia"""
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.DB = EncyclopediaData()
        self.DB.createtables()
        self.grid()
        self.master.title("Encyclopedia")
        #add search field
        self.txtsearchquery = Entry(self, bg="cyan", width=50)
        self.txtsearchquery.grid(row=0, column=0)
        #add search button
        self.btnSearch = Button(self)
        self.btnSearch["text"] = "Search"
        self.btnSearch["command"] = self.clickSearch
        self.btnSearch.grid(row=0, column=1, sticky=W+S)
        #add wiki textbox
        self.wikitext = Text(self)
        self.wikitext["height"] = 20
        self.wikitext["width"] = 50
        self.wikitext.grid(row=1, column=0)
        self.wikiscroll = Scrollbar(self, orient=VERTICAL)
        self.wikiscroll.grid(row=1, column=1)
        self.wikiscroll.config(command=self.wikitext.yview)
        #add twitter textbox
        self.twittertext = Text(self, wrap = NONE)
        self.twittertext["height"] = 20
        self.twittertext["width"] = 100
        self.twittertext.grid(row=1,column=2)
        self.twitteryscroll = Scrollbar(self, orient=VERTICAL)
        self.twitteryscroll.grid(row=1,column=3)
        self.twitteryscroll.config(command=self.twittertext.yview)
        #add quit button
        self.btnQuit = Button(self)
        self.btnQuit["text"] = "QUIT"
        self.btnQuit["fg"]   = "red"
        self.btnQuit["command"] =  self.clickQuitApp
        self.btnQuit.grid(row=2, column=0, sticky=W+S)

    def clickSearch(self):
        """Does a wiki and twitter search for the user's input, and then outputs the data to the two textboxes.
        Checks database first to see if there are any matching records before going to the APIs
        """
        self.wikitext.delete("1.0",END)
        self.twittertext.delete("1.0",END)
        self.searchquery = self.txtsearchquery.get()
        wikisearch = WikipediaSearch(self.DB,self.searchquery)
        articles = wikisearch.searchorloadarticle()
        self.wikitext.insert(END,articles[0].displayarticle())
        twittersearch = TwitterSearch(self.DB,self.searchquery)
        statuses = twittersearch.searchorloadtweets()
        tweetsarray = []
        for status in statuses:
            tweetsarray.append(("\n"+status.displaytweet()) + "\n")
        for i in tweetsarray:
            self.twittertext.insert(END,i)
    def clickQuitApp(self):
        self.quit()
