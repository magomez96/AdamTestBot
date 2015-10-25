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


print "@AdamTestBot - Reporting for duty!"
print "Written by Adam Gincel, shoutouts to Smesh"

APIKEY = '117924410:AAEVlUD58iH63xhcPpfklhf1N4FMvX07bfg'
REQUEST_URL = 'https://api.telegram.org/bot' + APIKEY

messageText = ""
imagePath = ""
keyboardLayout = [["" for x in range(5)] for x in range(5)]
logText = ""
sendingTextMessage = False
sendingImageMessage = False
sendingKeyboardMessage = False
sendingKillKeyboard = False
sendingReplyTo = False
sendingReplyToID = 0
user_id = 0
newestOffset = 0
commandString = ''
instanceAge = 0
messagesSent = 0
refreshRate = 2.5
failDelay = 0.5
timeSpentDisconnected = 0

fightMeString = "(" + "\xE0\xB8\x87".decode("utf-8") + "\xEF\xB8\xA1".decode("utf-8") + "\xE2\x80\x99".decode("utf-8") + "-" + "\xE2\x80\x99".decode("utf-8") + "\xEF\xB8\xA0".decode("utf-8") + ")" + "\xE0\xB8\x87".decode("utf-8")

wordlist = {}
verblist = {}
pastverblist = {}
verbinglist = {}
adjectivelist = {}
nounlist = {}
adverblist = {}
numberlist = {}

spamLimitTime = 15



