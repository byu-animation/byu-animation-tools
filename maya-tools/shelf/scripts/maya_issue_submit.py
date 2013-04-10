import webbrowser
import os

def go():
	webbrowser.open( os.environ['ISSUE_URL'] )