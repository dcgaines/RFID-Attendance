#Script to initialize table in database with names and tag IDs of students
#Dylan Gaines
#12/20/2015
#ThunderChickens 217
#dcgaines@mtu.edu

#!/usr/bin/python

import MySQLdb
import serial

db = MySQLdb.connect(host="localhost", user="root", passwd="chickens", db="HOURS")
cur = db.cursor()
another = "yes"
tag = ''
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
delete_statement = "DELETE FROM hours WHERE tagId = %(tag)s"
insert_statement = "INSERT INTO hours (tagId, first, last, status, hoursToday, hoursThisWeek) VALUES (%s, %s, %s, 0, 0, 0)"
update_statement = "UPDATE hours SET tagId = %(newTag)s WHERE tagId = %(oldTag)s"

while another=="yes":
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    while len(tag) != 0:
        tag = ser.read(12)
    print "Scan: "
    while len(tag) != 12:
        tag = ser.read(12)
	if "\n" in tag[1:11]:
		tag = ""
    tag = tag[1:11]
    print tag
    ser.read(12)
    data = (tag, first, last)
    cur.execute(insert_statement, data)
    db.commit()
    another = raw_input("Input another? (yes, no, rescan, deleteLast): ")
    if another == "deleteLast":
       cur.execute(delete_statement, { 'tag': tag })
       db.commit()
       another = raw_input("Input another? (yes, no): ")
    while another == "rescan":
	old = tag
	while len(tag) != 0:
		tag = ser.read(12)
        print "Scan: "
	while len(tag) != 12:
		tag = ser.read(12)
		if "\n" in tag:
			tag = ""
	tag = tag[1:11]
	print tag
	ser.read(12)
	cur.execute(update_statement, { 'oldTag' : old, 'newTag' : tag } )
	db.commit()
	another = raw_input("Input another? (yes, no, rescan): ")

db.close()
print "All Done!"
