from pymel.core import *

TAGGED = set()

def toggle_selected():
    print "Toggling selected objects."
    for obj in ls(sl=True):
        if not obj.hasAttr("BYU_Alembic_Export_Flag"):
            obj.addAttr("BYU_Alembic_Export_Flag", dv=True, at=bool, h=False, k=True)
            TAGGED.add(obj)
        else:
            curval = obj.attr("BYU_Alembic_Export_Flag").get()
            obj.attr("BYU_Alembic_Export_Flag").set(not curval)
            if curval:
                TAGGED.add(obj)
            else:
                TAGGED.remove(obj)
    print "Done"

def hide_not_tagged():
    hide(allObjects=True)
    showHidden(TAGGED)

toggle_selected()
print TAGGED
# hide_not_tagged()

