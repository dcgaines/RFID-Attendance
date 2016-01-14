#Script to initialize table in database with names and tag IDs of students
#Dylan Gaines
#12/20/2015
#ThunderChickens 217
#dcgaines@mtu.edu


import MySQLdb
import serial

db = MySQLdb.connect(host="localhost", user="user", passwd="chickens", db="HOURS")
cur = db.cursor()
another = "yes"
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)

while another=="yes":
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    tag = ""
    while len(tag) == 0:
        tag = ser.read(12)
    print tag
    cur.execute("INSERT INTO hours (tagId, first, last, status, hoursToday, hoursThisWeek) VALUES (%s, %s, %s, 0, 0, 0)", tag, first, last)
    db.commit()
    another = input("Input another? (yes, no, deleteLast): ")
    if another == "deleteLast":
       cur.execute("DELETE FROM hours WHERE tagId = %s", tag)
       db.commit()
       another = input("Input another? (yes, no): ")

db.close()
print "All Done!"
