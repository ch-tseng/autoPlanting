# -*- coding: utf-8 -*-
import sys, time
from datetime import datetime
import serial
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plot

Serial = serial.Serial("/dev/ttyS0", 9600, timeout= 0.5 )

plotLength = 8

tList = []
hList = []
lList = []
wList = []
timeList_t = []
timeList_h = []
timeList_l = []
timeList_w = []

def inputData(arrayName, data, length):
    if(len(arrayName)>length):
        arrayName.pop(0)

    arrayName.append(data)

    return arrayName

def readSerial():
    recv = ""
    dataString = ""
    count = Serial.inWaiting()
    if count != 0:
        recv = Serial.read(count).decode('utf-8')
        if(recv == "["):
            while recv != "]":
                if Serial.inWaiting():
                    recv = Serial.read(count).decode('utf-8')
                    if(recv!="]"):
                        dataString += recv

                    time.sleep(0.1)

    return dataString


#plot.figure()
figure = plot.figure(num=None, figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
ax_t = figure.add_subplot(2,2,1)
ax_t.set_title("Temperature (C)")
ax_h = figure.add_subplot(2,2,2)
ax_h.set_title("Humandity (%)")
ax_l = figure.add_subplot(2,2,3)
ax_l.set_title("Lightness (degree)")
ax_w = figure.add_subplot(2,2,4)
ax_w.set_title("Water (degree)")

i = 0
while True:
    data = readSerial()

    if(data != ""):
        dataList = data.split(",")
        for dataValue in dataList:
            if(dataValue!=""):
                now = datetime.now()
                dataTime = now.strftime("%H:%M:%S")
                sType, sValue = dataValue.split(":")
                #print(sType, sValue)

                if(sType=="T"):
                    tList = inputData(tList, float(sValue), plotLength)
                    timeList_t = inputData(timeList_t, dataTime, plotLength)

                elif(sType=="H"):
                    hList = inputData(hList, float(sValue), plotLength)
                    timeList_h = inputData(timeList_h, dataTime, plotLength)
                elif(sType=="L"):
                    lList = inputData(lList, int(sValue), plotLength)
                    timeList_l = inputData(timeList_l, dataTime, plotLength)
                elif(sType=="W"):
                    wList = inputData(wList, int(sValue), plotLength)
                    timeList_w = inputData(timeList_w, dataTime, plotLength)

                # draw a cardinal sine plot
                x = np.array (timeList_t )
                y = np.array (tList)
                ax_t.plot ( x, y )

                x = np.array (timeList_h )
                y = np.array (hList)
                ax_h.plot ( x, y )

                x = np.array (timeList_l )
                y = np.array (lList)
                ax_l.plot ( x, y )

                x = np.array (timeList_w )
                y = np.array (wList)
                ax_w.plot ( x, y )


                figure.canvas.draw()
                # convert canvas to image
                img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
                img  = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
                # img is rgb, convert to opencv's default bgr
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                print("LEN",len(wList))

                #matplotlib.pyplot.show()
                cv2.imshow("TEST", img)
                cv2.waitKey(1)

    i += 1
