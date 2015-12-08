import csv
from pydblite import Base

def convertcsv2db(csvpath, dbpath): #Converts a CSV file to a PyDBLite database
    db = Base(dbpath)
    try:
        csvfile = open(csvpath, 'rb')
    except csv.Error:
        print "Could not open CSV file at " + csvpath + "\n"
    reader = csv.reader(csvfile)
    header = reader.next()
    try:
        db.create(*header)
    except IOError:
        print "Existing DB at " + dbpath + "\n"
    for row in reader:
        db.insert(*row)
    db.commit()

def printdb(dbpath): #Prints the contents of a PyDBLite database to the console
    db = Base(dbpath)
    if db.exists():
        db.open()
        for obj in db:
            print obj
            print "\n"
    else:
        print "The database does not exist.\n"
