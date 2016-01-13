#Program to continuously read from Raspberry Pi Serial Port
#Uses Parallax RFID reader
#Dylan Gaines
#12/21/2015
#Thunder Chickens 217
#dcgaines@mtu.edu


import serial
import mysql

day = input("What day is today? ")



ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
while True:
    #continuously loops scanning for a card until it receives a value
    string = ser.read(12)   
    if len(string) == 0:
        print "Please scan your card..."
        continue
    else:
        #Interface with mysql server - reference Attendance.py and mysql.py for
        #proper interface syntax

        #tagId of master card used to log all out.
        if string == 'AAAAAAAAAAAA':
            print "Logging all out"
            if day == "Saturday" || day == "saturday":
                mysql.endWeek()
            else
                mysql.logAllOut()
                break
        else:
            #checks if student is currently logged in or out
            status = mysql.getInOut(string)

            if status == 0:
                #if student is out, log them in
                print "Hello "+mysql.getName(string)
                print "Logging In..."
                mysql.login(string)
                print "Logged In!"
                
            elif status == 1:
                #if student is in log them out
                print "Goodbye "+mysql.getName(string)
                print "Logging Out..."
                mysql.logout(string)
                print "Logged Out!"
            else:
                #status will only ever be 0 or 1
                print "Something went wrong blame mechanical"

        #test code
#        if string == '0415DB18A3':
#            print "You used your black tag"
#        elif string == '0F03028F57':
#            print "You used your white tag"
#        else:
#            print "You do not have a valid tag"
