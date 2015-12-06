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

from pydblite import Base #The PyDbLite stuff
import __builtin__

messagesSent = 0
spamLimitTime = 15

spamArray = {}

def helpResponse():
    response = "/goodmorning - say hello\n"
    response += "/goodnight - say goodbye\n"
    response += "/shotty - settle disputes over who gets to ride shotgun\n"
    response += "/snail words - sneeple have infiltrated the government\n"
    response += "/fight - Fight someone. Reply to a message to fight whoever wrote it\n"
    response += "/objection - reply to a message to object to its contents\n"
    response += "/pick Name Name Name - the bot will pick someone or something from the list\n"
    response += "/fmk Name or /fmk Name Name Name - the bot will answer your burning questions\n"
    response += "/age - learn how long this instance of the bot has been running\n"
    response += "/yesorno - let me guide your life choices\n"
    response += "/8ball - ask the emojic 8ball a question\n"
    response += "/summon Name - summon somebody to your chat\n"
    response += "/adlib - learn about this bot's ability to ad lib posts\n"
    response += "/more - extra commands"
    return response

def moreResponse():
    response = "/ping - returns pong\n"
    response = "/expand - expands dong\n"
    response += "/meme - only the dankest\n"
    response += "/john_madden - UUUUUUUUU\n"
    response += "/john_cena - THE UNDERTAKER\n"
    response += "/gtg - mom\'s here\n"
    response += "/yiss or /yiss word - aww yiss\n"
    response += "/smash - a catchphrase\n"
    response += "/screams - communicate your internal anguish\n"
    response += "/essay - fuck\n"
    response += "/community - learn about commands other people made, if they wrote about them"
    return response

def adlibResponse():
    response = "Ad lib commands will be replaced with appropriate words in a response by the bot.\n"
    response += "/whodefine Name, Name, Name, ... - define a list to select with /who\n"
    response += "/whocoulditbe - display the defined list\n"
    response += "/me - use this to insert yourself into a story.\n"
    response += "/who - replaced with a person or thing from the /whodefine list; will return [undefined] if none is found.\n"
    response += "/noun - replaced with a noun (person, place, or thing)\n"
    response += "/verb - replaced with a verb in the present tense\n"
    response += "/verbed - replaced with a verb in the past tense\n"
    response += "/verbing - replaced with a verb in the present participle (i.e. walking)\n"
    response += "/adjective - replaced with an adjective\n"
    response += "/adverb - replaced with an adverb\n"
    response += "/number - replaced with a number as a word (ie three)\n"
    response += "Any of these commands can be given with a capitalized first letter (ie /Noun) to guarantee the first letter of the returned word will be capitalized, or in all caps (ie /VERB) to get a word in all caps.\n"
    return response

def spamCheck(chat_id, date):
    global spamArray
    global spamLimitTime
    try:
        spamArray[chat_id]['checking'] = True
    except Exception:
        spamArray[chat_id] = {'checking': True, 'spamTimestamp': 0}

    if time.mktime(date.timetuple()) - spamLimitTime > spamArray[chat_id]['spamTimestamp']:
        spamArray[chat_id]['spamTimestamp'] = time.mktime(date.timetuple())
        return True
    else:
        return False



def atReply():
    x = random.randint(0, 5)
    if x == 0:
        return "haha"
    elif x == 1:
        return "good, good"
    elif x == 2:
        return "Don't you have someone else to be bothering?"
    elif x == 3:
        return "nah"
    elif x == 4:
        return "lmao"
    elif x == 5:
        return "shhhhhhhhhhh"

def smashCommand():
    x = random.randint(0, 11)
    response = ""
    if x == 0:
        response = "I'M REALLY FEELIN\' IT"
    elif x == 1:
        response = "SHOW ME YA MOVES"
    elif x == 2:
        response = "HYES"
    elif x == 3:
        response = "okey"
    elif x == 4:
        response = "YOU'RE TOO SLOW"
    elif x == 5:
        response = "HAIIIIIII~"
    elif x == 6:
        response = "I fight for my friends."
    elif x == 7:
        response = "You\'ll get no sympathy from me."
    elif x == 8:
        response = "TIME TO TIP THE SCALES"
    elif x == 9:
        response = "*extends hand* C'MON"
    elif x == 10:
            response = "FIYURRR"
    elif x == 11:
            response = "WA, WA, WAAAAH"
    return response

