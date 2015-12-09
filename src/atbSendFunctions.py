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


def sendText(bot, chat_id, messageText, replyingMessageID=0, keyboardLayout=[], killkeyboard=True):
    bot.sendChatAction(chat_id=chat_id, action='typing')
    try:
        print messageText + " at " + str(chat_id)
    except Exception:
        print "Sent something with weird characters to " + str(chat_id)

    if replyingMessageID != 0:
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_to_message_id=replyingMessageID, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))
    elif keyboardLayout != []:
        print "tried sending keyboard"
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardMarkup(keyboard=keyboardLayout, one_time_keyboard=True, resize_keyboard=True))
    else:
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))

def sendPhoto(bot, chat_id, imagePath):
    bot.sendChatAction(chat_id=chat_id, action='upload_photo')
    print "Sending picture to " + str(chat_id)
    bot.sendPhoto(chat_id=chat_id, photo=open(imagePath, "rb"))

def sendSticker(bot, chat_id, sticker):
    bot.sendChatAction(chat_id=chat_id, action='typing')
    print "Sending sticker to " + str(chat_id)
    bot.sendSticker(chat_id=chat_id, sticker=open(sticker, "rb"))
