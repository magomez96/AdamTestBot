#All community-made commands should go here. Write your command
#and make a pull request, and I'll try to implement it. I'll
#provide some examples here. Otherwise check out atbCommands.py
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
import psutil
import telegram

from .. import atbSendFunctions as atbSendFunctions
from .. import atbMiscFunctions as atbMiscFunctions

from pydblite import Base #The PyDbLite stuff
import builtins

#If you make your own python files for processing data, put them
#In the community folder and import them here:


####

chatInstanceArray = {}

def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        if not chatInstanceArray[chat_id]['adminDisable']:
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName):
        atbSendFunctions.sendPhoto(bot, chat_id, "images/" + imageName)

    def sendSticker(stickerName):
        atbSendFunctions.sendSticker(bot, chat_id, "stickers/" + stickerName)

    def passSpamCheck():
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date)

    try:
        chatInstanceArray[chat_id]['checking'] = True
    except Exception:
        chatInstanceArray[chat_id] = {'checking': True, 'adminDisable': False, 'spamTimestamp': 0, 'shottyTimestamp': 0, 'shottyWinner': "", 'checkingVehicles': False, 'whoArray': []}

    try:
        #commands go here, in this if-elif block. Python doesn't have switch statements.
        if parsedCommand == "/mom": #sends "MOM GET THE CAMERA"
            sendText("MOM GET THE CAMERA")

        elif atbMiscFunctions.isMoom(parsedCommand): #sends M {random number of Os} M
            if passSpamCheck(): #use this to prevent spamming of a command
                response = "M"
                for i in range(0, random.randint(3, 75)):
                    response += "O"
                sendText(response + "M")

        elif parsedCommand == "/swag":
            sendText("swiggity swag, what\'s in the bag?")

        elif parsedCommand == "/worms":
            if passSpamCheck():
                response = "hey man can I borrow your "
                if len(messageText) > len("/worms "):
                    response += messageText[len("/worms "):]
                else:
                    response += "worms"
                sendText(response)

        elif parsedCommand == "/shh" or parsedCommand == "/shhh":
            if passSpamCheck():
                sendPhoto("shhh.jpg")

        elif parsedCommand == "/father":
            if (random.randint(0, 1)):
                sendText("You ARE the father!")
            else:
                sendText("You are NOT the father!")

        elif parsedCommand == "/rip":   #sends "I can't believe that [name (defaults to sender's name)] is fucking dead."
            if passSpamCheck():
                response = "I can't believe that "
                if len(messageText) > len("/rip "):
                    if (messageText[len("/rip "):] == "me"):
                        response += currentMessage.from_user.first_name
                    else:
                        response += messageText[len("/rip "):]
                else:
                    response += currentMessage.from_user.first_name
                response += " is fucking dead."
                sendText(response)

        elif parsedCommand == "/scrub":
            checkingStats = False
            try:
                if currentMessage.text.lower().split()[1] == "stats":
                    db = Base('chatStorage/scrub.pdl') #The path to the DB
                    db.create('username', 'name', 'counter', mode="open")
                    K = list()
                    for user in db:
                        K.append(user)
                    sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
                    outputString = "SCRUBBIEST LEADERBOARD:\n"
                    for user in sortedK:
                        pluralString = " SCRUB POINT"
                        if not(int(user['counter']) == 1):
                            pluralString += "S"
                        pluralString += "\n"
                        outputString += user['name'].upper() + ": " + str(user['counter']) + pluralString
                    sendText(outputString)
                    checkingStats = True
            except IndexError:
                pass

            if not checkingStats and (currentMessage.from_user.id == 169883788 or currentMessage.from_user.id == 44961843):
                db = Base('chatStorage/scrub.pdl')
                db.create('username', 'name', 'counter', mode="open")

                userWasFound = False
                valueSuccessfullyChanged = False

                for user in db:
                    if int(user['username']) == currentMessage.reply_to_message.from_user.id:
                        db.update(user, counter=int(user['counter']) + 1)
                        valueSuccessfullyChanged = True
                        userWasFound = True
                db.commit()

                if not userWasFound:
                    db.insert(currentMessage.reply_to_message.from_user.id, currentMessage.reply_to_message.from_user.first_name, 1)
                    db.commit()

                if valueSuccessfullyChanged or not userWasFound:
                    sendText("Matt Gomez awarded a scrub point to " + currentMessage.reply_to_message.from_user.first_name + ".")

            elif not checkingStats:
                sendText("AdamTestBot, powered by ScrubSoft (C)")

        elif parsedCommand == "/hiss":
            checkingStats = False
            try:
                if currentMessage.text.lower().split()[1] == "stats":
                    db = Base('chatStorage/hiss.pdl')
                    db.create('username', 'name', 'counter', mode="open")
                    K = list()
                    for user in db:
                        K.append(user)
                    sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
                    outputString = "Hiss Leaderboard:\n"
                    for user in sortedK:
                        pluralString = " hiss"
                        if not(int(user['counter']) == 1):
                            pluralString += "es"
                        pluralString += "\n"
                        outputString += user['name'] + ": " + str(user['counter']) + pluralString
                    sendText(outputString)
                checkingStats = True
            except IndexError:
                pass

            if not checkingStats and (currentMessage.from_user.id == 122526873 or currentMessage.from_user.id == 44961843):
                db = Base('chatStorage/hiss.pdl')
                db.create('username', 'name', 'counter', mode="open")

                userWasFound = False
                valueSuccessfullyChanged = False

                for user in db:
                    if int(user['username']) == currentMessage.reply_to_message.from_user.id:
                        db.update(user, counter=int(user['counter']) + 1)
                        valueSuccessfullyChanged = True
                        userWasFound = True
                db.commit()

                if not userWasFound:
                    db.insert(currentMessage.reply_to_message.from_user.id, currentMessage.reply_to_message.from_user.first_name, 1)
                    db.commit()

                if valueSuccessfullyChanged or not userWasFound:
                    sendText("Robyn hissed at " + currentMessage.reply_to_message.from_user.first_name + ".")

        elif parsedCommand == "/water":
            if (random.randint(0, 1) == 0):
                sendSticker("water.webp")
            else:
                sendSticker("hoboken_water.webp")
        elif parsedCommand == "/sysinfo":
            cpu = []
            for x in range(5):
                cpu.append(psutil.cpu_percent(interval=1))
            cpuavg = round(sum(cpu) / float(len(cpu)), 1)
            memuse = psutil.virtual_memory()[2]
            diskuse = psutil.disk_usage('/')[3]
            sendText("The CPU uasge is " + str(cpuavg) + "%, the memory usage is " + str(memuse) + "%, and " + str(diskuse) + "% of the disk has been used.")
        #this command should go last:
        elif parsedCommand == "/community": #add your command to this list
            response = "/mom - get the camera\n"
            response += "/mooom (any number of \'o\'s) - call for help\n"
            response += "/swag - more memes\n"
            response += "/worms - can I borrow them?\n"
            response += "/shh(h) - here, be relaxed\n"
            response += "/father - are you the father?\n"
            response += "/rip (something) - I can't believe they're dead!\n"
            response += "/hiss stats - see how many time Robyn has hissed at people\n"
            response += "/scrub or /scrub stats - see who sponsors me or how many times Matt Gomez has called you a scrub\n"
            response += "/water - does this water look brown to you?\n"
            response += "/sysinfo - Gets server performance info."
            sendText(response)

        else:
            return False

        return True
    except Exception:
        print(traceback.format_exc())
        return False
