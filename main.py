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
thLight = 500
thWater = 200
lightTime = (6,17)  #hour
waterTime = (5,18) # hour

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
figure = plot.figure(num=None, figsize=(18, 7), dpi=70, facecolor='w', edgecolor='k')
ax_t = figure.add_subplot(2,2,1)
ax_h = figure.add_subplot(2,2,2)
ax_l = figure.add_subplot(2,2,3)
ax_w = figure.add_subplot(2,2,4)

powerT="OFF"
powerH="OFF"
powerL="OFF"
powerW="OFF"

i = 0
while True:
    data = readSerial()
    #bg = cv2.imread("bgplant.jpg")

    if(data != ""):
        dataList = data.split(",")
        for dataValue in dataList:
            if(dataValue!=""):
                now = datetime.now()
                dataTime = now.strftime("%H:%M:%S")
                hourNow = int(now.strftime("%H"))
                sType, sValue, sPower = dataValue.split(":")

                if(sType=="T"):
                    tList = inputData(tList, float(sValue), plotLength)
                    timeList_t = inputData(timeList_t, dataTime, plotLength)
                    powerT="ON" if sPower==1 else "OFF"

                elif(sType=="H"):
                    hList = inputData(hList, float(sValue), plotLength)
                    timeList_h = inputData(timeList_h, dataTime, plotLength)
                    powerH="ON" if sPower==1 else "OFF"

                elif(sType=="L"):
                    lList = inputData(lList, int(sValue), plotLength)
                    timeList_l = inputData(timeList_l, dataTime, plotLength)
                    powerL="ON" if sPower==1 else "OFF"

                    if(hourNow<=lightTime[1] and hourNow>=lightTime[0]):
                        if(int(sValue)<thLight and int(sPower)==0):
                            #--> a: power on ligher, b: power off light, c: power on water, d: power off water
                            Serial.write("a".encode())
                            print("Power on the Light.")
                    else:
                        if(int(sPower)==1):
                            Serial.write("b".encode())
                            print("Power on the Light.")

                elif(sType=="W"):
                    sValue = 1024 - int(sValue)
                    wList = inputData(wList, int(sValue), plotLength)
                    timeList_w = inputData(timeList_w, dataTime, plotLength)
                    powerW="ON" if sPower==1 else "OFF"

                    if(int(sValue)<thWater and int(sPower)==0):
                        Serial.write("c".encode())
                        print("Power on the water.")

                # draw a cardinal sine plot
                x = np.array (timeList_t )
                y = np.array (tList)
                ax_t.cla()
                ax_t.set_ylim(0, 80)
                ax_t.set_title("Temperature (C)")
                ax_t.plot ( x, y )

                x = np.array (timeList_h )
                y = np.array (hList)
                ax_h.cla()
                ax_h.set_title("Humandity (%)")
                ax_h.set_ylim(0, 100)
                ax_h.plot ( x, y )

                x = np.array (timeList_l )
                y = np.array (lList)
                ax_l.cla()
                ax_l.set_title("Lightness (degree)")
                ax_l.set_ylim(0, 1024)
                ax_l.plot ( x, y )

                x = np.array (timeList_w )
                y = np.array (wList)
                ax_w.cla()
                ax_w.set_title("Water (degree)")
                ax_w.set_ylim(0, 1024)
                ax_w.plot ( x, y )


                figure.canvas.draw()
                # convert canvas to image
                img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
                img  = img.reshape(figure.canvas.get_width_height()[::-1] + (3,))
                # img is rgb, convert to opencv's default bgr
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

                #matplotlib.pyplot.show()
                bg = cv2.imread("bgplant.jpg")
                bg[290:290+490, 85:85+1260] = img
                cv2.putText(bg, str(lightTime[0])+":00~"+str(lightTime[1])+":00", (760, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,0,0), 3)
                cv2.putText(bg, str(thLight), (1290, 140), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0,0,255), 3)
                cv2.putText(bg, str(waterTime[0])+":00~"+str(waterTime[1])+":00", (760, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,0,0), 3)
                cv2.putText(bg, str(thWater), (1290, 206), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0,0,255), 3)

                if(len(tList)>0):
                    cv2.putText(bg, str(tList[len(tList)-1])+"C", (146, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(hList)>0):
                    cv2.putText(bg, str(hList[len(hList)-1])+"%", (310, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(lList)>0):
                    cv2.putText(bg, str(lList[len(lList)-1]), (476, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)
                if(len(wList)>0):
                    cv2.putText(bg, str(wList[len(wList)-1]), (656, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0), 2)

                #color=(0,0,0) if powerL=="ON" else (0,0,255)
                color = (powerL=="ON") and (0,0,255) or (255,0,0)
                cv2.putText(bg, powerL, (753, 257), cv2.FONT_HERSHEY_COMPLEX, 1.3,  color, 2)
                #color=(0,0,0) if powerW=="ON" else (0,0,255)
                color = (powerW=="ON") and (0,0,255) or (255,0,0)
                cv2.putText(bg, powerL, (1118, 257), cv2.FONT_HERSHEY_COMPLEX, 1.3, color, 2)

                cv2.imshow("Planting", bg)

                print(img.shape, hourNow)
                cv2.waitKey(1)

    i += 1
