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

menu = ("Please select an option from the list below:\n"
        "1. View all\n"
        "2. View logged in\n"
        "3. View logged out\n"
        "4. Manual Login/out\n"
        "5. Log all out\n"
        "6. Cancel\n\n")

day = raw_input("What day is today? ")
if day.lower() == "saturday":
    while True:
        week = raw_input("What week number (spelled out)?")
        if week in('one', 'two', 'three', 'four', 'five', 'six'):
            break;
        else:
            print "Error in week number"
os.system('clear')            
print "Please scan your card..."
string = ''

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
while True:
    #continuously loops scanning for a card until it receives a value
    #string = ''
    string = ser.read(12)
    string = string[1:11]
    
    if len(string) == 0:
        continue
    else:
        #tagId of master card used to log all out.
        if string in('8800295F4D', '88002AC92D', '88002AC3D9', '0F03040D6F'):
            os.system('clear')
            while True:
                try:
                    choice = int(raw_input(menu))
                    if choice in (1,2,3,4,5,6):
                        break
                    else:
                        print "Invalid input, please enter an integer from 1-6."
                except ValueError:
                    print "Invalid input, please enter an integer from 1-6."

            os.system('clear')

            if choice == 1:
                mysql.viewAll()
                temp = raw_input("Press enter to continue")
            elif choice == 2:
                mysql.viewIn()
                temp = raw_input("Press enter to continue")
            elif choice == 3:
                mysql.viewOut()
                temp = raw_input("Press enter to continue")
            elif choice == 4:
                print "Manual Log\n\n"
                first = raw_input("First name: ")
                last = raw_input("Last name: ")
                mysql.manualLog(first,last)
                temp = raw_input("Press enter to continue")
            elif choice == 5:
                if day.lower() == "saturday":
                    mysql.endWeek(week.lower())
                else:
                    mysql.logAllOut()
                    break
            else:
                os.system('clear')
            os.system('clear')
            print "Please wait..."
            while len(string) != 0:
            string = ser.read(12)
            os.system('clear')
            print "Please scan your card..."

                
            
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
