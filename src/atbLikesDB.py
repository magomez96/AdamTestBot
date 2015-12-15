import traceback
import telegram
from pydblite import Base

def handleLikes(isLiking, currentMessage):
    try:
        db = Base('chatStorage/likes/likes.pdl') #The path to the database
        db.create('userID', 'likes', 'dislikes', 'history', 'liked', mode="open")  # Create a new DB if one doesn't exist. If it does, open it
        #get disliked comment ID
        likedID = currentMessage.reply_to_message.message_id
        likeReceivedID = currentMessage.reply_to_message.from_user.id
        #check if likedID is in user's liked history
        passedCheck = True
        isLikingSelf = int(likeReceivedID) == int(currentMessage.from_user.id)
        if isLikingSelf:
            passedCheck = False
        if passedCheck:
            if db(userID=currentMessage.from_user.id):
                liker = db(userID=currentMessage.from_user.id).pop()
            else:
                liker = ""
            if db(userID=likeReceivedID):
                liked = db(userID=likeReceivedID).pop()
            else:
                liked = ""
            if liker and likedID not in liker['history'] and liked:
                hist = liker['history']
                hist += " " + likedID
                db.update(liker, history=hist)
                lik = liker['liked']
                tmpLikes = liked['likes']
                tmpDis = liked['dislikes']
                if isLiking:
                    tmpLikes = int(tmpLikes) + 1
                    db.update(liked, likes=tmpLikes)
                    lik += " " + "t"
                else:
                    tmpDis = int(tmpDis) + 1
                    db.update(liked, dislikes=tmpDis)
                    lik += " " + "f"
                db.update(liker, liked=lik)
            elif liker and not liked:
                hist = liker['history']
                hist += " " + likedID
                db.update(liker, history=hist)
                lik = liker['liked']
                if isLiking:
                    db.insert(likeReceivedID, 1, 0, "", "")
                    lik += " " + "t"
                else:
                    db.insert(likeReceivedID, 0, 1, "", "")
                    lik += " " + "f"
                db.update(liker, liked=lik)
            elif not liker and liked:
                if isLiking:
                    tmpLikes = liked['likes']
                    db.insert(currentMessage.from_user.id, 0, 0, likedID, 't')
                    tmpLikes = int(tmpLikes) + 1
                    db.update(liked, likes=tmpLikes)
                else:
                    tmpDis = liked['dislikes']
                    db.insert(currentMessage.from_user.id, 0, 0, likedID, 'f')
                    tmpDis = int(tmpDis) + 1
                    db.update(liked, dislikes=tmpDis)
            elif not liker and not liked:
                if isLiking:
                    db.insert(currentMessage.from_user.id, 0, 0, likedID, 't')
                    db.insert(likeReceivedID, 1, 0, "", "")
                else:
                    db.insert(currentMessage.from_user.id, 0, 0, likedID, 'f')
                    db.insert(likeReceivedID, 0, 1, "", "")
            db.commit()
    except Exception:
        print traceback.format_exc()

def likes(currentMessage):
    try:
        db = Base('chatStorage/likes/likes.pdl') #The path to the database
        db.create('userID', 'likes', 'dislikes', 'history', 'liked', mode="open") #Create a new DB if one doesn't exist. If it does, open it
        sentMyKarma = False
        try:
            likes = 0
            dislikes = 0
            if int(currentMessage.reply_to_message.from_user.id) == int(117924410): #is replying to bot message with /likes
                for user in db:
                    if int(user['userID']) == 117924410:
                        likes = int(user['likes'])
                        dislikes = int(user[dislikes])
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
            for user in db:
                if(int(user['userID']) == int(currentMessage.from_user.id)):
                    userWasFound = True
                    likes = int(user['likes'])
                    dislikes = int(user['dislikes'])

            if userWasFound:
                return currentMessage.from_user.first_name + ", you have " + str(likes) + " likes and " + str(dislikes) + " dislikes, for a total of " + str(int(likes) - int(dislikes)) + " karma."
            else:
                return "No like data found!"
    except Exception:
        print traceback.format_exc()
        return ""
