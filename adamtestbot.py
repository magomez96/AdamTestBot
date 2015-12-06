import requests
import time
import sys
import datetime
import csv
import random
import re
import json
import traceback
import os
import telegram
import gc

import __builtin__ #I'm so sorry
from pydblite import Base #The PyDbLite stuff

import src.atbCommands as atbCommands

APIKEY = ''
with open('../apikey.csv', 'r+') as csvfile: #apikey is not stored on git, sorry
    reader = csv.DictReader(csvfile)
    APIKEY = list(reader)[0]['key']

atb = telegram.Bot(token=APIKEY)

updates = {}
currentMessage = {}

print "@AdamTestBot 2.0 - Ready to go!"
print "Written by Adam Gincel, shoutouts to Smesh, KARMAT, Dank Meme Network, and SG(DC)^2"

newestOffset = 0
networkFailure = True
while networkFailure:
    try:
        updates = atb.getUpdates(offset=newestOffset)
        for u in updates:
            newestOffset = u.update_id
        networkFailure = False
    except Exception:
        print traceback.format_exc()
        print "...",
print "...Connected!"

startTime = datetime.datetime.now()

previousTime = datetime.datetime.now().time();
currentTime = 0;

instanceAge = 0
refreshRate = 0.2
user_id = 0

__builtin__.blazeDB = Base('chatStorage/blaze.pdl') #The path to the database
__builtin__.blazeDB.create('username', 'name', 'counter', 'timestamp', mode="open") #Create a new DB if one doesn't exist. If it does, open it

blacklist = [-23535579, -28477145]

running = True
while running:
    networkFailure = True
    while networkFailure:
        try:
            updates = atb.getUpdates(offset=newestOffset+1)
            for u in updates:
                newestOffset = u.update_id
            networkFailure = False
        except Exception:
            print "...",

    if instanceAge % 10 == 0: #print 1 X every ten ticks
        print "Y"
    else:
        print "X",


    for u in updates:
        currentMessage = u.message
        try:
            user_id = currentMessage.chat.id
            if user_id not in blacklist:
                parsedCommand = re.split(r'[@\s:,\'*]', currentMessage.text.lower())[0]
                running = atbCommands.process(atb, user_id, parsedCommand, currentMessage.text, currentMessage, u, datetime.datetime.now() - startTime)


        except Exception as myException:
            print traceback.format_exc()

    currentTime = datetime.datetime.now().time()

    if previousTime.minute != currentTime.minute:
        if currentTime.hour == 16 and currentTime.minute == 21: #commit Blaze Database
            __builtin__.blazeDB.commit()
        elif currentTime.hour == 16 and currentTime.minute == 22: #TEST
            atb.sendMessage(chat_id=-12788453, text="AUTOMATED")

    previousTime = currentTime


    gc.collect()
    instanceAge += 1
    time.sleep(refreshRate)