def screamsCommand():
    x = random.randint(0, 3)
    response = ""
    if x == 0:
        response = "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    elif x == 1:
        response = "UGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    elif x == 2:
        response = "AUGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    elif x == 3:
        response = "?!!?!?!?!?!!!?!!!?!!?!!?!?!?!?!?!?!?!!!!!!???!??!?!?!?!?!??!??!!?!"
    return response

def fmk(options):
    if len(options) == 1:
        x = random.randint(1, 3)
        if x == 1:
            return "Fuck"
        elif x == 2:
            return "Marry"
        elif x == 3:
            return "Kill"
    elif len(options) == 3:
        x = random.randint(1, 6)
        if x == 1:
            return "Fuck: " + options[0] + ". Marry: " + options[1] + ". Kill: " + options[2] + "."
        elif x == 2:
            return "Fuck: " + options[0] + ". Marry: " + options[2] + ". Kill: " + options[1] + "."
        elif x == 3:
            return "Fuck: " + options[1] + ". Marry: " + options[0] + ". Kill: " + options[2] + "."
        elif x == 4:
            return "Fuck: " + options[1] + ". Marry: " + options[2] + ". Kill: " + options[0] + "."
        elif x == 5:
            return "Fuck: " + options[2] + ". Marry: " + options[1] + ". Kill: " + options[0] + "."
        elif x == 6:
            return "Fuck: " + options[2] + ". Marry: " + options[0] + ". Kill: " + options[1] + "."
    else:
        return "Usage: /fmk Name or /fmk Name Name Name"

def snailResponse(messageText):
    try:
        result = ""
        for modifyingWord in re.split(r'[@\s*]', messageText.lower()):
            if modifyingWord != "/snail":
                result += "sn" + modifyingWord[first_vowel(modifyingWord.decode("ascii")):] + " "
        return result
    except Exception:
        return "Usage: /snail word - NO WEIRD CHARACTERS."

def objectionResponse(currentMessage):
    response = ""
    try:
        if currentMessage.reply_to_message.username.lower() == "adamtestbot":
            response = "Objecting to me, " + currentMessage.from_user.first_name + "? Overruled."
        else:
            response = currentMessage.from_user.first_name.upper() + " OBJECTS TO WHAT " + currentMessage.reply_to_message.from_user.first_name.upper() + " SAID HERE!"
    except Exception: #reply_to_message didn't exist
        response = "Object to messages by replying to them with /object."
    return response

def ageCommand(instanceAge):
    weeks = int(instanceAge/(3600*24*7))
    days = int((instanceAge - (weeks * 3600 * 24 * 7))/(3600*24))
    hours = int((instanceAge - (weeks * 3600 * 24 * 7) - (days * (3600 * 24)))/3600)
    minutes = int((instanceAge - (weeks * 3600 * 24 * 7) - (days * (3600 * 24)) - (hours * 3600))/60)
    seconds = int((instanceAge % 60))

    stringWeeks = str(weeks) + "w"

    stringDays = str(days) + "d"

    stringHours = ""
    if hours < 10:
        stringHours = "0" + str(hours)
    else:
        stringHours = str(hours)
    stringHours += "h"

    stringMinutes = ""
    if minutes < 10:
        stringMinutes = "0" + str(minutes)
    else:
        stringMinutes = str(minutes)
    stringMinutes += "m"


    stringSeconds = ""
    if seconds < 10:
        stringSeconds = "0" + str(seconds)
    else:
        stringSeconds = str(seconds)
    stringSeconds += "s"

    stringDisplay = ""

    if weeks > 0:
        stringDisplay += stringWeeks + stringDays + stringHours + stringMinutes + stringSeconds
    elif days > 0:
        stringDisplay += stringDays + stringHours + stringMinutes + stringSeconds
    elif hours > 0:
        stringDisplay += stringHours + stringMinutes + stringSeconds
    elif minutes > 0:
        stringDisplay += stringMinutes + stringSeconds
    else:
        stringDisplay += stringSeconds

    return stringDisplay

