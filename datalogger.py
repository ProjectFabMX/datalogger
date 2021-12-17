# python3
# read data from Denver S-2002 scale via RS232/serial and write into csv file
import serial
import csv
from datetime import datetime


#port = '/dev/ttyACM0'
port = 'COM7'
timestamp = datetime.now().isoformat().replace(":","_")
csvFile = './data_' + timestamp + '.csv'
useTestData = False



class DataReader:
    def __init__(self, useTestData):
        self.useTestData = useTestData
        if self.useTestData:
            self.ser = open('testdata.txt')
            print('Reading test data')   
        else:
            print("Reading data from %s ..." % (port))
            self.ser = serial.Serial(port)
            self.ser.flushInput()

    def readLine(self):
        if self.useTestData:
            line = self.ser.readline()
            if not line:
                raise Exception("end of file")
        else:
            line = self.ser.readline().decode("ascii")
        line = line.strip("\n\r ")
        return line

class DataLogger:
    def __init__(self, csvFile, reader):
        self.csvFile = csvFile
        self.reader = reader

    def run(self):        
        f = open(self.csvFile, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Mass", "stable"])

        print("Saving to %s ..." % (csvFile))

        while True:
            try:
                line = self.reader.readLine()
                timestamp = datetime.now().isoformat()
                #print (line)
                if len(line) >= 10:
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

reader = DataReader(useTestData)
dataLogger = DataLogger(csvFile, reader)
dataLogger.run()
