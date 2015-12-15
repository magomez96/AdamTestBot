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

def getWordList(listname):
    with open('wordlists/' + listname + '.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

verbinglist = getWordList("verbinglist")
pastverblist = getWordList("pastverblist")
verblist = getWordList("verblist")
adjectivelist = getWordList("adjectivelist")
nounlist = getWordList("nounlist")
numberlist = getWordList("numberlist")
adverblist = getWordList("adverblist")
wordlist = getWordList("wordlist")

def getWho(chat_id):
    try:
        with open("chatStorage/" + str(chat_id) + "whoArray.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            whoArrayCurrent = list(reader)
            print(whoArrayCurrent)
            return random.choice(whoArrayCurrent)['who']
    except Exception:
        print(traceback.format_exc())
        return "[undefined]"
def whoCouldItBe(chat_id):
    response = ""
    try:
        with open("chatStorage/" + str(chat_id) + "whoArray.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            whoArrayCurrent = list(reader)
            response = "Current /who list:\n"
            for x in whoArrayCurrent:
                response += x['who'] + "\n"
        return response
    except Exception:
        return "No /who list defined. Use /whodefine to create a list of people."

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

def overwrite_response(s, name, chat_id):
    while "/ME" in s:
        s = s.replace("/ME", name.upper(), 1)

    while "/me" in s:
        s = s.replace("/me", name, 1)

    while "/WHO" in s:
        s = s.replace("/WHO", getWho(chat_id).upper(), 1)

    while "/Who" in s:
        s = s.replace("/Who", getWho(chat_id).title(), 1)

    while "/who" in s:
        s = s.replace("/who", getWho(chat_id), 1)

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

def is_valid_text_overwrite(s):
    theString = s.lower()
    valid = "/who" in theString
    valid = valid or ("/me " in theString or "/me." in theString or theString.endswith("/me"))
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

def whoDefine(chat_id, messageText):
    theText = messageText[len("/whodefine "):].replace(", ", ",")
    wholeTextArray = re.split(r'[,*]', theText)
    fieldnames = ['who']
    if len(messageText) > len("/whodefine "):
        with open("chatStorage/" + str(chat_id) + "whoArray.csv", "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for who in wholeTextArray:
                writer.writerow({'who': who})
        return True
    else:
        with open("chatStorage/" + str(chat_id) + "whoArray.csv", "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return False
