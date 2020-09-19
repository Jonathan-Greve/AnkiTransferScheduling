# -*- coding: utf-8 -*-
# Copyright: Samuel Allain
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Transfer scheduling data and properties from one card to another,
# useful to merge two notes in one notes with two cards.

"""
In the browser,
 1. select the first card (from which data have to be taken), then go in "Cards" > "Scheduling data : Transfer from" (or Ctrl+Alt+C)
 2. select the second card (to which data have to be transfered), then go in "Cards" > "Scheduling data : Transfer from" (or Ctrl+Alt+V)
Shortcuts are customizable in config.json. Auto-deletion after the transfer can also be set in config.json.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import anki.notes
from anki.hooks import addHook
from anki.importing.anki2 import Anki2Importer
from anki.lang import _
from anki.utils import intTime, guid64
from aqt import mw
from aqt.utils import showWarning, tooltip, showInfo
from aqt.qt import *
import time

# load the config.json where the parameters are stored
global config
config = mw.addonManager.getConfig(__name__)

global header
header = "Scheduling data transfer : "

# function which truncates too long strings
def truncateString(string, maxSize = 17) :
    if len(string) > maxSize :
        return(string[0:maxSize-1] + "...")
    else :
        return(string)

# tests wheter several cards are selected
def severalCid(cids) :
    try  :
        cids[0]
    except :
        tooltip(_(header + """please select one card."""))
        return True
        
    if len(cids) > 1 : # refuse to store if several cards are selected
        tooltip(_(header + """please select only one card."""))
        return True


# Store the cid of the first card
def transferFrom(browser):
    cids = browser.selectedCards()
    if severalCid(cids) : return
    global cid1 # global variable so that it is reachable in transferTo() 
    cid1 = cids[0] # if sever
    old = mw.col.getNote(mw.col.getCard(cid1).nid).fields[0] # get the first field of the related note
    tooltip(_("""Data transfered from {}.""".format(truncateString(old))))

def transferTo(browser):
    global cid1 #needed

    cids = browser.selectedCards()

    # Make a few checks
    if severalCid(cids) : return  # refuse the transfer if several cards are selected
    cid2 = cids[0]
    
    try :
        cid1 # must exist
    except :
        tooltip(_(header + """please first select a card to take the data from ({}).""".format(config['Shortcut : Copy'])))
        return
    if cid1 == cid2 :
        tooltip(_(header + """please select a different card."""))
        return

    browser.mw.checkpoint(_("Transfer data")) # everything between beginReset() and endReset() will be named "Transfer data" and will be reversible with CTRL+ALT+Z
    browser.model.beginReset()
    
    new = mw.col.getCard(cid2)
    old = mw.col.getCard(cid1)
    new_note = mw.col.getNote(new.nid)
    old_note = mw.col.getNote(old.nid)

    # the following will try to give a new cid to the old card as long as it fails (because of unique cid constraint)
    # cid is the epoch milliseconds date of the card creation so changing it by up to 100 will not make a big difference
#    i = 0
#    while True :
#        i += 1
#        try :
#            mw.col.db.execute("update cards set id = ? where id = ?", cid1-i, cid1) 
#            break
#        except : #sqlite3.IntegrityError :
#            pass

    #cid1 = 1429369872289
    i = 0
    #liste = mw.col.db.list("select id from revlog where cid = ?", 111)
    while True :
        i += 1
        try :
            # first check that the cid is not used in the revlog (possibly by a deleted card)
            # if it was used by a deleted card, it would not fail the sqlite3.Intregrity test
            # but it would put the history of the deleted card on the old card, which is not acceptable
            liste = mw.col.db.list("select id from revlog where cid = ?", cid1-i)
            if len(liste) > 0 : 
                raise 
            mw.col.db.execute("update cards set id = ? where id = ?", cid1-i, cid1) # will fail if the cid is already taken
            break
        except : #sqlite3.IntegrityError :
            pass


    # Transfer all data from the old to the new
    # all those operations could be done with the anki python commands and then using flush()
    # those commands eventually rely on SQL commands which are easier
    ## on cards :
    mw.col.db.execute("update cards set id = ? where id = ?", cid1, cid2)
    if config["Change deck"] == "Yes" :
        mw.col.db.execute("update cards set did = ? where id = ?", old.did, cid1)
        mw.col.db.execute("update cards set odid = ? where id = ?", old.odid, cid1)

    mw.col.db.execute("update cards set due = ? where id = ?", old.due, cid1)
    mw.col.db.execute("update cards set factor = ? where id = ?", old.factor, cid1)
    mw.col.db.execute("update cards set flags = ? where id = ?", old.flags, cid1)
    mw.col.db.execute("update cards set ivl = ? where id = ?", old.ivl, cid1)
    mw.col.db.execute("update cards set lapses = ? where id = ?", old.lapses, cid1)
    mw.col.db.execute("update cards set left = ? where id = ?", old.left, cid1)
    mw.col.db.execute("update cards set mod = ? where id = ?", old.mod, cid1)
    mw.col.db.execute("update cards set usn = -1 where id = ?", cid1) # -1 to force sync
    mw.col.db.execute("update cards set odue = ? where id = ?", old.odue, cid1)
    mw.col.db.execute("update cards set reps = ? where id = ?", old.reps, cid1)
    mw.col.db.execute("update cards set queue = ? where id = ?", old.queue, cid1)
    mw.col.db.execute("update cards set type = ? where id = ?", old.type, cid1)

    ## on notes :
    mw.col.db.execute("update notes set usn = -1 where id = ?", new.nid) # -1 to force sync

    ### delete the old note if it is required
    if config["Delete old card"] == "Yes" :
        mw.col.db.execute("delete from notes where id = ?", old.nid) # SQL instead of mw.col.remNotes()
        mw.col.db.execute("delete from cards where nid = ?", old.nid) # SQL instead of mw.col.remNotes()

    ## on the collection :
    epoch = str(time.time()).replace(".", "")[0:13]
    mw.col.db.execute("update col set mod = ?", epoch) # update modification time of the collection
    #mw.col.db.execute("update col set usn = -1") # -1 to force sync BEWARE this line broke sync after a certain version of anki, see https://forums.ankiweb.net/t/syncing-with-ankiweb-downloads-entire-deck-when-change-is-made-in-local-deck/1868/4

    # Refresh the browser
    browser.search()
    browser.model.focusedCard = cid1 # put the selector on card2 which has now cid1

    # Success message :
    nom1 = truncateString(old_note.fields[0])
    nom2 = truncateString(new_note.fields[0])
    tooltip(_("""Data transfered from {} to {}.""".format(nom1, nom2)))

    # Delete cid1
    # to avoid a second transfer of the same data, which would be a mistake
    del cid1 

    browser.model.endReset()
    browser.mw.requireReset()

def setupMenu(browser):
    # 2 actions
    a = QAction("Scheduling data : Transfer from", browser)
    b = QAction("Scheduling data : Transfer to", browser)
    
    # Add shortcuts
    a.setShortcut(QKeySequence(config['Shortcut : Copy']))
    b.setShortcut(QKeySequence(config['Shortcut : Paste']))

    # Connect the actions to functions
    a.triggered.connect(lambda : transferFrom(browser))
    b.triggered.connect(lambda : transferTo(browser))

    # Add actions to the Cards menu
    browser.form.menu_Cards.addSeparator() # separation line
    browser.form.menu_Cards.addAction(a)
    browser.form.menu_Cards.addAction(b)


# Hook
addHook("browser.setupMenus", setupMenu)
