#Program to Test RFID reader

import serial
ser = serial.Serial('dev/ttyAMA0', 2400, timeout=1)
while True:
    string = ser.read(12)
    if len(string) != 0:
        print string
