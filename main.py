# -*- coding: utf-8 -*-
import sys, time
from datetime import datetime
import serial
import cv2
import imutils
import numpy as np
import matplotlib.pyplot

Serial = serial.Serial("/dev/ttyS0", 9600, timeout= 0.5 )

plotLength = 200

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

figure = matplotlib.pyplot.figure(num=None, figsize=(16, 4), dpi=80, facecolor='w', edgecolor='k')
plot   = figure.add_subplot ( 111 )

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

while True:
    data = readSerial()

    if(data != ""):
        dataList = data.split(",")
        for dataValue in dataList:
            if(dataValue!=""):
                print(dataValue)
                now = datetime.now()
                dataTime = now.strftime("%H:%M:%S")
                sType, sValue = dataValue.split(":")
                print("Split:", sType ,sValue )

                if(sType=="T"):
                    tList = inputData(tList, float(sValue), plotLength)
                    timeList_t = inputData(timeList_t, dataTime, plotLength)
                elif(sType=="H"):
                    hList = inputData(hList, float(sValue), plotLength)
                    timeList_h = inputData(timeList_h, dataTime, plotLength)
                elif(sType=="L"):
                    lList = inputData(hList, int(sValue), plotLength)
                    timeList_l = inputData(timeList_l, dataTime, plotLength)
                elif(sType=="W"):
                    wList = inputData(hList, int(sValue), plotLength)
                    timeList_w = inputData(timeList_w, dataTime, plotLength)

                # draw a cardinal sine plot
                x = np.array (timeList_t )
                y = np.array (tList)
                print(x)
                print(y)
                plot.plot ( x, y )

                figure.canvas.draw()
                # convert canvas to image
                img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
                img  = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
                # img is rgb, convert to opencv's default bgr
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

                #matplotlib.pyplot.show()
                cv2.imshow("TEST", img)
                cv2.waitKey(1)
