#Program to continuously read from Raspberry Pi Serial Port
#Uses Parallax RFID reader
#Dylan Gaines
#12/21/2015
#Thunder Chickens 217
#dcgaines@mtu.edu


import serial
import mysql
import time
import os

day = raw_input("What day is today? ")
if day.lower() == "saturday":
    while True:
        week = raw_input("What week number (spelled out)?")
        if week in('one', 'two', 'three', 'four', 'five', 'six'):
            break;
        else:
            print "Error in week number"
            
print "Please scan your card..."
string = ''

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
while True:
    #continuously loops scanning for a card until it receives a value
    #string = ''
    string = ser.read(12)
    string = string[1:11]
    
    if len(string) == 0:
        #print "Please scan your card..."
        continue
    else:
        #tagId of master card used to log all out.
        if string in('8800295F4D', '88002AC92D', '88002AC3D9', '0F03040D6F'):
            print "Logging all out"
            if day.lower() == "saturday":
                mysql.endWeek(week.lower())
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
                print "\n\nPlease Wait..."
                time.sleep(7)
                os.system('clear')
                print "Please wait..."
                while len(string) != 0:
                    string = ser.read(12)
                os.system('clear')
                print "Please scan your card..."
                
            elif status == 1:
                #if student is in log them out
                print "Goodbye "+mysql.getName(string)
                print "Logging Out..."
                mysql.logOut(string)
                print "Logged Out!"
                print "\n\nPlease Wait..."
                time.sleep(7)
                os.system('clear')
                print "Please wait..."
                while len(string) != 0:
                    string = ser.read(12)
                os.system('clear')
                print "Please scan your card..."
            else:
                #status will only ever be 0 or 1
                print "Something went wrong blame mechanical"
