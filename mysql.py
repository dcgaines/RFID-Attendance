#Script with functions to interface with the SQL database to log hours
#Dylan Gaines
#12/21/2015
#ThunderChickens 217
#dcgaines@mtu.edu

import MySQLdb
import datetime

select_name = "SELECT first,last FROM hours WHERE tagId = %(tag)s"
select_status = "SELECT status FROM hours WHERE tagId = %(tag)s"
log_in_status = "UPDATE hours SET status = 1 WHERE tagId = %(tag)s"
log_in_time = "UPDATE hours SET timeIn = NOW() WHERE tagId = %(tag)s"
select_hours = "SELECT hoursToday,hoursThisWeek FROM hours WHERE tagId = %(tag)s"
log_out_status = "UPDATE hours SET status = 0 WHERE tagId = %(tag)s"
log_out_time = "UPDATE hours SET timeOut = NOW() WHERE tagId = %(tag)s"
hours_today = "UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(timeOut, timeIn)) WHERE tagId = %(tag)s"
hours_this_week = "UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(timeOut, timeIn)) WHERE tagId = %(tag)s"
manual_log = "SELECT tagId FROM hours WHERE last = %s and first = %s"
busLogIn = "UPDATE hours SET status = 1 WHERE tagId = %(tag)s"
select_session = "SELECT TIMEDIFF(timeOut,timeIn) FROM hours WHERE tagId = %(tag)s"

def connect():
    # Mysql connection setup. Insert your values here
    return MySQLdb.connect(host="localhost", user="root", passwd="chickens", db="HOURS")

