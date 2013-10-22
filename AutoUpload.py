###################################
##  AutoUpload
##  By Matthew Maxson
##  © 2013
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
###################################

import flickrapi
import sys
import time
from xml.etree import ElementTree as ET
import shelve 
import os
import string
import re
from optparse import OptionParser


api_key = 'PutYourAPIKeyHere'
api_secret = 'PutYourAPISecretHere'
MINYEAR = 1900

TheUserID = 'YourUserIDGoesHere'
TheTokenPath = 'c:\\PictureUploader\\flickrtokens'
TheHistoryPath = 'c:\\PictureUploader\\flickrhistory'
RootPathToMonitor = 'PathToSearchForPictures'
DefaultLicense = ''
LogPath = 'c:\\PictureUploader\\Logs\\' + time.strftime('%Y%m%d_%H%M%S')  + "_AutoUpload.log"
DefaultTags = ["AutoUpload", time.strftime('%Y%m%d')]
CurrentSets = {}
Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def addtosets(ThePicID, CurrentSetList, NewSetList):
    
    for set in CurrentSetList:
        writetolog(LogPath, "     Adding To Set = " + set)
        try:
            res = flickr.flickr_call(method='flickr.photosets.addPhoto', photoset_id = set, photo_id = ThePicID)
        except flickrapi.FlickrError as e:
            writetolog(LogPath, "     " + str(e))
        
        writetolog(LogPath, "     " + res.get("stat"))
    for setname in NewSetList:
        writetolog(LogPath, "     Creating Set = " + setname)
        
        try:
            res = flickr.flickr_call(method='flickr.photosets.create', title = setname, primary_photo_id = ThePicID)
        except flickrapi.FlickrError as e:
            writetolog(LogPath, "     " + str(e))
        
        writetolog(LogPath, "     " + res.get("stat"))
    

def getyears(minyear):
    return [str(i) for i in range(minyear, time.localtime().tm_year + 1)]

def walker(startdir, relpath=""):
#written by Alan Monroe
    theresult = ""
    os.chdir(startdir)
    listing = os.listdir(startdir)
    for x in listing:
        if os.path.isfile(x):
            theresult = checkpic(os.path.abspath(x))
            if theresult == "new":
                uploadpic(os.path.abspath(x))
        elif os.path.isdir(x):
            walker(os.path.abspath(x) + os.sep)
            os.chdir(startdir)
        else:
            pass
            
def writetolog(thelogfile, message):
    if os.path.isfile(thelogfile):
        outfile = open(thelogfile, 'a')
    else:
        outfile = open(thelogfile, 'w')
    outfile.write(time.strftime('%m/%d/%Y %H:%M:%S') + ", " + message + "\n")
    outfile.close()
    
def checkpic(TheFile):
    TheReturn = "already done"
    uploaded = shelve.open(TheHistoryPath, writeback=True)
    if (not(uploaded.has_key(TheFile))):
        TheReturn = "new"
    uploaded.close()
    return TheReturn
    
def getsets():
    sets = {}
    rsp = flickr.flickr_call(method='flickr.photosets.getList')
    if rsp.get("stat") == "ok":
        for photosets in rsp:
            for photoset in photosets:
                sets[photoset[0].text.encode('utf8')] = photoset.get("id")
    return sets
    
