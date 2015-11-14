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

import telegram

from .. import atbSendFunctions
from .. import atbMiscFunctions

#If you make your own python files for processing data, put them
#In the community folder and import them here:


####

chatInstanceArray = {}

def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        if not chatInstanceArray[chat_id]['adminDisable']:
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName):
        atbSendFunctions.sendPhoto(bot, chat_id, "images/"+ imageName)

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
                for i in range (0, random.randint(3, 75)):
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
                    response += messageText[len("/rip "):]
                else:
                    response += currentMessage.from_user.first_name
                response += " is fucking dead."
                sendText(response)



        #this command should go last:
    	elif parsedCommand == "/community": #add your command to this list
            response = "/mom - get the camera\n"
            response += "/mooom (any number of \'o\'s) - call for help\n"
            response += "/swag - more memes\n"
            response += "/worms - can I borrow them?\n"
            response += "/shh(h) - here, be relaxed\n"
            response += "/father - are you the father?\n"
            response += "/rip (something) - I can't believe they're dead!\n"

            sendText(response)

        else:
            return False

        return True
    except Exception:
        print traceback.format_exc()
        return False
