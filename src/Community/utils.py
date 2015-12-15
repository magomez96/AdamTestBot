import csv
import os
from pydblite import Base

def convertcsv2db(csvpath, dbpath): #Converts a CSV file to a PyDBLite database
    db = Base(dbpath)
    try:
        csvfile = open(csvpath, 'rb')
    except csv.Error:
        print("Could not open CSV file at " + csvpath + "\n")
    reader = csv.reader(csvfile)
    header = next(reader)
    try:
        db.create(*header)
    except IOError:
        print("Existing DB at " + dbpath + "\n")
    for row in reader:
        db.insert(*row)
    db.commit()

def printdb(dbpath): #Prints the contents of a PyDBLite database to the console
    db = Base(dbpath)
    if db.exists():
        db.open()
        retstr = ""
        for obj in db:
            retstr += str(obj)
            retstr += "\n"
        print(retstr)
        return retstr
    else:
        print("The database does not exist or is corrupt.\n")
def likeconvert(likesRoot):
    histPath = likesRoot + '/history'
    convertcsv2db(likesRoot + '/totals.csv', likesRoot + '/likes.pdl')
    db = Base(likesRoot + '/likes.pdl')
    db.open()
    db.add_field('history', "")
    db.add_field('liked', "")
    dirContents = os.listdir(histPath)
    histFiles = []

    for File in dirContents:
        if ".csv" in File:
            histFiles.append(File)
    for histFile in histFiles:
        try:
            csvfile = open(histPath + '/' + histFile, 'rb')
            reader = csv.DictReader(csvfile)
            for row in reader:
                if histFile.endswith('history.csv'):
                    recName = histFile[:-11]
                    print(recName)
                if db(userID=recName):
                    rec = db(userID=recName).pop()
                    if not rec['liked']:
                        db.update(rec, liked=row['liked'])
                    else:
                        tmpLiked = rec['liked']
                        tmpLiked += " " + row['liked']
                        db.update(rec, liked=tmpLiked)
                    if not rec['history']:
                        db.update(rec, history=row['messageID'])
                    else:
                        tmpHist = rec['history']
                        tmpHist += " " + row['messageID']
                        db.update(rec, history=tmpHist)
                db.commit()
        except csv.Error:
                print("Could not open CSV file")