def getName(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute(select_name, {'tag' : tagId})
    row = cur.fetchone()
    db.close()
    if(row==None):
        return "Invalid ID, try again"
    else:
        return row[0]+" "+row[1]

def getInOut(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute(select_status,{'tag' : tagId})
    #1 is in, 0 is out
    inOut = cur.fetchone()
    status = int(inOut[0])
    db.close()
    return status

def logIn(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute(log_in_status,{'tag' : tagId})
    db.commit()
    cur.execute(log_in_time,{'tag' : tagId})
    db.commit()
    cur.execute(select_hours,{'tag' : tagId})
    hrs = cur.fetchone()
    db.close()
    print "You have %s today and %s this week." % (hrs[0], hrs[1])

def logOut(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute(select_session,{'tag' : tagId})
    time = cur.fetchone()
    if time < 5:
        print "Error 2 talk to Dylan"
        return 0
    cur.execute(log_out_status,{'tag' : tagId})
    db.commit()
    cur.execute(log_out_time,{'tag' : tagId})
    db.commit()
    cur.execute(hours_today,{'tag' : tagId})
    db.commit()
    cur.execute(hours_this_week,{'tag' : tagId})
    db.commit()
    cur.execute(select_hours,{'tag' : tagId})
    hrs = cur.fetchone()
    db.close()
    print "You have %s today and %s this week." % (hrs[0], hrs[1])
    return 1

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
    
def endWeek(week):
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
    if week == 1:        
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekOne.csv'")
    elif week == 2:
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekTwo.csv'")
    elif week == 3:
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekThree.csv'")
    elif week == 4:
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekFour.csv'")
    elif week == 5:
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekFive.csv'")
    elif week == 6:
        cur.execute("SELECT * FROM hours INTO OUTFILE '/tmp/weekSix.csv'")
    else:
        print "Uh oh"
    cur.execute("UPDATE hours SET hoursThisWeek = 0")
    db.commit()
    cur.execute("UPDATE hours SET hoursToday = 0")
    db.commit()
    db.close()
    print ("All logged out. Hours saved. Have a good night!")

def viewAll():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(NOW(), timeIn)) WHERE status = 1")
    cur.execute("UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(NOW(), timeIn)) WHERE status = 1")
    cur.execute("UPDATE hours SET timeIn = NOW() WHERE status = 1")
    db.commit()
    cur.execute("SELECT * FROM hours")
    rows = cur.fetchall()
    desc = cur.description
    print "%s\t\t%s\t\t%s\t\t%s\t%s\t%s\n" % (desc[0][0],desc[1][0],desc[2][0],desc[3][0],desc[6][0],desc[7][0])
    for row in rows:
        if len(row[1]) <= 7:
            if len(row[2]) <= 7:
                print "%s\t%s\t\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])    
        else:
            if len(row[2]) <= 7:
                print "%s\t%s\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])        


    db.close()

def viewIn():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET hoursToday = ADDTIME(hoursToday, TIMEDIFF(NOW(), timeIn)) WHERE status = 1")
    cur.execute("UPDATE hours SET hoursThisWeek = ADDTIME(hoursThisWeek, TIMEDIFF(NOW(), timeIn)) WHERE status = 1")
    cur.execute("UPDATE hours SET timeIn = NOW() WHERE status = 1")
    cur.execute("SELECT * FROM hours WHERE status = 1")
    rows = cur.fetchall()
    desc = cur.description
    print "%s\t\t%s\t\t%s\t\t%s\t%s\t%s\n" % (desc[0][0],desc[1][0],desc[2][0],desc[3][0],desc[6][0],desc[7][0])
    for row in rows:
        if len(row[1]) <= 7:
            if len(row[2]) <= 7:
                print "%s\t%s\t\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])    
        else:
            if len(row[2]) <= 7:
                print "%s\t%s\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])        


    db.close()

def viewOut():
    db = connect()
    cur = db.cursor()
    cur.execute("SElECT * FROM hours WHERE status = 0")
    rows = cur.fetchall()
    desc = cur.description
    print "%s\t\t%s\t\t%s\t\t%s\t%s\t%s\n" % (desc[0][0],desc[1][0],desc[2][0],desc[3][0],desc[6][0],desc[7][0])
    for row in rows:
        if len(row[1]) <= 7:
            if len(row[2]) <= 7:
                print "%s\t%s\t\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])    
        else:
            if len(row[2]) <= 7:
                print "%s\t%s\t%s\t\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7]) 
            else:
                print "%s\t%s\t%s\t%s\t%s\t\t%s" % (row[0],row[1],row[2],row[3],row[6],row[7])        

    db.close()
    
def manualLog(f,l):
    db = connect()
    cur = db.cursor()
    name = (l,f)
    cur.execute(manual_log,name)
    tagId = cur.fetchone()
    status = getInOut(tagId)
    if status == 0:
        logIn(tagId)
        print "Logged In\n"
    else:
        logOut(tagId)
        print "Logged Out\n"
    print "Bring your card next time!"
    db.close()

def busMode():
    db = connect()
    cur = db.cursor()
    print "Present"
    cur.execute("SELECT * FROM hours WHERE status = 1")
    rows = cur.fetchall()
    desc = cur.description
    print "%s\t\t%s\n" % (desc[1][0],desc[2][0])
    for row in rows:
        if len(row[1]) <= 7:
            print "%s\t\t%s" % (row[1],row[2])
        else:
            print "%s\t%s" % (row[1],row[2])

    print "\nMissing"
    cur.execute("SELECT * FROM hours WHERE status = 0")
    rows = cur.fetchall()
    desc = cur.description
    print "%s\t\t%s\n" % (desc[1][0],desc[2][0])
    for row in rows:
        if len(row[1]) <= 7:
            print "%s\t\t%s" % (row[1],row[2])
        else:
            print "%s\t%s" % (row[1],row[2])
    db.close()

def busIn(tagId):
    db = connect()
    cur = db.cursor()
    cur.execute(busLogIn, {'tag' : tagId})
    db.commit()
    db.close()
    
def busReset():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET status = 0 WHERE status = -1")
    db.commit()
    db.close()

def busNotPresent():
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE hours SET status = -1 WHERE status = 0")
    db.commit()
    cur.execute("UPDATE hours SET status = 0 WHERE status = 1")
    db.commit()
    db.close()

def manualBus(f, l):
    db = connect()
    cur = db.cursor()
    name = (l,f)
    cur.execute(manual_log,name)
    tagId = cur.fetchone()
    cur.execute(log_in_status, {'tag' : tagId})
    db.commit()
    print "BRING YOUR CARD!"
    db.close()
