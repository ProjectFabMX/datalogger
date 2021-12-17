# python3
# read data from Denver S-2002 scale via RS232/serial and write into csv file
import serial
import csv
from datetime import datetime


#port = '/dev/ttyACM0'
port = 'COM7'
csvFile = './data.csv'
useTestData = True

ser = None
if useTestData:
    ser = open('testdata.txt')
else:
    serial.Serial(port)
    ser.flushInput()

f = open(csvFile, 'w')
writer = csv.writer(f)
writer.writerow(["Timestamp", "Mass", "stable"])

print("Reading data from %s ..." % (port))
print("Saving to %s ..." % (csvFile))

while True:
    try:
        line = ser.readline().decode("ascii").replace("\n","").replace("\r","")
        timestamp = datetime.now().isoformat()
        #print (line)
        if len(line) > 10:
            try:
                valueStr = line[:10].replace("+","").replace(" ","")
                value = float(valueStr) # try to convert, if error, skip line
                stable = line[10:].strip()
                writer.writerow([timestamp, valueStr, stable])
                #print("%s, %s, %s" % (timestamp, valueStr, stable))
            except:
                pass        
    except:        
        break