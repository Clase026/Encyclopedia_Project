__author__ = '?'
#http://effbot.org/tkinterbook/tkinter-index.htm
#http://stackoverflow.com/que# stions/6129899/python-multiple-frames-with-grid-manager
from Tkinter import *
from src.Logic.Wikipedia import *
from src.Logic.Twitter import *
from src.Database.EncyclopiaData import *
from thread import *

class Interface(Frame):

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
        self.wikitext["height"] = 10
        self.wikitext["width"] = 50
        self.wikitext.grid(row=1, column=0)
        self.wikiscroll = Scrollbar(self, orient=VERTICAL)
        self.wikiscroll.grid(row=1, column=1)
        self.wikiscroll.config(command=self.wikitext.yview)
        #add twitter textbox
        self.twittertext = Text(self, wrap = NONE)
        self.twittertext["height"] = 10
        self.twittertext["width"] = 100
        self.twittertext.grid(row=1,column=2)
        self.twitteryscroll = Scrollbar(self, orient=VERTICAL)
        self.twitteryscroll.grid(row=1,column=3)
        self.twitteryscroll.config(command=self.twittertext.yview)
        #self.twitterxscroll = Scrollbar(self, orient=HORIZONTAL)
        #self.twitterxscroll.grid(row=2,column=2)
        #self.twitterxscroll.config(command=self.twittertext.xview)
        #add quit button
        self.btnQuit = Button(self)
        self.btnQuit["text"] = "QUIT"
        self.btnQuit["fg"]   = "red"
        self.btnQuit["command"] =  self.clickQuitApp
        self.btnQuit.grid(row=2, column=0, sticky=W+S)

    def clickSearch(self):
        self.wikitext.delete("1.0",END)
        self.twittertext.delete("1.0",END)
        self.searchquery = self.txtsearchquery.get()
        wikisearch = WikipediaSearch(self.DB,self.searchquery)
        articles = wikisearch.searchorloadarticle()
        self.wikitext.insert(END,articles[0].displayarticle())
        twittersearch = TwitterSearch(self.DB,self.searchquery)
        statuses = twittersearch.searchorloadtweets()
        tweetsstring = ""
        for status in statuses:
            tweetsstring += (status.displaytweet()) + "\n"

        self.twittertext.insert(END,tweetsstring)

    def clickQuitApp(self):
        self.quit()
