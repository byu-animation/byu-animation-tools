import checkin_Nuke as ci
import checkout_Nuke as co

def checkout():
    # nuke.message('check out')
    co.go()

def checkin():
    # nuke.message('check in')
    ci.go()

def rollback():
    nuke.message('rollback')

nuke.menu( 'Nuke' ).addCommand( 'Owned/check out', 'checkout()')
nuke.menu( 'Nuke' ).addCommand( 'Owned/check in', 'checkin()')
nuke.menu( 'Nuke' ).addCommand( 'Owned/rollback', 'rollback()')


