import sys, os, glob
import utilities as amu
import nuke

def checkin():
    filePath = nuke.callbacks.filenameFilter( nuke.root().name() )
    save = nuke.scriptSave()
    if save==True:
        toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
        if amu.canCheckin(toCheckin):
            dest = amu.checkin(toCheckin, False)
            nuke.message('Checkin Successful!')
            nuke.scriptClose()
        else:
            nuke.message('Can not check in')

def go():
    checkin()
