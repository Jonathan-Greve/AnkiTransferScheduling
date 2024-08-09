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

import anki.notes
from anki.hooks import addHook
from anki.importing.anki2 import Anki2Importer
from anki.lang import _
from anki.utils import int_time, guid64
from aqt import QAction, QKeySequence, mw
from aqt.utils import showWarning, tooltip, showInfo
from aqt.qt import debug # use debug() to get access to the terminal debugger
# though I could not get access to any useful variable of the environment...
import time

# load the config.json where the parameters are stored
global config
config = mw.addonManager.getConfig(__name__)

# To provide context to all tooltips
global header
header = "Scheduling data transfer : "

def truncateString(string, maxSize = 17) :
    """Truncates strings which are too long."""
    if len(string) > maxSize :
        return(string[0:maxSize-1] + "...")
    else :
        return(string)

def severalCid(cids) :
    """Tests wether several cards are selected."""
    try  :
        cids[0]
    except :
        tooltip(header + """please select one card.""")
        return True
        
    if len(cids) > 1 : # refuse to store if several cards are selected
        tooltip(header + """please select only one card.""")
        return True

def transferFrom(browser):
    """Store the cid of the first card from which to take scheduling data."""
    if browser.table.is_notes_mode() :
        tooltip(header + """please toggle the card mode instead of the note mode.""")
        return
    cids = browser.selectedCards()
    print("selected cards : " + str(cids))
    if severalCid(cids) : return
    global cid1 # global variable so that it is reachable in transferTo()
    cid1 = cids[0] # if several though it was already checked
    old = mw.col.get_note(mw.col.get_card(cid1).nid).fields[0] # get the first field of the related note
    tooltip("""Data transfered from {}.""".format(truncateString(old)))

def transferTo(browser):
    """Transfer scheduling data to the second card if transferFrom has already been used."""
    global cid1 #needed

    cids = browser.selectedCards()

    # Make a few checks
    if severalCid(cids) : return  # refuse the transfer if several cards are selected
    cid2 = cids[0]
    
    try :
        cid1 # must exist
    except :
        tooltip(header + """please first select a card to take the data from ({}).""".format(config['Shortcut : Copy']))
        return
    if cid1 == cid2 :
        tooltip(header + """please select a different card.""")
        return

    # Old way of making the action undoable (before Anki 23.10) :
    #browser.mw.checkpoint(_("Transfer data")) # everything between beginReset() and endReset() will be named "Transfer data" and will be reversible with CTRL+ALT+Z
    #browser.model.beginReset()
    
    card2 = mw.col.get_card(cid2)
    card1 = mw.col.get_card(cid1)
    note2 = mw.col.get_note(card2.nid)
    note1 = mw.col.get_note(card1.nid)
    print("Old card : " + str(cid1) + ", new card : " + str(cid2))

    # Transfer all attributes from the old card to the new card
    # Previously used SQL commands with .checkpoint() but this way was deprecated
    if config["Change deck"] == "Yes" :
        #mw.col.db.execute("update cards set did = ? where id = ?", old.did, cid1)
        #mw.col.db.execute("update cards set odid = ? where id = ?", old.odid, cid1)
        card2.did = card1.did
        card2.odid = card1.odid
    card2.due = card1.due
    card2.factor = card1.factor
    card2.flags = card1.flags
    card2.ivl = card1.ivl
    card2.lapses = card1.lapses
    card2.left = card1.left
    card2.mod = card1.mod
    card2.usn = -1
    card2.odue = card1.odue
    card2.reps = card1.reps
    card2.queue = card1.queue
    card2.type = card1.type

    # Effective update
    mw.col.update_card(card2)

    # We will give the cid of the old card to the new card, in order to transfer the reviews of revlog
    # 1) we free the cid by giving the the old card a different one
    # the following will try to give a new cid to the old card as long as it fails (because of unique cid constraint)
    # cid is the epoch milliseconds date of the card creation so changing it by up to 100 will not make a big difference
    #cid1 = 1429369872289
    i = 0
    #liste = mw.col.db.list("select id from revlog where cid = ?", 111)
    while True :
        i += 1
        try :
            # first check that the cid is not used in the revlog (possibly by a deleted card)
            # if it was used by a deleted card, it would not fail the sqlite3.Intregrity test
            # but it would put the history of the deleted card on the old card, which is not acceptable
            liste = mw.col.db.list("select id from revlog where cid = ?", cid1+i)
            print("Trying to free cid " + str(cid1) + " (attempt " + str(i) + "), checking if cid " + str(cid1+i) + " has reviews : " + str(liste))
            if len(liste) > 0 :
                raise
            mw.col.db.execute("update cards set id = ? where id = ?", cid1+i, cid1) # will fail if the cid is already taken
            print("Free " + str(cid1) + " by giving old card the id " + str(cid1+i))
            break
        except : #sqlite3.IntegrityError :
            pass

    # 2) now that the cid is free, we can give it to the new card
    mw.col.db.execute("update cards set id = ? where id = ?", cid1, cid2) # TODO UPDATE
    print("Put " + str(cid1) + " as the new id of the new card")

    ### on notes :
    mw.col.db.execute("update notes set usn = -1 where id = ?", card2.nid) # -1 to force sync, TODO UPDATE

    #### delete the old note if it is required
    if config["Delete old card"] == "Yes" :
        mw.col.db.execute("delete from notes where id = ?", card1.nid) # SQL instead of mw.col.remNotes() # TODO UPDATE
        mw.col.db.execute("delete from cards where nid = ?", card1.nid) # SQL instead of mw.col.remNotes() # TODO UPDATE

    ### on the collection :
    epoch = str(time.time()).replace(".", "")[0:13]
    mw.col.db.execute("update col set mod = ?", epoch) # update modification time of the collection
    ##mw.col.db.execute("update col set usn = -1") # -1 to force sync BEWARE this line broke sync after a certain version of anki, see https://forums.ankiweb.net/t/syncing-with-ankiweb-downloads-entire-deck-when-change-is-made-in-local-deck/1868/4

    ## Refresh the browser
    browser.search() # necessary to refresh data of the table but loses the
    #browser.model.focusedCard = cid1 # OBSOLETE put the selector on card2 which has now cid1 # TODO UPDATE
    #browser.editor.card = mw.col.get_card(cid1) # not working
    #browser.model.focusedCard = mw.col.get_card(cid1)
    #browser.editor.loadNote(focusTo=0)
    #browser.table.to_last_row() # works to reach the last row of the table
    #:wbrowser.on

    ## Success message :
    txt1 = truncateString(note1.fields[0])
    txt2 = truncateString(note2.fields[0])
    tooltip("""Data transfered from {} to {}.""".format(txt1, txt2))

    ## Delete cid1
    ## to avoid a second transfer of the same data, which would be a mistake
    del cid1

    ##browser.model.endReset()
    ##browser.mw.requireReset()

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
