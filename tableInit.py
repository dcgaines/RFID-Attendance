#Script to initialize table in database with names and tag IDs of students
#Dylan Gaines
#12/20/2015
#ThunderChickens 217
#dcgaines@mtu.edu

#!/usr/bin/python

import MySQLdb
import serial

db = MySQLdb.connect(host="localhost", user="root", passwd="obfuscate", db="HOURS")
cur = db.cursor()
another = "yes"
tag = ''
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
delete_statement = "DELETE FROM hours WHERE tagId = %s"
insert_statement = "INSERT INTO hours (tagId, first, last, status, hoursToday, hoursThisWeek) VALUES (%s, %s, %s, 0, 0, 0)"

while another=="yes":
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    while len(tag) != 0:
        tag = ser.read(12)
    while len(tag) == 0:
        tag = ser.read(12)
    tag = tag[1:11]
    print tag
    ser.read(12)
    data = (tag, first, last)
    cur.execute(insert_statement, data)
    db.commit()
    another = raw_input("Input another? (yes, no, deleteLast): ")
    if another == "deleteLast":
       cur.execute(delete_statement, tag)
       db.commit()
       another = raw_input("Input another? (yes, no): ")

db.close()
print "All Done!"
