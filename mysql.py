#Script with functions to interface with the SQL database to log hours
#Dylan Gaines
#12/21/2015
#ThunderChickens 217
#dcgaines@mtu.edu

import MySQLdb
import datetime

def connect():
    # Mysql connection setup. Insert your values here
    return MySQLdb.connect(host="localhost", user="user", passwd="chickens", db="HOURS")

def getName(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT first,last FROM hours WHERE tagId = %s",(tagId))
    row = cur.fetchone()
    db.close()
    if(row==None):
        return "Invalid ID, try again"
    else:
        return row[0]+" "+row[1]

def getInOut(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT status FROM hours WHERE tagId = %s",(tagId))
    #1 is in, 0 is out
    inOut = cur.fetchone()
    db.close()
    return inOut

def logIn(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET status = 1 WHERE tagId = %s", (tagId))
    db.commit()
    cur.exucute("UPDATE hours SET timeIn = NOW() WHERE tagId = %s",(tagId))
    db.commit()
    cur.execute("SELECT hoursToday,hoursThisWeek FROM hours WHERE tagId = %s", (tagId))
    hrs = cur.fetchone()
    db.close()
    print ("You have %s today and %s this week.",(hrs[0], hrs[1])) 

def logOut(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET status = 0 WHERE tagId = %s", (tagId))
    db.commit()
    cur.execute("UPDATE hours SET timeOut = NOW() WHERE tagId = %s", (tagId))
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(timeOut, timeIn)) WHERE tagId = %s", (tagId))
    db.commit()
    cur.execute("UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(timeOut, timeIn)) WHERE tagId = %s", (tagId)")
    db.commit()
    cur.execute("SELECT hoursToday,hoursThisWeek FROM hours WHERE tagId = %s", (tagId))
    hrs = cur.fetchone()
    db.close()
    print ("You have %s today and %s this week.",(hrs[0], hrs[1])) 

def logAllOut():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET timeOut = NOW() WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(timeOut, timeIn)) WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(timeOut, timeIn)) WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET status = 0 WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = 0")
    db.commit()
    db.close()
    print ("All logged out. Have a good night!")
    
def endWeek():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET timeOut = NOW() WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(timeOut, timeIn)) WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(timeOut, timeIn)) WHERE status = 1")
    db.commit()
    cur.execute("UPDATE hours SET status = 0 WHERE status = 1")
    db.commit()
    cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weeklyHours.txt')
    cur.execute("UPDATE hours SET hoursThisWeek = 0")
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = 0")
    db.commit()
    db.close()
    print ("All logged out. Hours saved. Have a good night!")