def eightBall():
    x = random.randint(0, 15)
    if x == 0:
        return telegram.emoji.Emoji.FISTED_HAND_SIGN + telegram.emoji.Emoji.SPLASHING_SWEAT_SYMBOL
    elif x == 1:
        return telegram.emoji.Emoji.POUTING_FACE
    elif x == 2:
        return telegram.emoji.Emoji.THUMBS_UP_SIGN
    elif x == 3:
        return telegram.emoji.Emoji.SMILING_FACE_WITH_HEART_SHAPED_EYES
    elif x == 4:
        return telegram.emoji.Emoji.DISAPPOINTED_FACE
    elif x == 5:
        return telegram.emoji.Emoji.UNAMUSED_FACE
    elif x == 6:
        return telegram.emoji.Emoji.WEARY_FACE
    elif x == 7:
        return telegram.emoji.Emoji.FIRE + telegram.emoji.Emoji.WEARY_FACE + telegram.emoji.Emoji.FIRE
    elif x == 8:
        return telegram.emoji.Emoji.PISTOL + telegram.emoji.Emoji.FEARFUL_FACE
    elif x == 9:
        return telegram.emoji.Emoji.SMILING_FACE_WITH_OPEN_MOUTH_AND_COLD_SWEAT
    elif x == 10:
        return telegram.emoji.Emoji.HEART_DECORATION
    elif x == 11:
        return telegram.emoji.Emoji.THUMBS_DOWN_SIGN
    elif x == 12:
        return telegram.emoji.Emoji.CRYING_FACE
    elif x == 13:
        return telegram.emoji.Emoji.SMILING_FACE
    elif x == 14:
        return telegram.emoji.Emoji.FEARFUL_FACE
    elif x == 15:
        return telegram.emoji.Emoji.SMIRKING_FACE

def isMoom(parsedCommand):
    try:
        i = 1
        if parsedCommand.lower()[0] == "/" and parsedCommand.lower()[i] == "m":
            i += 1
            while parsedCommand.lower()[i] == "o":
                i += 1
            if parsedCommand.lower()[i] == "m" and i + 1 == len(parsedCommand) and i > 3:
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False

def fightResponse(currentMessage):
    response = ""
    fightingMe = False
    try:
        response = "OH FUCK, " + currentMessage.from_user.first_name.upper() + " WANTS TO FIGHT " + currentMessage.reply_to_message.from_user.first_name.upper() + "!"
        fightingMe = currentMessage.reply_to_message.from_user.first_name.lower() == "adamtestbot"
    except Exception:
        try:
            if len(currentMessage.text) <= len("/fight "):
                raise Exception
            response = "OH SHIT, " + currentMessage.from_user.first_name.upper() + " WANTS TO FIGHT "  + currentMessage.text[len("/fight "):].upper() + "!"
            fightingMe = currentMessage.text[len("/fight "):].lower() == "adamtestbot" or currentMessage.text[len("/fight "):].lower() == "@adamtestbot"
        except Exception:
            fightingMe = True
    if fightingMe:
        response = "You wanna fight ME, " + currentMessage.from_user.first_name + "??"
    return response

def summonResponse(currentMessage):
    response = ""
    summoningMe = False
    try:
        response = currentMessage.from_user.first_name + " is summoning " + currentMessage.reply_to_message.from_user.first_name + "!"
        summoningMe = currentMessage.reply_to_message.from_user.first_name.lower() == "adamtestbot"
    except Exception:
        try:
            if len(currentMessage.text) <= len("/summon "):
                raise Exception
            response = currentMessage.from_user.first_name + " is summoning " + currentMessage.text[len("/summon "):] + "!"
            summoningMe = currentMessage.text[len("/summon "):].lower() == "adamtestbot" or currentMessage.text[len("/summon "):].lower() == "@adamtestbot"
        except Exception:
            summoningMe = True
    if summoningMe:
        response = "I\'m already here, " + currentMessage.from_user.first_name + "."
    return response

def pickResponse(messageText):
    wholeTextArray = re.split(r'[@\s*]', messageText[len("/pick "):])
    if len(messageText) <= len("/pick "):
        return "Usage: /pick Name Name Name"
    else:
        answerIndex = random.randint(0, len(wholeTextArray) - 1)
        return wholeTextArray[answerIndex]




