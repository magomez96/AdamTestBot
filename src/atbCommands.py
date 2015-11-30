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

import atbSendFunctions
import atbMiscFunctions
import atbAdLib
import atbLikes
import Community.atbCommunity as atbCommunity

chatInstanceArray = {}
spamLimitTime = 15
messageSent = 1


def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    global messageSent

    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        if not chatInstanceArray[chat_id]['adminDisable']:
            global messageSent
            messageSent += 1
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName):
        global messageSent
        messageSent += 1
        atbSendFunctions.sendPhoto(bot, chat_id, "images/"+ imageName)

    def passSpamCheck():
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date)

    try:
        atbMiscFunctions.log(chat_id, currentMessage)

        try:
            chatInstanceArray[chat_id]['checking'] = True
        except Exception:
            chatInstanceArray[chat_id] = {'checking': True, 'adminDisable': False, 'spamTimestamp': 0, 'shottyTimestamp': 0, 'shottyWinner': "", 'checkingVehicles': False, 'whoArray': []}

        if parsedCommand == "/admin":
            if currentMessage.from_user.username == "Adam_ZG":
                try:
                    if messageText.lower().split()[1] == "disable":
                        chatInstanceArray[chat_id]['adminDisable'] = True
                        sendText("Adam has disabled me.")
                    elif messageText.lower().split()[1] == "enable":
                        chatInstanceArray[chat_id]['adminDisable'] = False
                        sendText("Adam has enabled me.")
                    elif messageText.lower().split()[1] == "sendto":
                        atbSendFunctions.sendText(bot, int(messageText.lower().split()[2]), messageText[15 + len(messageText.split()[2]):])
                except Exception:
                    pass

        elif messageText.lower().startswith("@adamtestbot"):
            sendText(atbMiscFunctions.atReply())

        elif parsedCommand == "/whodefine":
            if atbAdLib.whoDefine(chat_id, messageText):
                sendText("Entries stored to file.")
            else:
                sendText("Entries cleared. Define new array before using /who")

        elif parsedCommand == "/whocoulditbe":
            sendText(atbAdLib.whoCouldItBe(chat_id))

        elif parsedCommand == "/like":
            atbLikes.handleLikes(True, currentMessage)

        elif parsedCommand == "/dislike":
            atbLikes.handleLikes(False, currentMessage)

        elif parsedCommand == "/likes":
            sendText(atbLikes.likes(currentMessage))

        elif parsedCommand == "/vehicles" and (currentMessage.from_user.id == 51561968 or currentMessage.from_user.id == 44961843): 
            chatInstanceArray[chat_id]['checkingVehicles'] = True
            sendText("Do you like vehicles?", keyboardLayout=[["they\'re okay"],["I FUCKING LOVE VEHICLES"], ["they\'re okay"], ["they\'re okay"]])

        #normal commands go here

        elif parsedCommand == "/ping":
            sendText("pong")

        elif parsedCommand == "/expand":
            sendText("dong")

        elif parsedCommand == "/meme":
            sendText("get memed on")

        elif parsedCommand == "/john_madden":
            sendText("aeiou")

        elif parsedCommand == "/john_cena":
            if passSpamCheck():
                sendText("ARE YOU READY FOR THIS SUNDAY NIGHT WHEN WWE CHAMP JOHN CENA DEFENDS HIS TITLE IN THE WWE SUUUUUUPERSLAMMMMMMM")
                sendText("right now you can order this awesome pay per view event for just $59.99")

        elif parsedCommand == "/blaze":
            sendText(atbMiscFunctions.blaze(currentMessage))

        elif parsedCommand == "/snail":
            sendText(atbMiscFunctions.snailResponse(messageText))

        elif parsedCommand == "/essay":
            sendText(random.choice(["NO. FUCK ESSAYS.", "I DON\'T WANNA."]))

        elif parsedCommand == "/kevi" + "\xC3\xB1".decode("utf-8"):
            if passSpamCheck():
                sendPhoto("kevin.jpg")

        elif parsedCommand == "/bitch":
            if passSpamCheck():
                sendPhoto("engling.jpg")

        elif parsedCommand == "/smash":
            sendText(atbMiscFunctions.smashCommand())

        elif parsedCommand == "/screams":
            if passSpamCheck():
                sendText(currentMessage.from_user.first_name + ": " + atbMiscFunctions.screamsCommand())

        elif parsedCommand == "/summon":
            sendText(atbMiscFunctions.summonResponse(currentMessage))

        elif parsedCommand == "/pick":
            sendText(atbMiscFunctions.pickResponse(messageText))

        elif parsedCommand == "/fmk":
            sendText(atbMiscFunctions.fmk(re.split(r'[@\s*]', messageText[len("/fmk "):])))

        elif parsedCommand == "/fight":
            sendText(atbMiscFunctions.fightResponse(currentMessage))

        elif parsedCommand == "/age":
            sendText("This instance has been running for " + atbMiscFunctions.ageCommand(instanceAge) + " and has sent " + str(messageSent) + " messages!")

        elif parsedCommand == "/yesorno":
            x = random.randint(0, 1)
            if x == 0:
                sendText("No.")
            else:
                sendText("Yes.")

        elif parsedCommand == "/gtg":
            sendText(currentMessage.from_user.first_name + "\'s mom is here; they have to go.")

        elif parsedCommand == "/yiss":
            if passSpamCheck():
                sendText("aww")
                sendText("yiss")
                sendText("motha")
                sendText("fuckin")
                if len(messageText) > len("/yiss "):
                    sendText(messageText[len("/yiss "):])
                else:
                    sendText("breadcrumbs")

        elif parsedCommand == "/objection":
            sendText(atbMiscFunctions.objectionResponse(currentMessage), replyingMessageID=currentMessage.reply_to_message.message_id)

        elif parsedCommand == "/goodnight":
            sendText("Good night, " + currentMessage.from_user.first_name + "! " + telegram.emoji.Emoji.SLEEPING_FACE.decode("utf-8"))

        elif parsedCommand == "/goodmorning":
            time_received = currentMessage.date
            actual_time = datetime.time(time_received.hour, time_received.minute)

            if actual_time < datetime.time(12, 0) and actual_time > datetime.time(4, 59):
                sendText("Good morning, " + currentMessage.from_user.first_name + "! " + telegram.emoji.Emoji.SMILING_FACE_WITH_OPEN_MOUTH.decode("utf-8"))
            elif actual_time == datetime.time(3, 0):
                sendText(currentMessage.from_user.first_name + ": Oh boy, three AM!")
            elif actual_time <= datetime.time(4, 59):
                sendText("It's the middle of the night, " + currentMessage.from_user.first_name + "! Go to bed!")
            else:
                sendText(currentMessage.from_user.first_name + "\'s a lazy shit. It isn\'t morning anymore! " + telegram.emoji.Emoji.WEARY_FACE.decode("utf-8"))

        elif parsedCommand == "/8ball":
            if currentMessage.from_user.id == 68536910:
                sendText(telegram.emoji.Emoji.SPARKLING_HEART)
            else:
                sendText(atbMiscFunctions.eightBall())

        elif parsedCommand == "/debug":
            sendText("ID: " + str(chat_id))

        elif parsedCommand == "/shotty":
            if time.mktime(currentMessage.date.timetuple()) - 3600 > chatInstanceArray[chat_id]['shottyTimestamp']:
                chatInstanceArray[chat_id]['shottyTimestamp'] = time.mktime(currentMessage.date.timetuple())
                chatInstanceArray[chat_id]['shottyWinner'] = currentMessage.from_user.first_name
                sendText(chatInstanceArray[chat_id]['shottyWinner'] + " called shotgun. Dibs no blitz for the next hour.")
            else:
                timeRemaining = int(chatInstanceArray[chat_id]['shottyTimestamp'] - (time.mktime(currentMessage.date.timetuple()) - 3600))/60 + 1
                sendText(chatInstanceArray[chat_id]['shottyWinner'] + " has shotty for the next " + str(timeRemaining) + " minutes.")

        elif parsedCommand == "/help":
            sendText(atbMiscFunctions.helpResponse())

        elif parsedCommand == "/adlib":
            sendText(atbMiscFunctions.adlibResponse())

        elif parsedCommand == "/more":
            sendText(atbMiscFunctions.moreResponse())

        elif atbAdLib.is_valid_text_overwrite(messageText): #all adlibbing logic done here
            sendText(atbAdLib.overwrite_response(messageText, currentMessage.from_user.first_name, chat_id))

        elif parsedCommand[0] != "/" and parsedCommand[0] != "@": #normal text
            if chatInstanceArray[chat_id]['checkingVehicles']:
                if messageText.lower() == "they\'re okay":
                    sendText("You disgust me, " + currentMessage.from_user.first_name, replyingMessageID=currentMessage.message_id)
                    chatInstanceArray[chat_id]['checkingVehicles'] = False    
                elif messageText.lower() == "i fucking love vehicles":
                    sendText("FUCKIN RIGHT YOU DO, " + currentMessage.from_user.first_name.upper(), replyingMessageID=currentMessage.message_id)
                    chatInstanceArray[chat_id]['checkingVehicles'] = False
                    
        else:
            if not atbCommunity.process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
                pass

        return True
    except Exception:
        print traceback.format_exc()
        return True
