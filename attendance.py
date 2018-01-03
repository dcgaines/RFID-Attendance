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
        "6. Reset Bus Mode\n"
        "7. Cancel\n\n")

os.system('clear')            
print "Please scan your card..."
string = ''

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)
while True:
    #continuously loops scanning for a card until it receives a value

    while len(string) != 12:
	string = ser.read(12)
	if "\n" in string[1:11]:
		string = ""
    string = string[1:11]
    
    
    
    
    #tagId of master card used to log all out.
    if string in('8800295F4D', '88002AC92D', '88002AC3D9', '0F03040D6F', '88002BDE26'):
        os.system('clear')
        while True:
            try:
                choice = int(raw_input(menu))
                if choice in (1,2,3,4,5,6,7):
                    break
                else:
                    print "Invalid input, please enter an integer from 1-7."
            except ValueError:
                print "Invalid input, please enter an integer from 1-7."

        os.system('clear')

        if choice == 1:
            mysql.viewAll()
            temp = raw_input("\nPress enter to continue")
        elif choice == 2:
            mysql.viewIn()
            temp = raw_input("\nPress enter to continue")
        elif choice == 3:
            mysql.viewOut()
            temp = raw_input("\nPress enter to continue")
        elif choice == 4:
            print "Manual Log\n\n"
            while True:
                try:
                    first = raw_input("First name: ")
                    last = raw_input("Last name: ")
                    mysql.manualLog(first,last)
                    break
                except Exception:
                    print "That is not a valid name"
            temp = raw_input("Press enter to continue")
        elif choice == 5:
            end = raw_input("Is this the end of the week? (yes/no)")
            if day.lower() == "yes":
                while True:
                    week = int(raw_input("What week number? "))
                    if week in(1,2,3,4,5,6):
                        break
                    else:
                        print "Error in week number"
                mysql.endWeek(week)
                break
            else:
                mysql.logAllOut()
                break
        elif choice == 6:
            mysql.busReset()
        else:
            os.system('clear')
        os.system('clear')
        print "Please wait..."
        while len(string) != 0:
            string = ser.read(12)
        os.system('clear')
        print "Please scan your card..."

    #card to view all hours    
    elif string == '88002A5CBD':
        os.system('clear')
        mysql.viewAll()
        temp = raw_input("\nPress Enter to continue.")
        os.system('clear')
        print "Please wait..."
        while len(string) != 0:
            string = ser.read(12)
        os.system('clear')
        print "Please scan your card..."
            
    #Card for bus mode
    elif string == '88002BE876':
        done = 0
        while True:
            os.system('clear')
            print "Bus Mode \n"
            mysql.busMode()
            print "\nPlease wait..."
            while len(string) != 0:
                string = ser.read(12)
            print "\nPlease scan your card..."
            while True:
                string = ser.read(12)
                string = string[1:11]
   
                if len(string) == 0:
                    continue
                    
                #Bus card again sets all missing to not present for
                #this competition (status = -1) and ends script
                elif string == '88002BE876':
                    mysql.busNotPresent()
                    done = 1
                    break
                elif string in ('8800295F4D', '88002AC92D', '88002AC3D9', '0F03040D6F', '88002BDE26'):
                    os.system('clear')
                    print "Who forgot their card?"
                    while True:
                        try:
                            first = raw_input("First name: ")
                            last = raw_input("Last name: ")
                            mysql.manualBus(first,last)
                            break
                        except Exception:
                            print "That is not a valid name"

                    temp = raw_input("Press Enter to continue")
                    break
                else:
                    mysql.busIn(string)
                    break
            if done == 1:
                break
        break
                    
            
    else:
        #checks if student is currently logged in or out
        try:
	    print "scanned"
            status = mysql.getInOut(string)
        except Exception:
            continue
        if status == -1:
            print "Tell Cameron to reset bus mode"
            time.sleep(5)
            os.system('clear')
            print "Please wait..."
            while len(string) != 0:
                string = ser.read(12)
            os.system('clear')
            print "Please scan your card..."
                
        elif status == 0:
            #if student is out, log them in
            print "Hello "+mysql.getName(string)
            print "Logging In..."
            mysql.logIn(string)
            print "Logged In!"
            print "\n\nPlease Wait..."
            time.sleep(5)
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
            if mysql.logOut(string) == 1:
                print "Logged Out!"
                print "\n\nPlease Wait..."
            else:
                print "Error talk to Dylan"
            time.sleep(5)
            os.system('clear')
            print "Please wait..."
            while len(string) != 0:
                    string = ser.read(12)
            os.system('clear')
            print "Please scan your card..."
        else:
            #status will only ever be 0 or 1 or -1
            print "Something went wrong blame mechanical"
