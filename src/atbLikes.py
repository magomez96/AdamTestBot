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

def handleLikes(isLiking, currentMessage):
    try:
        #get disliked comment ID
        likedID = currentMessage.reply_to_message.message_id
        likeReceivedID = currentMessage.reply_to_message.from_user.id
        #check if likedID is in user's liked history
        K = list()
        passedCheck = True
        fieldnames = ['messageID', 'liked']
        isLikingSelf = int(likeReceivedID) == int(currentMessage.from_user.id)
        if isLikingSelf:
            passedCheck = False
        historyExists = os.path.exists('chatStorage/likes/history/' + str(currentMessage.from_user.id) + 'history.csv')

        if historyExists and passedCheck:
            with open('chatStorage/likes/history/' + str(currentMessage.from_user.id) + 'history.csv', 'r+') as csvfile:
                reader = csv.DictReader(csvfile)
                K = list(reader)
                for x in K:
                    if int(x['messageID']) == int(likedID):
                        passedCheck = False
            with open('chatStorage/likes/history/' + str(currentMessage.from_user.id) + 'history.csv', 'w+') as csvfile:
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
            file('chatStorage/likes/history/' + str(currentMessage.from_user.id) + 'history.csv', 'w').close()
            with open('chatStorage/likes/history/' + str(currentMessage.from_user.id) + 'history.csv', 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                if int(likeReceivedID) != int(currentMessage.from_user.id):
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
            with open('chatStorage/likes/totals.csv', 'r+') as csvfile:
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
            with open('chatStorage/likes/totals.csv', 'w+') as csvfile:
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
                    writer.writerow({'userID': currentMessage.reply_to_message.from_user.id, 'likes': likes, 'dislikes': dislikes})
    except Exception as instanceException:
        print traceback.format_exc()

def likes(currentMessage):
    try:
        sentMyKarma = False
        try:
            if int(currentMessage.reply_to_message.from_user.id) == int(117924410): #is replying to bot message with /likes
                with open('chatStorage/likes/totals.csv', 'r+') as csvfile:
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
                    return response
                    sentMyKarma = True
        except Exception:
            print traceback.format_exc()

        if not sentMyKarma:
            userWasFound = False
            likes = 0
            dislikes = 0
            with open('chatStorage/likes/totals.csv', 'r+') as csvfile:
                    reader = csv.DictReader(csvfile)
                    K = list(reader)
                    for x in K:
                        if int(x['userID']) == int(currentMessage.from_user.id):
                            userWasFound = True
                            likes = x['likes']
                            dislikes = x['dislikes']

            if userWasFound:
                return currentMessage.from_user.first_name + ", you have " + str(likes) + " likes and " + str(dislikes) + " dislikes, for a total of " + str(int(likes) - int(dislikes)) + " karma."
            else:
                return "No like data found!"
    except Exception:
        print traceback.format_exc()
        return ""
