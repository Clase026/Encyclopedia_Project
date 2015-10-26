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
        # Search box and button frame
        self.topFrame = Frame()# test frame
        self.topFrame.grid(row=1, column=0, pady=5) # test grid

        # Images frame
        self.sideFrame = Frame()
        self.sideFrame.grid(row=1, column=1, padx=5)

        # Label(self.topFrame, text = "test").grid(row=0,column=0) # test label
        self.DB = EncyclopediaData()
        self.DB.createtables()
        self.grid()
        self.master.title("Encyclopedia")
        #add search field
        self.txtsearchquery = Entry(self.topFrame, bg="white", width=30)
        self.txtsearchquery.grid(row=0,column=0)
        # self.txtsearchquery = Entry(self, bg="cyan", width=50)
        # self.txtsearchquery.grid(row=0, column=0)

        #add search button
        self.btnSearch = Button(self.topFrame, text="Search", command=self.clickSearch).grid(row=0, column=1, sticky=W+S)
        # self.btnSearch["text"] = "Search"
        # self.btnSearch["command"] = self.clickSearch
        # self.btnSearch.grid(row=0, column=1, sticky=W+S)

        # Wiki Label
        self.wikiLabel = Label(self, text="Wikipedia Summary")
        self.wikiLabel.grid(row=1, column=0)

        #add wiki textbox
        self.wikitext = Text(self)
        self.wikitext["height"] = 20
        self.wikitext["width"] = 100
        self.wikitext.grid(row=2, column=0)
        self.wikiscroll1 = Scrollbar(self, orient=VERTICAL)
        self.wikiscroll1.grid(row=2, column=1)
        self.wikiscroll1.config(command=self.wikitext.yview)
        # self.wikiscroll2 = Scrollbar(self, orient=HORIZONTAL)
        # self.wikiscroll2.grid(row=2,column=0)
        # self.wikiscroll2.config(command=self.wikitext.xview)

        # add image frame
        self.imageLabel = Label(self.sideFrame, text="Photo Example")
        self.imageLabel.grid(row=2, column=2)
        self.image = PhotoImage(self.sideFrame, width=40)
        # self.image.grid(row=2, column= 1)

        # twitter label
        self.label = Label(self, text="Twitter Posts")
        self.label.grid(row=3, column=0)
        #add twitter textbox
        self.twittertext = Text(self, wrap = NONE)
        self.twittertext["height"] = 20
        self.twittertext["width"] = 140
        self.twittertext.grid(row=4,column=0)
        self.twitteryscroll = Scrollbar(self, orient=VERTICAL)
        self.twitteryscroll.grid(row=4,column=1)
        self.twitteryscroll.config(command=self.twittertext.yview)
        # self.twitterscroll2 = Scrollbar(self, orient=HORIZONTAL)
        # self.twitterscroll2.grid(row=2,column=2)
        # self.twitterscroll2.config(command=self.twittertext.xview)
        #add quit button
        self.btnQuit = Button(self)
        self.btnQuit["text"] = "QUIT"
        self.btnQuit["fg"]   = "red"
        self.btnQuit["command"] =  self.clickQuitApp
        self.btnQuit.grid(row=5, column=0, sticky=W+S)

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

        try:
            for i, status in enumerate(statuses):
                tweetsarray.append(("\n"+"Tweet "+str(i+1)+status.displaytweet()) + "\n")
        except Exception, e:
            print("AttributeError: "+str(e))

        for i in tweetsarray:
            self.twittertext.insert(END,i)
    def clickQuitApp(self):
        self.quit()