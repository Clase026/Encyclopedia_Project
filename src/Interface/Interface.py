__author__ = '?'
#http://effbot.org/tkinterbook/tkinter-index.htm
#http://stackoverflow.com/que# stions/6129899/python-multiple-frames-with-grid-manager
from Tkinter import *
from src.Logic.Wikipedia import *
from src.Logic.Twitter import *
from src.Logic.Imgur import *
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
        # search bar and search button
        self.TopFrame = Frame(self)
        self.TopFrame.grid(row=0,column=1)
        # Side Panel for image urls
        self.sideFrame = Frame(self)
        self.sideFrame.grid(row=1,column=0)
        # Main Frame panel for twitter and wikipedia
        self.mainFrame = Frame(self)
        self.mainFrame.grid(row=1,column=1)
        #add search field
        self.txtsearchquery = Entry(self.TopFrame, bg="cyan", width=30)
        self.txtsearchquery.grid(row=0, column=0)
        #add search button
        self.btnSearch = Button(self.TopFrame)
        self.btnSearch["text"] = "Search"
        self.btnSearch["command"] = self.clickSearch
        self.btnSearch.grid(row=0, column=1, sticky=W+S)
        # add image url box
        self.urlText = Text(self.sideFrame)
        self.urlText["height"]= 30
        self.urlText["width"]=20
        self.urlText.grid(row=0,column=0)
        self.urlTextScroll = Scrollbar(self.sideFrame, orient=VERTICAL)
        self.urlTextScroll.grid(row=0,column=1)
        self.urlTextScroll.config(command=self.urlText.yview)
        #add wiki textbox
        self.wikitext = Text(self.mainFrame)
        self.wikitext["height"] = 20
        self.wikitext["width"] = 100
        self.wikitext.grid(row=0, column=0)
        self.wikiscroll = Scrollbar(self.mainFrame, orient=VERTICAL)
        self.wikiscroll.grid(row=0, column=1)
        self.wikiscroll.config(command=self.wikitext.yview)
        #add twitter textbox
        self.twittertext = Text(self.mainFrame, wrap = NONE)
        self.twittertext["height"] = 10
        self.twittertext["width"] = 100
        self.twittertext.grid(row=1,column=0)
        self.twitteryscroll = Scrollbar(self.mainFrame, orient=VERTICAL)
        self.twitteryscroll.grid(row=1,column=1)
        self.twitteryscroll.config(command=self.twittertext.yview)
        #add quit button
        self.btnQuit = Button(self.TopFrame)
        self.btnQuit["text"] = "QUIT"
        self.btnQuit["fg"]   = "red"
        self.btnQuit["command"] =  self.clickQuitApp
        self.btnQuit.grid(row=0, column=2, sticky=W+S)

    def clickSearch(self):
        """Does a wiki and twitter search for the user's input, and then outputs the data to the two textboxes.
        Checks database first to see if there are any matching records before going to the APIs
        """
        self.searchquery = self.txtsearchquery.get()
        self.imgurResults()
        self.wikiResults()
        self.twitterResults()

    def clickQuitApp(self):
        self.quit()
    def twitterResults(self):
        # twitter results
        self.twittertext.config(state = NORMAL)
        self.twittertext.delete("1.0",END)
        twittersearch = TwitterSearch(self.DB,self.searchquery)
        statuses = twittersearch.searchorloadtweets()
        tweetsstring = ""
        for status in statuses:
            tweetsstring += "\n"+status.displaytweet() + "\n"
        self.twittertext.insert(END,tweetsstring)
        self.twittertext.config(state = DISABLED)

    def wikiResults(self):
        try:
            # wikipedia results
            self.wikitext.config(state = NORMAL)
            self.wikitext.delete("1.0",END)
            wikisearch = WikipediaSearch(self.DB,self.searchquery)
            articles = wikisearch.searchorloadarticle()
            self.wikitext.insert(END,articles[0].displayarticle())
            self.wikitext.config(state = DISABLED)
        except Exception:
            print("Wikipedia results failed to load.")
            print(Exception)

    def imgurResults(self):
        try:
            # Imgur results
            self.urlText.config(state = NORMAL)
            self.urlText.delete("1.0",END)
            imgr = ImgurSearch(self.searchquery)
            gifurls = imgr.dosearch()
            gifs = ""
            for gif in gifurls:
                gifs += "\n"+str(gif)+"\n"
            self.urlText.insert(END, gifs)
            self.urlText.config(state = DISABLED)
        except Exception:
            print("Imgur results failed to load")
            print(Exception)