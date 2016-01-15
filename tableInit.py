#Script to initialize table in database with names and tag IDs of students
#Dylan Gaines
#12/20/2015
#ThunderChickens 217
#dcgaines@mtu.edu

#!/usr/bin/python

import MySQLdb
import serial

db = MySQLdb.connect(host="localhost", user="user", passwd="chickens", db="HOURS")
cur = db.cursor()
another = "yes"
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
delete_statement = "DELETE FROM hours WHERE tagId = %s"
insert_statement = "INSERT INTO hours (tagId, first, last, status, hoursToday, hoursThisWeek) VALUES (%s, %s, %s, 0, 0, 0)"

while another=="yes":
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    tag = ""
    while len(tag) == 0:
        tag = ser.read(10)
    tag = string.strip(tag)
    print tag
    data = (tag, first, last)
    cur.execute(insert_statement, data)
    db.commit()
    another = raw_input("Input another? (yes, no, deleteLast): ")
    if another == "deleteLast":
       cur.execute(delete_statement, tag)
       db.commit()
       another = input("Input another? (yes, no): ")

db.close()
print "All Done!"