def blaze(currentMessage):
    checkingStats = False
    try:
        if currentMessage.text.lower().split()[1] == "stats":
            #db = Base('chatStorage/blaze.pdl') #The path to the database
            #db.create('username', 'name', 'counter', 'timestamp', mode="open") #Create a new DB if one doesn't exist. If it does, open it
            outputString = "JOINTS BLAZED:\n"
            K = list()
            for user in __builtin__.blazeDB:
            	K.append(user)
            sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
            for user in sortedK:
                pluralString = " JOINT"
                if not(int(user["counter"]) == 1):
                    pluralString += "S"
                pluralString += "\n"

                if int(user['timestamp']) + (24 * 3600) - 60 > time.mktime(currentMessage.date.timetuple()):
                    outputString += "*"
                outputString += user["name"].upper() + ": " + str(user["counter"]) + pluralString

            return outputString
            checkingStats = True
    except IndexError:
        pass

    start = datetime.time(4, 20)
    end = datetime.time(4, 20)
    time_received = currentMessage.date
    print start
    print time_received

    start2 = datetime.time(16, 20)
    end2 = datetime.time(16, 20)

    if start <= datetime.time(time_received.hour, time_received.minute) <= end: #4:20 AM
        if not checkingStats:
            return currentMessage.from_user.first_name + ", I know you like staying up late, but you really need to puff puff pass out."
    elif (start2 <= datetime.time(time_received.hour, time_received.minute) <= end2) and not checkingStats:
        pointsReceived = 4 - int(time_received.second/15)
        print "DEBUG TIME: PointsReceived=" + str(pointsReceived)

        #db = Base('chatStorage/blaze.pdl') #The path to the database
        #db.create('username', 'name', 'counter', 'timestamp', mode="open") #Create a new DB if one doesn't exist. If it does, open it

        userWasFound = False
        valueSuccessfullyChanged = False
        userPoints = 0

        for user in __builtin__.blazeDB:
              # print user['username']
            if int(user['username']) == currentMessage.from_user.id:
                if time.mktime(currentMessage.date.timetuple()) - 60 > int(user['timestamp']):
                    __builtin__.blazeDB.update(user, counter=int(user['counter']) + pointsReceived)
                    userPoints = user['counter']
                    __builtin__.blazeDB.update(user, timestamp=int(time.mktime(currentMessage.date.timetuple())))
                    valueSuccessfullyChanged = True
                    print "Found user!\n"
                userWasFound = True

        if not userWasFound:
            __builtin__.blazeDB.insert(currentMessage.from_user.id, currentMessage.from_user.first_name, pointsReceived, int(time.mktime(currentMessage.date.timetuple())))
            userPoints = pointsReceived

        if valueSuccessfullyChanged or not userWasFound:
            pluralString = " JOINT"
            if pointsReceived > 1:
                pluralString = pluralString + "S"
            #db.commit() #Write the in memory DB changes to disk
            return currentMessage.from_user.first_name.upper() + " 420 BLAZED IT AT " + str(time_received.second).upper() + " SECONDS. THEY BLAZED " + str(pointsReceived) + pluralString + " AND HAVE NOW SMOKED " + str(userPoints) + " IN TOTAL."
        else:
            return currentMessage.from_user.first_name + " is getting a bit too eager to blaze it."
    else:
        if not checkingStats:
            return currentMessage.from_user.first_name + " failed to blaze."




def first_vowel(s):
    if s[0].lower() != "y":
        i = re.search("[aeiouy]", s, re.IGNORECASE)
    else:
        i = re.search("[aeiou]", s, re.IGNORECASE)
    return 0 if i == None else i.start()

def log(user_id, currentMessage):
    try:
        K = list()
        logExists = os.path.exists('../log/' + str(user_id * -1) + 'log.csv')
        fieldnames=['name', 'text']
        if logExists:
            try:
                with open('../log/' + str(user_id * -1) + 'log.csv', 'r+') as csvfile:
                    reader = csv.DictReader(csvfile)
                    K = list(reader)
                with open('../log/' + str(user_id * -1) + 'log.csv', 'w+') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for x in K:
                        writer.writerow(x)
                    writer.writerow({'name': currentMessage.from_user.first_name, 'text': currentMessage.text})
            except Exception:
                pass
        else:
            file('../log/' + str(user_id * -1) + 'log.csv', 'a').close()
            with open('../log/' + str(user_id * -1) + 'log.csv', 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'name': currentMessage.from_user.first_name, 'text': currentMessage.text})
    except Exception:
        traceback.format_exc()

