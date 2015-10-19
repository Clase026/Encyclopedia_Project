__author__ = '?'

from src.Logic.Wikipedia import *
from src.Logic.Twitter import *
from src.Logic.Imgur import *
from src.Interface.Interface import *

def main():

    root = Tk()
    app = Interface(root)
    app.mainloop()
    app.destroy()
    root.destroy()

main()