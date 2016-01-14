#Program to Test RFID reader

import serial
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)

print "yes hello"
print "this is a test of print"
print "might need a main def"

while True:
    string = ser.read(12)
    if len(string) != 0:
        print string