with open('wordlists/verbinglist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    verbinglist = list(reader)

with open('wordlists/pastverblist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    pastverblist = list(reader)

with open('wordlists/verblist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    verblist = list(reader)

with open('wordlists/adjectivelist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    adjectivelist = list(reader)

with open('wordlists/nounlist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    nounlist = list(reader)

with open('wordlists/numberlist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    numberlist = list(reader)

with open('wordlists/adverblist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    adverblist = list(reader)

with open('wordlists/wordlist.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    wordlist = list(reader)



#clears the update queue and makes sure the bot only replies to updates received after it starts
data = {'offset': newestOffset + 1}
networkFailure = True
while networkFailure: #keep pinging until you get a response
    try:
        u = requests.get(REQUEST_URL + '/getUpdates', data=data).json()
        networkFailure = False
        newestOffset = u['result'][-1]['update_id']
    except Exception:
        print "...",
        time.sleep(failDelay)
        timeSpentDisconnected += failDelay
        if timeSpentDisconnected >= 30:
            pass
print "...Connected!"



def first_vowel(s):
    if s[0].lower() != "y":
        i = re.search("[aeiouy]", s, re.IGNORECASE)
    else:
        i = re.search("[aeiou]", s, re.IGNORECASE)
    return 0 if i == None else i.start()

def is_valid_text_overwrite(s):
    theString = s.lower()
    valid = "/who" in theString
    valid = valid or "/me" in theString
    valid = valid or "/word" in theString
    valid = valid or "/verb" in theString
    valid = valid or "/verbed" in theString
    valid = valid or "/verbing" in theString
    valid = valid or "/adjective" in theString
    valid = valid or "/noun" in theString
    valid = valid or "/adverb" in theString
    valid = valid or "/number" in theString
    return valid

def is_valid_text_overwrite_outer(s):
    theString = s.lower()
    valid = theString == "/who"
    valid = valid or theString == "/me"
    valid = valid or theString == "/word"
    valid = valid or theString == "/verb"
    valid = valid or theString == "/verbed"
    valid = valid or theString == "/verbing"
    valid = valid or theString == "/adjective"
    valid = valid or theString == "/noun"
    valid = valid or theString == "/adverb"
    valid = valid or theString == "/number"
    return valid

def cmd_textResponse(returnedString, logString, killKeyboard=False, replyTo=False, replyToOverride=user_id):
                global messageText
                global logText
                global sendingTextMessage
                global sendingImageMessage
                global sendingKeyboardMessage
                global sendingKillKeyboard
                global sendingReplyTo
                global sendingReplyToID
                messageText = returnedString;
                logText = logString + str(user_id)
                sendingTextMessage = True
                sendingImageMessage = False
                sendingKeyboardMessage = False

                if replyTo:
                    sendingReplyTo = True
                    sendingReplyToID = replyToOverride

                if killKeyboard:
                    sendingReplyTo = False
                    sendingKillKeyboard = True
                return

def cmd_imageResponse(givenImagePath, logString):
                global imagePath
                global logText
                global sendingImageMessage
                global sendingTextMessage
                global sendingKeyboardMessage
                imagePath = givenImagePath
                logText = logString + str(user_id)
                sendingImageMessage = True
                sendingTextMessage = False
                sendingKeyboardMessage = False
                return

def cmd_keyboardResponse(responseText, twodStringArray, logString):
                global keyboardLayout
                global logText
                global messageText
                global sendingImageMessage
                global sendingTextMessage
                global sendingKeyboardMessage
                messageText = responseText
                keyboardLayout = twodStringArray
                logText = logString + str(user_id)
                sendingImageMessage = False
                sendingTextMessage = False
                sendingKeyboardMessage = True
                return


#########Create Instance Dict
chatInstanceArray = {}
running = True

while running:

    timeSpentDisconnected = 0
    networkFailure = True
    while networkFailure and running: #keep pinging until you get a response
        try:
            data = {'offset': newestOffset + 1}
            u = requests.get(REQUEST_URL + '/getUpdates', data=data).json()
            networkFailure = False
        except Exception:
            print ".",
            timeSpentDisconnected += failDelay
            time.sleep(failDelay)
            if timeSpentDisconnected > 30:
                pass

    if instanceAge % (refreshRate * 10) == 0: #print 1 X every eight ticks
        print "Y"
    else:
        print "X",


    for current_message in u['result']:
        try:
            user_id = current_message['message']['chat']['id']


            #######populate chat Instance Array
            try:
                chatInstanceArray[user_id]['checking'] = True
            except Exception:
                chatInstanceArray[user_id] = {'checking': True, 'adminDisable': False, 'spamTimestamp': 0, 'shottyTimestamp': 0, 'shottyWinner': "", 'checkingVehicles': False, 'whoArray': []}

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
                        writer.writerow({'name': current_message['message']['from']['first_name'], 'text': current_message['message']['text']})
                except Exception:
                    pass
            else:
                file('../log/' + str(user_id * -1) + 'log.csv', 'a').close()
                with open('../log/' + str(user_id * -1) + 'log.csv', 'w+') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'name': current_message['message']['from']['first_name'], 'text': current_message['message']['text']})


            def getWho():
                try:
                    with open("chatStorage/" + str(user_id) + "whoArray.csv", "r+") as csvfile:
                        reader = csv.DictReader(csvfile)
                        whoArrayCurrent = list(reader)
                        return random.choice(whoArrayCurrent)['who']
                except Exception:
                    print traceback.format_exc()
                    return "[undefined]"

            def getWord():
                return random.choice(wordlist)['word']

            def getNoun():
                return random.choice(nounlist)['word'].replace(" ", "")

            def getNumber():
                return random.choice(numberlist)['word']

            def getAdjective():
                return random.choice(adjectivelist)['word'].replace(" ", "")

            def getVerb():
                return random.choice(verblist)['word'].replace(" ", "")

            def getVerbed():
                return random.choice(pastverblist)['word'].replace(" ", "")

            def getVerbing():
                return random.choice(verbinglist)['word'].replace(" ", "")

            def getAdverb():
                return random.choice(adverblist)['word'].replace(" ", "")

            def getScream():
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

            def overwrite_response(s):
                while "/ME" in s:
                    s = s.replace("/ME", current_message['message']['from']['first_name'].upper(), 1)

                while "/me" in s:
                    s = s.replace("/me", current_message['message']['from']['first_name'], 1)

                while "/WHO" in s:
                    s = s.replace("/WHO", getWho().upper(), 1)

                while "/Who" in s:
                    s = s.replace("/Who", getWho().title(), 1)

                while "/who" in s:
                    s = s.replace("/who", getWho(), 1)

                while "/WORD" in s:
                    s = s.replace("/WORD", getWord().upper(), 1)

                while "/Word" in s:
                    s = s.replace("/Word", getWord().capitalize(), 1)

                while "/word" in s:
                    s = s.replace("/word", getWord(), 1)

                while "/VERBING" in s:
                    s = s.replace("/VERBING", getVerbing().upper(), 1)

                while "/Verbing" in s:
                    s = s.replace("/Verbing", getVerbing().capitalize(), 1)

                while "/verbing" in s:
                    s = s.replace("/verbing", getVerbing(), 1)

                while "/VERBED" in s:
                    s = s.replace("/VERBED", getVerbed().upper(), 1)

                while "/Verbed" in s:
                    s = s.replace("/Verbed", getVerbed().capitalize(), 1)

                while "/verbed" in s:
                    s = s.replace("/verbed", getVerbed(), 1)

                while "/ADVERB" in s:
                    s = s.replace("/ADVERB", getAdverb().upper(), 1)

                while "/Adverb" in s:
                    s = s.replace("/Adverb", getAdverb().capitalize(), 1)

                while "/adverb" in s:
                    s = s.replace("/adverb", getAdverb(), 1)

                while "/VERB" in s:
                    s = s.replace("/VERB", getVerb().upper(), 1)

                while "/Verb" in s:
                    s = s.replace("/Verb", getVerb().capitalize(), 1)

                while "/verb" in s:
                    s = s.replace("/verb", getVerb(), 1)

                while "/ADJECTIVE" in s:
                    s = s.replace("/ADJECTIVE", getAdjective().upper(), 1)

                while "/Adjective" in s:
                    s = s.replace("/Adjective", getAdjective().capitalize(), 1)

                while "/adjective" in s:
                    s = s.replace("/adjective", getAdjective(), 1)

                while "/NOUN" in s:
                    print "replacing /NOUN..."
                    s = s.replace("/NOUN", getNoun().upper(), 1)

                while "/Noun" in s:
                    s = s.replace("/Noun", getNoun().capitalize(), 1)

                while "/noun" in s:
                    s = s.replace("/noun", getNoun(), 1)

                while "/NUMBER" in s:
                    s = s.replace("/NUMBER", getNumber().upper(), 1)

                while "/Number" in s:
                    s = s.replace("/Number", getNumber().capitalize(), 1)

                while "/number" in s:
                    s = s.replace("/number", getNumber(), 1)

                return s

            def handleLikes(isLiking):
                try:
                    #get disliked comment ID
                    likedID = current_message['message']['reply_to_message']['message_id']
                    likeReceivedID = current_message['message']['reply_to_message']['from']['id']
                    #check if likedID is in user's liked history
                    K = list()
                    passedCheck = True
                    fieldnames = ['messageID', 'liked']
                    isLikingSelf = int(likeReceivedID) == int(current_message['message']['from']['id'])
                    if isLikingSelf:
                        passedCheck = False
                    historyExists = os.path.exists('likes/history/' + str(current_message['message']['from']['id']) + 'history.csv')

                    if historyExists and passedCheck:
                        with open('likes/history/' + str(current_message['message']['from']['id']) + 'history.csv', 'r+') as csvfile:
                            reader = csv.DictReader(csvfile)
                            K = list(reader)
                            for x in K:
                                if int(x['messageID']) == int(likedID):
                                    passedCheck = False
                        with open('likes/history/' + str(current_message['message']['from']['id']) + 'history.csv', 'w+') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            for x in K:
                                writer.writerow(x)
                            if passedCheck:
                                text = ''
                                if isLiking:
                                    text = 't'
                                else:
                                    text = 'f'
                                writer.writerow({'messageID': likedID, 'liked': text})
                    else:
                        file('likes/history/' + str(current_message['message']['from']['id']) + 'history.csv', 'w').close()
                        with open('likes/history/' + str(current_message['message']['from']['id']) + 'history.csv', 'w+') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            if int(likeReceivedID) != int(current_message['message']['from']['id']):
                                text = ''
                                if isLiking:
                                    text = 't'
                                else:
                                    text = 'f'
                                writer.writerow({'messageID': likedID, 'liked': text})
                            else:
                                passedCheck = False
                    #if isn't in liked history and has passed any other checks:
                    if passedCheck:
                        K = list()
                        userWasFound = False
                        with open('likes/totals.csv', 'r+') as csvfile:
                            reader = csv.DictReader(csvfile)
                            K = list(reader)
                            for x in K:
                                if int(x['userID']) == int(likeReceivedID):
                                    userWasFound = True
                                    if isLiking:
                                        x['likes'] = str(int(x['likes']) + 1)
                                    else:
                                        x['dislikes'] = str(int(x['dislikes']) + 1)
                        fieldnames = ['userID', 'likes', 'dislikes']
                        with open('likes/totals.csv', 'w+') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            for x in K:
                                writer.writerow(x)
                            if not userWasFound:
                                if isLiking:
                                    likes = 1
                                    dislikes = 0
                                else:
                                    dislikes = 1
                                    likes = 0
                                writer.writerow({'userID': current_message['message']['reply_to_message']['from']['id'], 'likes': likes, 'dislikes': dislikes})
                except Exception as instanceException:
                    print traceback.format_exc()


            parsedCommand = re.split(r'[@\s:,\'*]', current_message['message']['text'].lower())[0]

            currentMessageText = "" + current_message['message']['text']

            #BEGIN COMMAND RESPONSES

            try:
                isNotCommand = parsedCommand[0] != "/" and parsedCommand[0] != "@"
            except Exception:
                isNotCommand = False

            if current_message['message']['text'].lower().split()[0] == "/admin" and current_message['message']['from']['username'] == "Adam_ZG":
                try:
                    if current_message['message']['text'].lower().split()[1] == "disable":
                        chatInstanceArray[user_id]['adminDisable'] = True
                        data = {'chat_id': user_id, 'text': "Adam has disabled me."}  #, 'reply_to_message_id': current_message['message']['message_id']}
                        requests.get(REQUEST_URL + '/sendMessage', data=data)
                    elif current_message['message']['text'].lower().split()[1] == "enable":
                        chatInstanceArray[user_id]['adminDisable'] = False
                        cmd_textResponse("Adam has enabled me.", "Reenabling at ")
                    elif current_message['message']['text'].lower().split()[1] == "sendto":
                        try:
                            data = {'chat_id': int(current_message['message']['text'].lower().split()[2]), 'text': current_message['message']['text'][15 + len(current_message['message']['text'].lower().split()[2]):]}
                            requests.get(REQUEST_URL + '/sendMessage', data=data)
                        except Exception:
                            pass
                    elif current_message['message']['text'].lower().split()[1] == "restart":
                        running = False
                except IndexError:
                    pass

            elif current_message['message']['text'].lower().startswith("@adamtestbot"):
                x = random.randint(0, 5)
                response = ""
                if x == 0:
                    response = "Haha"
                elif x == 1:
                    response = "Mhm. Right."
                elif x == 2:
                    response = "I\'m definitely listening."
                elif x == 3:
                    response = "Don\'t you have someone else to be bothering?"
                elif x == 4:
                    response = "I don\'t follow."
                elif x == 5:
                    response = "*sigh* okay, whatever."

                cmd_textResponse(response, response + "...Replying at ")

            elif isNotCommand or is_valid_text_overwrite_outer(parsedCommand): ###Handle any chat input recieved not starting with / for command or @ for dm
                if chatInstanceArray[user_id]['checkingVehicles'] and current_message['message']['text'].lower() == "i fucking love vehicles":
                    chatInstanceArray[user_id]['checkingVehicles'] = False
                    refreshRate = 2.5
                    cmd_textResponse("FUCKIN RIGHT YOU DO, " + current_message['message']['from']['first_name'].upper(), "Loved vehicles at ", True)
                elif chatInstanceArray[user_id]['checkingVehicles'] and current_message['message']['text'].lower() == "they\'re okay":
                    chatInstanceArray[user_id]['checkingVehicles'] = False
                    refreshRate = 2.5
                    cmd_textResponse(current_message['message']['from']['first_name'] + ", you disgust me.", "Did\'nt love vehicles at ", True)
                elif is_valid_text_overwrite(current_message['message']['text'].lower()):
                    response = "" + current_message['message']['text']
                    response = overwrite_response(response)
                    cmd_textResponse(response, response + " at ")


            elif parsedCommand == "/ping":
                cmd_textResponse("pong", "Ponged at ")

            elif parsedCommand == "/expand":
                cmd_textResponse("dong", "Expanded dong at ")

            elif parsedCommand == "/meme":
                cmd_textResponse("get memed on", "Memed on at ")

            elif parsedCommand == "/john_madden":
                cmd_textResponse("aeiou", "Chinese earthquake at ")

            elif parsedCommand == "/blaze":
                checkingStats = False
                try:
                    if current_message['message']['text'].lower().split()[1] == "stats":
                        with open('users.csv', 'r+') as csvfile:
                            reader = csv.DictReader(csvfile)
                            K = list(reader)
                            sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
                            outputString = "JOINTS BLAZED:\n"
                            for user in sortedK:
                                pluralString = " JOINT"
                                if not(int(user['counter']) == 1):
                                    pluralString += "S"
                                pluralString += "\n"

                                if int(user['timestamp']) + (12 * 3600) - 60 > current_message['message']['date']:
                                    outputString += "*"

                                outputString += user['name'].upper() + ": " + user['counter'] + pluralString

                            cmd_textResponse(outputString, "Blaze stats going to ")
                            checkingStats = True
                except IndexError:
                   pass

                start = datetime.time(4, 20)
                end = datetime.time(4, 20)
                time_received = datetime.datetime.fromtimestamp(current_message['message']['date']).time()
                print start
                print time_received

                start2 = datetime.time(16, 20)
                end2 = datetime.time(16, 20)

                if start <= datetime.time(time_received.hour, time_received.minute) <= end:
                    if not checkingStats:
                        cmd_textResponse(current_message['message']['from']['first_name'] + ", I know you like staying up late, but you really need to puff puff pass out.", "Puff puff pass out at")
                elif (start2 <= datetime.time(time_received.hour, time_received.minute) <= end2) and not checkingStats:
                    fieldnames = ['username', 'name', 'counter', 'timestamp']
                    K = list()

                    pointsReceived = 4 - int(time_received.second/15)

                    with open('users.csv', 'r+') as csvfile:
                        reader = csv.DictReader(csvfile)
                        K = list(reader)

                        userWasFound = False
                        valueSuccessfullyChanged = False
                        userPoints = 0

                        for user in K:
                           # print user['username']
                            if int(user['username']) == current_message['message']['from']['id']:
                                if current_message['message']['date'] - 60 > int(user['timestamp']):
                                    user['counter'] = int(user['counter']) + pointsReceived
                                    userPoints = user['counter']
                                    user['timestamp'] = current_message['message']['date']
                                    valueSuccessfullyChanged = True
                                userWasFound = True
                                print current_message['message']['date']
                    with open('users.csv', 'w+') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        for x in K:
                            writer.writerow(x)

                        if not userWasFound:
                            writer.writerow({'username': current_message['message']['from']['id'], 'name': current_message['message']['from']['first_name'], 'counter': pointsReceived, 'timestamp': current_message['message']['date']})
                            userPoints = 1


                    if valueSuccessfullyChanged or not userWasFound:
                        pluralString = " JOINT"
                        if pointsReceived > 1:
                            pluralString = pluralString + "S"
                        cmd_textResponse(current_message['message']['from']['first_name'].upper() + " 420 BLAZED IT AT " + str(time_received.second).upper() + " SECONDS. THEY BLAZED " + str(pointsReceived) + pluralString + " AND HAVE NOW SMOKED " + str(userPoints) + " IN TOTAL.", "Blazed! ")
                    else:
                        cmd_textResponse(current_message['message']['from']['first_name'] + " is getting a bit too eager to blaze it.", "Tried spamming blaze at ")
                else:
                    if not checkingStats:
                        cmd_textResponse(current_message['message']['from']['first_name'] + " failed to blaze.", "Failed blaze. ")


            elif parsedCommand == "/snail":
                try:
                    result = ""
                    for modifyingWord in re.split(r'[@\s*]', current_message['message']['text'].lower()):
                        if modifyingWord != "/snail":
                            result += "sn" + modifyingWord[first_vowel(modifyingWord.decode("ascii")):] + " "
                    cmd_textResponse(result, result + " at ", False, True)
                except Exception:
                    cmd_textResponse("Usage: /snail word - NO WEIRD CHARACTERS", "Wrong parameters for snail at ", False, True)

            elif parsedCommand == "/essay":
                x = random.randint(0, 1)
                response = ""

                if x == 0:
                    response = "NO. FUCK ESSAYS."
                elif x == 1:
                    response = "I DON\'T WANNA."
                cmd_textResponse(response, "Essay complaining at ")

            elif parsedCommand == "/smash":
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

                cmd_textResponse(response, response + " at ")

            elif parsedCommand == "/screams":
                if current_message['message']['date'] - spamLimitTime > chatInstanceArray[user_id]['spamTimestamp']:
                    chatInstanceArray[user_id]['spamTimestamp'] = current_message['message']['date']
                    response = current_message['message']['from']['first_name'] + ": "
                    response += getScream()
                    cmd_textResponse(response, "Scream at ")
                else:
                    pass

            elif parsedCommand == "/summon":
                response = ""
                summoningMe = False
                try:
                    response = current_message['message']['from']['first_name'] + " is summoning " + current_message['message']['reply_to_message']['from']['first_name'] + "!"
                    summoningMe = (current_message['message']['reply_to_message']['from']['first_name'].upper() == "ADAMTESTBOT")
                except Exception:
                    try:
                        if (len(current_message['message']['text']) <= 8):
                            raise Exception
                        response = current_message['message']['from']['first_name'] + " is summoning " + current_message['message']['text'][len("/summon "):] + "!"
                        summoningMe = current_message['message']['text'][len("/summon "):].upper() == "ADAMTESTBOT" or current_message['message']['text'][len("/summon "):].upper() == "@ADAMTESTBOT"
                    except Exception:
                        summoningMe = True
                if summoningMe:
                    response = "I\'m already here, " + current_message['message']['from']['first_name'] + "."

                cmd_textResponse(response, "Summoning at ")

            elif parsedCommand == "/whodefinespace":
                wholeTextArray = re.split(r'[@\s*]', current_message['message']['text'][len("/whodefinespace "):])
                if len(current_message['message']['text']) > len("/whodefinespace "):
                    chatInstanceArray[user_id]['whoArray'] = wholeTextArray
                    cmd_textResponse("Entries stored.", "Stored who array at ")
                else:
                    chatInstanceArray[user_id]['whoArray'] = []
                    cmd_textResponse("Entries cleared. Define new array before using /who", "Cleared whodefine at ")

            elif parsedCommand == "/whodefine":
                theText = current_message['message']['text'][len("/whodefine "):].replace(", ", ",")
                wholeTextArray = re.split(r'[,*]', theText)
                fieldnames = ['who']
                if len(current_message['message']['text']) > len("/whodefine "):
                    with open("chatStorage/" + str(user_id) + "whoArray.csv", "w+") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        for who in wholeTextArray:
                            writer.writerow({'who': who})
                    cmd_textResponse("Entries stored to file.", "Who perm at ")
                else:
                    with open("chatStorage/" + str(user_id) + "whoArray.csv", "w+") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                    cmd_textResponse("Entries cleared. Define new array before using /who", "Cleared whodefine at ")

            elif parsedCommand == "/whocoulditbe":
                response = ""
                try:
                    with open("chatStorage/" + str(user_id) + "whoArray.csv", "r+") as csvfile:
                        reader = csv.DictReader(csvfile)
                        whoArrayCurrent = list(reader)
                        response = "Current Who List:\n"
                        for x in whoArrayCurrent:
                            response += x['who'] + "\n"
                except Exception:
                    response = "No who list defined. Please use the /whodefine command to create a list of people."

                cmd_textResponse(response, "Sent wholist at ")

            elif parsedCommand == "/pick":
                wholeTextArray = re.split(r'[@\s*]', current_message['message']['text'][len("/pick "):])

                if len(current_message['message']['text']) <= len("/pick "):
                    cmd_textResponse("No answers given. Usage: /pick Name Name Name", "No whoArray at ")
                else:
                    answerIndex = random.randint(0, len(wholeTextArray) - 1)
                    response = wholeTextArray[answerIndex]
                    cmd_textResponse(response, response + " at ")

            elif parsedCommand == "/fight":
                response = ""
                fightingMe = False
                try:
                    response = "OH FUCK, " + current_message['message']['from']['first_name'].upper() + " WANTS TO FIGHT " + current_message['message']['reply_to_message']['from']['first_name'].upper() + "!!! " + fightMeString
                    fightingMe = (current_message['message']['reply_to_message']['from']['first_name'].upper() == "ADAMTESTBOT")
                except Exception:
                    print traceback.format_exc()
                    try:
                        if (len(current_message['message']['text']) <= 7):
                            raise Exception
                        response = "OH SHIT, " + current_message['message']['from']['first_name'].upper() + " WANTS TO FIGHT " + current_message['message']['text'][len("/fight "):].upper() + "!! " + fightMeString
                        fightingMe = current_message['message']['text'][len("/fight "):].upper() == "ADAMTESTBOT" or current_message['message']['text'][len("/fight "):].upper() == "@ADAMTESTBOT"
                    except Exception:
                        fightingMe = True
                if fightingMe:
                    response = "You wanna fight ME, " + current_message['message']['from']['first_name'] + "?? " + fightMeString

                cmd_textResponse(response, "Fight at ")

            elif parsedCommand == "/age":

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



                cmd_textResponse("This instance has been running for " + stringDisplay + " and has sent " + str(messagesSent + 1) + " messages!", "Sent age to ")

            elif parsedCommand == "/get":
                continueGoing = True
                try:
                    if re.split(r'[@\s*]', current_message['message']['text'].lower())[1] == "adamtestbot":
                        cmd_textResponse("ImageBot is dead and I killed him.", "Admitting Murder at ")
                        continueGoing = False
                    else:
                        continueGoing = False
                except IndexError:
                    cmd_textResponse("ImageBot is dead and I killed him.", "Admitting Murder at ")

            elif parsedCommand == "/yesorno":
                x = random.randint(0, 1)
                response = ""
                if x == 0:
                    response = "No."
                else:
                    response = "Yes."
                cmd_textResponse(response, response + " at ")

            elif parsedCommand == "/gtg":
                response = current_message['message']['from']['first_name'] + "\'s mom is here; they have to go."
                cmd_textResponse(response, "gtg at ")

            elif parsedCommand == "/yiss":
                if current_message['message']['date'] - spamLimitTime > chatInstanceArray[user_id]['spamTimestamp'] and not chatInstanceArray[user_id]['adminDisable']:
                    chatInstanceArray[user_id]['spamTimestamp'] = current_message['message']['date']
                    data = {'chat_id': user_id, 'text': "aww"}
                    requests.get(REQUEST_URL + '/sendMessage', data=data)
                    data = {'chat_id': user_id, 'text': "yiss"}
                    requests.get(REQUEST_URL + '/sendMessage', data=data)
                    data = {'chat_id': user_id, 'text': "motha"}
                    requests.get(REQUEST_URL + '/sendMessage', data=data)
                    data = {'chat_id': user_id, 'text': "fuckin"}
                    requests.get(REQUEST_URL + '/sendMessage', data=data)
                    data = {'chat_id': user_id, 'text': "breadcrumbs"}
                    requests.get(REQUEST_URL + '/sendMessage', data=data)
                    print "Aw yiss, breadcrumbs... " + current_message['message']['id']

            elif parsedCommand == "/objection":
                try:
                    response = current_message['message']['from']['first_name'].upper() + " OBJECTS TO WHAT " + current_message['message']['reply_to_message']['from']['first_name'].upper() + " SAID HERE!"
                    cmd_textResponse(response, response + " at ", False, True, current_message['message']['reply_to_message']['message_id'])
                except Exception:
                    cmd_textResponse("You have to object to SOMETHING, " + current_message['message']['from']['first_name'] + ".", "Failed objection at ")

            elif parsedCommand == "/goodnight":
                response = "Good night, " + current_message['message']['from']['first_name'] + "! " + "\xF0\x9F\x98\xAA".decode("utf-8")
                cmd_textResponse(response, "Said good night at ")

            elif parsedCommand == "/goodmorning":
                time_received = datetime.datetime.fromtimestamp(current_message['message']['date'])
                actual_time = datetime.time(time_received.hour, time_received.minute)

                if actual_time < datetime.time(12, 0) and actual_time > datetime.time(4, 59):
                    response = "Good morning, " + current_message['message']['from']['first_name'] + "! " + "\xF0\x9F\x98\x83".decode("utf-8")
                elif actual_time == datetime.time(3, 0):
                    response = current_message['message']['from']['first_name'] + ": Oh boy, three AM!"
                elif actual_time <= datetime.time(4, 59):
                    response = "It's the middle of the night, " + current_message['message']['from']['first_name'] + "! Go to bed!"
                else:
                    response = current_message['message']['from']['first_name'] + "'s a lazy shit. It isn't morning anymore! " + "\xF0\x9F\x98\xA9".decode("utf-8")

                cmd_textResponse(response, "Said good morning at ")

            elif parsedCommand == "/8ball":
                x = random.randint(0, 15)
                response = ""
                if x == 0:
                    response = "\xE2\x9C\x8A".decode("utf-8") + "\xF0\x9F\x92\xA6".decode("utf-8") #fist and sweat
                elif x == 1:
                    response = "\xF0\x9F\x98\xA1".decode("utf-8") #pouting face
                elif x == 2:
                    response = "\xF0\x9F\x91\x8D".decode("utf-8") #thumbs up
                elif x == 3:
                    response = "\xF0\x9F\x98\x8D".decode("utf-8") #heart eyes
                elif x == 4:
                    response = "\xF0\x9F\x98\xA3".decode("utf-8") #perversing face
                elif x == 5:
                    response = "\xF0\x9F\x98\x92".decode("utf-8") #unamused face
                elif x == 6:
                    response = "\xF0\x9F\x98\xA9".decode("utf-8") #weary face
                elif x == 7:
                    response = "\xF0\x9F\x94\xA5".decode("utf-8") + "\xF0\x9F\x98\xA9".decode("utf-8") + "\xF0\x9F\x94\xA5".decode("utf-8") #fire, weary face, fire
                elif x == 8:
                    response = "\xF0\x9F\x98\xA8".decode("utf-8") + "\xF0\x9F\x94\xAB".decode("utf-8") #gun and fearful face
                elif x == 9:
                    response = "\xF0\x9F\x98\x85".decode("utf-8") #sweating smiley
                elif x == 10:
                    response = "\xF0\x9F\x98\x8F".decode("utf-8") #smirking face
                elif x == 11:
                    response = "\xF0\x9F\x98\xA8".decode("utf-8") #fearful face
                elif x == 12:
                    response = "\xF0\x9F\x98\x83".decode("utf-8") #smiley
                elif x == 13:
                    response = "\xE2\x9D\xA4".decode("utf-8") #heart
                elif x == 14:
                    response = "\xF0\x9F\x91\x8E".decode("utf-8") #thumbs down
                elif x == 15:
                    response = "\xF0\x9F\x98\xAD".decode("utf-8") #crying face

                cmd_textResponse(response, "Send emoji to ")

            elif parsedCommand == "/kevi" + "\xC3\xB1".decode("utf-8"):
                if current_message['message']['date'] - spamLimitTime > chatInstanceArray[user_id]['spamTimestamp']:
                    cmd_imageResponse("kevin.jpg", "Sent kevin to ")
                    chatInstanceArray[user_id]['spamTimestamp'] = current_message['message']['date']
                else:
                    cmd_textResponse(current_message['message']['from']['first_name'] + ", you can\'t handle THAT much Kevi" + "\xC3\xB1".decode("utf-8") + ".", "Not that much kevin at ")

            elif parsedCommand == "/bitch":
                if current_message['message']['date'] - spamLimitTime > chatInstanceArray[user_id]['spamTimestamp']:
                    cmd_imageResponse("engling.jpg", "Sent engling to ")
                    chatInstanceArray[user_id]['spamTimestamp'] = current_message['message']['date']
                else:
                    cmd_textResponse(current_message['message']['from']['first_name'] + ", you can\'t handle THAT much Engling.", "Not that much Engling at ")


            elif parsedCommand == "/like":
                handleLikes(True)

            elif parsedCommand == "/dislike":
                handleLikes(False)

            elif parsedCommand == "/likes":
                try:
                    sentMyKarma = False
                    try:
                        if int(current_message['message']['reply_to_message']['from']['id']) == int(117924410): #is replying to bot message with /likes
                            with open('likes/totals.csv', 'r+') as csvfile:
                                reader = csv.DictReader(csvfile)
                                K = list(reader)
                                likes = K[0]['likes']
                                dislikes = K[0]['dislikes']
                                karma = int(likes) - int(dislikes)
                                response = "Since you asked, I have " + str(likes) + " likes and " + str(dislikes) + " dislikes, for a total of " + str(karma) + " karma. "
                                if karma > 0:
                                    response += "\xF0\x9F\x98\x83".decode("utf-8") #smiley
                                else:
                                    response += "\xF0\x9F\x98\xAD".decode("utf-8") #crying
                                cmd_textResponse(response, "Sent my karma to ")
                                sentMyKarma = True
                    except Exception:
                        print traceback.format_exc()

                    if not sentMyKarma:
                        userWasFound = False
                        likes = 0
                        dislikes = 0
                        with open('likes/totals.csv', 'r+') as csvfile:
                                reader = csv.DictReader(csvfile)
                                K = list(reader)
                                for x in K:
                                    if int(x['userID']) == int(current_message['message']['from']['id']):
                                        userWasFound = True
                                        likes = x['likes']
                                        dislikes = x['dislikes']

                        if userWasFound:
                            cmd_textResponse(current_message['message']['from']['first_name'] + ", you have " + str(likes) + " likes and " + str(dislikes) + " dislikes, for a total of " + str(int(likes) - int(dislikes)) + " karma.", "Sent likes at")
                        else:
                            cmd_textResponse("No like data found!", "No like data at")
                except Exception:
                    print traceback.format_exc()

            elif parsedCommand == "/shotty":
                if current_message['message']['date'] - 3600 > chatInstanceArray[user_id]['shottyTimestamp']:
                    chatInstanceArray[user_id]['shottyWinner'] = current_message['message']['from']['first_name']
                    chatInstanceArray[user_id]['shottyTimestamp'] = current_message['message']['date']
                    cmd_textResponse(current_message['message']['from']['first_name'] + " called shotgun. Dibs no blitz for the next hour.", current_message['message']['from']['first_name'] + " took shotty at ")
                else:
                    timeRemaining = int(chatInstanceArray[user_id]['shottyTimestamp'] - (current_message['message']['date'] - 3600))/60 + 1
                    cmd_textResponse(chatInstanceArray[user_id]['shottyWinner'] + " has shotty for the next " + str(timeRemaining) + " minutes.", "Failed shotty at ")

            elif parsedCommand == "/killkeyboard":
                cmd_textResponse("Killing keyboards.", "Killing keyboards at ", True)

            elif parsedCommand == "/vehicles":
                if current_message['message']['from']['id'] == 51561968 or current_message['message']['from']['id'] == 44961843:
                    myStringArray = [["I FUCKING LOVE VEHICLES"], ["they\'re okay"], ["they\'re okay"], ["they\'re okay"]]
                    random.shuffle(myStringArray)
                    chatInstanceArray[user_id]['checkingVehicles'] = True
                    refreshRate = .1
                    cmd_keyboardResponse("Do you like vehicles?", myStringArray, "Asking about vehicles at ")
                else:
                    cmd_textResponse("Sorry, " + current_message['message']['from']['first_name'] + ", the vehicles command belongs to Skylar.", "Not Skylar vehicles at ")

            elif parsedCommand == "/test" and current_message['message']['from']['username'] == "Adam_ZG":
                myStringArray = [["A", "B"]]
                cmd_keyboardResponse("Question:", myStringArray, "Testing at ")

            elif parsedCommand == "/mom":
                cmd_textResponse("MOM GET THE CAMERA", "/mom at ")

            elif parsedCommand == "/moom" or parsedCommand == "/mooom":
                response = "M"
                for i in range(1, random.randint(3, 50)):
                    response += "O"
                response += "M"
                cmd_textResponse(response, "/moom at ")

            elif parsedCommand == "/help":
                response = "/goodmorning - say hello\n"
                response += "/goodnight - say goodbye\n"
                response += "/shotty - settle disputes over who gets to ride shotgun\n"
                response += "/snail word - sneeple have taken over the government\n"
                response += "/fight - fight somebody, or reply to message to fight whoever wrote it\n"
                response += "/objection - object to somebody, or reply to a message to object to it\n"
                response += "/pick Name Name Name - the bot will pick someone or something from the list\n"
                response += "/summon Name - summon somebody to your chat\n"
                response += "/adlib - learn about this bot's ability to ad lib posts\n"
                response += "/more - extra commands"

                cmd_textResponse(response, "Sending help at ")

            elif parsedCommand == "/adlib":
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

                cmd_textResponse(response, "Sending ad lib tutorial at ")




            elif parsedCommand == "/more":
                response = "/ping - returns pong\n"
                response += "/expand - expands dong\n"
                response += "/meme - only the dankest\n"
                response += "/john_madden - UUUUUUUUU\n"
                response += "/get - a confession\n"
                response += "/gtg - mom\'s here\n"
                response += "/yiss - aww yiss\n"
                response += "/kevi" + "\xC3\xB1".decode("utf-8") + " - a face\n"
                response += "/vehicles - Skylar's special command\n"
                response += "/smash - a catchphrase\n"
                response += "/screams - communicate your internal anguish\n"

                cmd_textResponse(response, "Sending more at ")

            ##################################################################

            #Actual sending, text, photo, or keyboard for now

            if sendingTextMessage and not chatInstanceArray[user_id]['adminDisable']:
                print logText
                sendingTextMessage = False
                sendingImageMessage = False
                sendingKeyboardMessage = False

                messagesSent += 1

                data = {'chat_id': user_id, 'action': "typing"}
                requests.get(REQUEST_URL + "/sendChatAction", data=data)

                if sendingKillKeyboard:
                    sendingKillKeyboard = False
                    replyKeyboardHide = {"hide_keyboard": True}
                    payload = {"chat_id": user_id, "text": messageText, "reply_markup": json.dumps(replyKeyboardHide)}
                elif sendingReplyTo:
                    sendingReplyTo = False
                    payload = {"chat_id": user_id, "text": messageText, "reply_to_message_id": sendingReplyToID}
                else:
                    payload = {'chat_id': user_id, 'text': messageText}
                requests.get(REQUEST_URL + '/sendMessage', data=payload)


            elif sendingImageMessage and not chatInstanceArray[user_id]['adminDisable']:
                print logText
                sendingTextMessage = False
                sendingImageMessage = False
                sendingKeyboardMessage = False
                messagesSent += 1
                data = {'chat_id': user_id, 'action': "upload_photo"}
                requests.get(REQUEST_URL + "/sendChatAction", data=data)
                data = {'chat_id': user_id}
                files = {'photo': (imagePath, open(imagePath, "rb"))}
                requests.post(REQUEST_URL + '/sendPhoto', data=data, files=files)

            elif sendingKeyboardMessage and not chatInstanceArray[user_id]['adminDisable']:
                sendingTextMessage = False
                sendingImageMessage = False
                sendingKeyboardMessage = False
                messagesSent += 1
                replyKeyboardMakeup = {"keyboard": keyboardLayout, "one_time_keyboard": True, "resize_keyboard": True}
                payload = {"chat_id": user_id, "text": messageText, "reply_markup": json.dumps(replyKeyboardMakeup)}
                print requests.get(REQUEST_URL + "/sendMessage", data=payload).url
                print logText


            ######################################
        except KeyError:
            pass
        except Exception as instanceException:
            print traceback.format_exc()
    try:
        newestOffset = u['result'][-1]['update_id']
    except IndexError:
        pass
    instanceAge += refreshRate
    time.sleep(refreshRate)


#found at https://core.telegram.org/bots/api

#u['result'] has ['update_id'] or ['message']
#['message'] has: message_id, from (type: User), date (int in unix), chat (User or GroupChat)...
#...forward_from (User), forward_date (int in unix time), reply_to_message (Message, not recursive)...
#...text (String), audio (Audio), document (Document), photo (Array of PhotoSize), sticker (Sticker)...
#...video (Video), contact (Contact), location (Location), new_chat_participant (User), left_chat_participant
#(user), new_chat_title (String), new_chat_photo (String), delete_chat_photo/group_chat_created (True)

#useful: message -> from (User), date, chat (User or GroupChat), text (String)

#User: id (Integer), first_name (String), last_name (String), username (String)

#GroupChat: id (Integer), title (String)
