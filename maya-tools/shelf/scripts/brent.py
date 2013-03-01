import maya.cmds as cmds
import random
import os

def getQuote():
        with open(os.path.join(os.environ['MAYA_SHELF_DIR'], 'scripts', 'brent_quotes.txt'), 'r') as f:
                quotes = f.readlines()
        f.closed
        index = random.randint(0, len(quotes)-1)
        quote = quotes[index]
        quote = quote.replace('\n', '')
        if quote.isspace():
                quote = "We're in finish mode. Kay?"
        return quote

def speak_brent():

	cmds.confirmDialog(  title     = 'Speak Brent!'
                       , message       = getQuote()
                       , button        = ['Ok']
                       , defaultButton = 'Ok'
                       , cancelButton  = 'Ok'
                       , dismissString = 'Ok')

## The shelf will call this method each time
## the button is pressed. If you want something
## to run each time, put it here.
def go():
    speak_brent()
