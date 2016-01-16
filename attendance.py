#Program to continuously read from Raspberry Pi Serial Port
#Uses Parallax RFID reader
#Dylan Gaines
#12/21/2015
#Thunder Chickens 217
#dcgaines@mtu.edu


import serial
import mysql
import time

day = raw_input("What day is today? ")

string = ''

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=15)
while True:
    #continuously loops scanning for a card until it receives a value
    ser.read(12)
    string = ser.read(12)
    string = string[1:11]
    
    if len(string) == 0:
        print "Please scan your card..."
        continue
    else:
        #tagId of master card used to log all out.
        if string == '0F03040D6F':
            print "Logging all out"
            if day.lower() == "saturday":
                mysql.endWeek()
            else:
                mysql.logAllOut()
                break
        else:
            #checks if student is currently logged in or out
            status = mysql.getInOut(string)

            if status == 0:
                #if student is out, log them in
                print "Hello "+mysql.getName(string)
                print "Logging In..."
                mysql.logIn(string)
                print "Logged In!"
                time.sleep(5)
                
            elif status == 1:
                #if student is in log them out
                print "Goodbye "+mysql.getName(string)
                print "Logging Out..."
                mysql.logOut(string)
                print "Logged Out!"
                time.sleep(5)
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