def uploadpic(TheFile):
    public = 1
    thetags = ""
    publicfound = False
    privatefound = False
    result = ET.fromstring('<res stat="error"></res>')
    errorstring = " with errors"
    picid = 0
    setids = []
    newsets = []
    havemonth = False
    haveyear = False
    themonth = ''
    theyear = ''
    monthyear = ''
    CurrentSets = getsets()
    
    for tag in DefaultTags:
        thetags += " " + tag
    TheSplitPath = string.split(string.replace(TheFile, RootPathToMonitor, ""), "\\")
    for x in TheSplitPath:
        if not x == "":
            thetags += " " + x
            
            if x in Years:
                haveyear = True
                theyear = x
                
            if x in Months:
                havemonth = True
                themonth = x
            
            if not x == TheFile:                
                if x in CurrentSets:
                    setids.append(CurrentSets[x])
                else:
                    if x == "01-Jan":
                        if "January" in CurrentSets:
                            setids.append(CurrentSets["January"])
                            havemonth = True
                            themonth = "January"
                    elif x == "02-Feb":
                        if "February" in CurrentSets:
                            setids.append(CurrentSets["February"])
                            havemonth = True
                            themonth = "February"
                    elif x == "03-Mar":
                        if "March" in CurrentSets:
                            setids.append(CurrentSets["March"])
                            havemonth = True
                            themonth = "March"
                    elif x == "04-Apr":
                        if "April" in CurrentSets:
                            setids.append(CurrentSets["April"])
                            havemonth = True
                            themonth = "April"
                    elif x == "05-May":
                        if "May" in CurrentSets:
                            setids.append(CurrentSets["May"])
                            havemonth = True
                            themonth = "May"
                    elif x == "06-Jun":
                        if "June" in CurrentSets:
                            setids.append(CurrentSets["June"])
                            havemonth = True
                            themonth = "June"
                    elif x == "07-Jul":
                        if "July" in CurrentSets:
                            setids.append(CurrentSets["July"])
                            havemonth = True
                            themonth = "July"
                    elif x == "08-Aug":
                        if "August" in CurrentSets:
                            setids.append(CurrentSets["August"])
                            havemonth = True
                            themonth = "August"
                    elif x == "09-Sep":
                        if "September" in CurrentSets:
                            setids.append(CurrentSets["September"])
                            havemonth = True
                            themonth = "September"
                    elif x == "10-Oct":
                        if "October" in CurrentSets:
                            setids.append(CurrentSets["October"])
                            havemonth = True
                            themonth = "October"
                    elif x == "11-Nov":
                        if "November" in CurrentSets:
                            setids.append(CurrentSets["November"])
                            havemonth = True
                            themonth = "November"
                    elif x == "12-Dec":
                        if "December" in CurrentSets:
                            setids.append(CurrentSets["December"])
                            havemonth = True
                            themonth = "December"
                    else:
                        newsets.append(x)
            
        if x.lower() == "private":
            privatefound = True
    
    if privatefound:
        public = 0
        
    if havemonth and haveyear:
        monthyear = themonth + " " + theyear
        if monthyear in CurrentSets:
            setids.append(CurrentSets[monthyear])
        else:
            newsets.append(monthyear)
        
    writetolog(LogPath, TheFile)
    writetolog(LogPath, "     Starting upload")
    writetolog(LogPath, "     Public = " + str(public))
    writetolog(LogPath, "     Tags = " + thetags)
    
    try:
        result = flickr.upload(filename=TheFile, is_public=public, tags=thetags)
    except flickrapi.FlickrError as e:
        writetolog(LogPath, "     " + str(e))
    
    if result.get("stat") == "ok":
        errorstring = " with no errors"
        uploaded = shelve.open(TheHistoryPath, writeback=True)
        picid = result[0].text
        uploaded[TheFile] = picid
        uploaded.close()
        
        addtosets(picid, setids, newsets)
        CurrentSets = getsets()
    
    writetolog(LogPath, "     Finished upload" + errorstring)

def cleanup():
    sets = {}
    photocount = 0
    writetolog(LogPath, "-----")
    writetolog(LogPath, "The following sets look like files and have 1 image")
    rsp = flickr.flickr_call(method='flickr.photosets.getList')
    if rsp.get("stat") == "ok":
        for photosets in rsp:
            for photoset in photosets:
                photocount = photoset.get("photos")
                if  ((photocount == "1") and (possiblefile(photoset[0].text.encode('utf8')))):
                    writetolog(LogPath, photoset[0].text.encode('utf8') + " http://www.flickr.com/me/sets/" + photoset.get("id"))
                    DeleteSet(photoset.get("id"))                    
        writetolog(LogPath, "-----")
        writetolog(LogPath, "The following sets look like files and have multiple images.  POSSIBLE DUPLICATES")
        for photosets in rsp:
            for photoset in photosets:
                photocount = photoset.get("photos")
                if  ((photocount != "1") and (possiblefile(photoset[0].text.encode('utf8')))):
                    writetolog(LogPath, photoset[0].text.encode('utf8') + " http://www.flickr.com/me/sets/" + photoset.get("id"))

def DeleteSet(SetID):
    writetolog(LogPath, "Attempting to Delete " + SetID)
    rsp = flickr.flickr_call(method='flickr.photosets.delete', photoset_id=SetID)
    if rsp.get("stat") == "ok":
        writetolog(LogPath, "Deleted")
    else:
        writetolog(LogPath, "Not Deleted")
                
def possiblefile(TheName):
    thereturn = False
    regex = re.compile(r"[a-zA-Z0-9_]*[\.][a-zA-Z]{3}")
    if regex.match(TheName):
        thereturn = True
    return thereturn
    
    
Years = getyears(MINYEAR)
flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.token.path = TheTokenPath
(token, frob) = flickr.get_token_part_one(perms='write')
if not token: 
    raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

CurrentSets = getsets()
walker(RootPathToMonitor)
cleanup()