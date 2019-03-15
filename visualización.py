import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QRadioButton, QDialog,QRadioButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QUrl
import easygui as eg
import pandas as pd
from matplotlib.dates import date2num, DateFormatter
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import datetime
from mapsplotlib import mapsplot as mplt
import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Cansat(QMainWindow):
    infile = ""
    path = 'c:\data\det\*.csv'
    cansat = ""
    mensaje = "Waiting for data"

    def __init__(self):
        super().__init__()
        textLabel = QLabel(self)
        Font = QtGui.QFont("Times", 20, QFont.Bold)
        textLabel.setText("Simple Space Data Visualization")
        textLabel.setFont(Font)
        textLabel.move(200,10)
        textLabel.adjustSize()



        textLabel1 = QLabel(self)
        Font1 = QtGui.QFont("Times", 12)
        textLabel1.setText("Select the file to be displayed and the type of CanSat")
        textLabel1.setFont(Font1)
        textLabel1.move(225,90)
        textLabel1.adjustSize()

        button1 = QPushButton(self)
        button1.setText("File")
        button1.move(20,200)
        button1.clicked.connect(lambda: self.SubirArchivo())


        self.textLabel2 = QLabel(self)
        Font2 = QtGui.QFont("Times", 12)
        self.textLabel2.setText(self.path)
        self.textLabel2.setFont(Font2)
        self.textLabel2.move(130,205)
        self.textLabel2.adjustSize()

        self.b1 = QRadioButton(self)
        self.b1.setText("Cansat Simple-2")
        self.b1.adjustSize()

        self.b1.move(200,300)
        self.b1.toggled.connect(lambda:self.CansatState(self.b1))

        self.b2 = QRadioButton(self)
        self.b2.setText("Cansat Simple-3")
        self.b2.adjustSize()
        self.b2.move(500,300)
        self.b2.toggled.connect(lambda: self.CansatState(self.b2))

        button2 = QPushButton(self)
        button2.setText("Data Preprocessing")
        button2.move(330,500)
        button2.adjustSize()
        button2.clicked.connect(lambda: self.DataValidation())

        self.textLabel3 = QLabel(self)
        Font3 = QtGui.QFont("Times", 12)
        self.textLabel3.setText(self.mensaje)
        self.textLabel3.setFont(Font3)
        self.textLabel3.move(335,550)
        self.textLabel3.adjustSize()


        self.setGeometry(50,50,800,600)
        self.setWindowTitle("Simple Space Data Visualization")

        self.show()

    def SubirArchivo(self):
        self.infile = eg.fileopenbox(msg='Please locate the csv file',
                    title='Specify File', default='c:\data\det\*.CSV',
                    filetypes='*.csv')
        self.path = self.infile
        self.textLabel2.setText(self.path)
        self.textLabel2.adjustSize()

    def CansatState(self, cansat):
         if cansat.text() == "Cansat Simple-2":
             if cansat.isChecked() == True:
                self.cansat = "2"
         if cansat.text() == "Cansat Simple-3":
             if cansat.isChecked() == True:
                self.cansat = "3"
         print(self.cansat)

    def DataValidation(self):
        if (self.path != 'c:\data\det\*.csv' or len(self.path) < 1) and (self.cansat == "2" or self.cansat == "3"):
            self.mensaje = "File and CanSat selected"
            self.textLabel3.move(310,550)
            self.Graficacion()


        else:
            self.mensaje = "Please select a file and a type of CanSat"
            self.textLabel3.move(280,550)

        self.textLabel3.setText(self.mensaje)
        self.textLabel3.adjustSize()

    def Graficacion(self):
        ventana = Graficacion(self.cansat, self.path).exec_()


class Graficacion(QDialog):

    cansat = ""
    file = ""
    TimeLabel = "Time [UTC-5]"

    def __init__(self, cansat, file):
        super().__init__()
        self.cansat = cansat
        self.file = file
        self.Preprocessing()

        textLabel = QLabel(self)
        Font = QtGui.QFont("Times", 20, QFont.Bold)
        textLabel.setText("Simple Space Data Visualization Simple-" + self.cansat)
        textLabel.setFont(Font)
        textLabel.move(200,10)
        textLabel.adjustSize()

        textLabel1 = QLabel(self)
        Font1 = QtGui.QFont("Times", 12)
        textLabel1.setText("Please select the grpahic that you want to generate for the CanSat")
        textLabel1.setFont(Font1)
        textLabel1.move(225,90)
        textLabel1.adjustSize()

        self.b8 = QRadioButton(self)
        self.b8.setText("Time vs CO")
        self.b8.adjustSize()
        self.b8.move(650,200)
        self.b8.toggled.connect(lambda:self.COvsTime(self.b8))

        self.b5 = QRadioButton(self)
        self.b5.setText("Time vs NO2")
        self.b5.adjustSize()
        self.b5.move(450,200)
        self.b5.toggled.connect(lambda:self.NO2vsTime(self.b5))

        self.b6 = QRadioButton(self)
        self.b6.setText("Time vs NH3")
        self.b6.adjustSize()
        self.b6.move(250,200)
        self.b6.toggled.connect(lambda:self.NH3vsTime(self.b6))

        self.b7 = QRadioButton(self)
        self.b7.setText("Time vs H2")
        self.b7.adjustSize()
        self.b7.move(50,200)
        self.b7.toggled.connect(lambda:self.H2vsTime(self.b7))

        self.b10 = QRadioButton(self)
        self.b10.setText("All gases vs Time - 1")
        self.b10.adjustSize()
        self.b10.move(450,300)
        self.b10.toggled.connect(lambda:self.GasesvsTime_1(self.b10))

        self.b15 = QRadioButton(self)
        self.b15.setText("All gases vs Time - 2")
        self.b15.adjustSize()
        self.b15.move(650,300)
        self.b15.toggled.connect(lambda:self.GasesvsTime_2(self.b15))

        self.b9 = QRadioButton(self)
        self.b9.setText("All data vs Time")
        self.b9.adjustSize()
        self.b9.move(250,300)
        self.b9.toggled.connect(lambda:self.DatavsTime(self.b9))

        self.b21 = QRadioButton(self)
        self.b21.setText("Geoposition")
        self.b21.adjustSize()
        self.b21.move(50,300)
        self.b21.toggled.connect(lambda:self.GPS(self.b21))

        self.b11 = QRadioButton(self)
        self.b11.setText("Time vs CH4")
        self.b11.adjustSize()
        self.b11.move(450,250)
        self.b11.toggled.connect(lambda:self.CH4vsTime(self.b11))

        self.b12 = QRadioButton(self)
        self.b12.setText("Time vs C3H8")
        self.b12.adjustSize()
        self.b12.move(250,250)
        self.b12.toggled.connect(lambda:self.C3H8vsTime(self.b12))

        self.b13 = QRadioButton(self)
        self.b13.setText("Time vs C4H10")
        self.b13.adjustSize()
        self.b13.move(650,250)
        self.b13.toggled.connect(lambda:self.C4H10vsTime(self.b13))

        self.b14 = QRadioButton(self)
        self.b14.setText("Time vs C2H6OH")
        self.b14.adjustSize()
        self.b14.move(50,250)
        self.b14.toggled.connect(lambda:self.C2H6OHvsTime(self.b14))

        self.b1 = QRadioButton(self)
        self.b1.setText("Time vs Pressure")
        self.b1.adjustSize()
        self.b1.move(650,350)
        self.b1.toggled.connect(lambda:self.PressurevsTime(self.b1))

        self.b2 = QRadioButton(self)
        self.b2.setText("Time vs Humidity")
        self.b2.adjustSize()
        self.b2.move(450,350)
        self.b2.toggled.connect(lambda:self.HumidityvsTime(self.b2))

        self.b3 = QRadioButton(self)
        self.b3.setText("Time vs Temperature")
        self.b3.adjustSize()
        self.b3.move(250,350)
        self.b3.toggled.connect(lambda:self.TemperaturevsTime(self.b3))

        self.b4 = QRadioButton(self)
        self.b4.setText("Time vs Altitude")
        self.b4.adjustSize()
        self.b4.move(50,350)
        self.b4.toggled.connect(lambda:self.AltitudevsTime(self.b4))

        self.b20 = QRadioButton(self)
        self.b20.setText("Aceleration vs Time")
        self.b20.adjustSize()
        self.b20.move(50,400)
        self.b20.toggled.connect(lambda:self.AcelvsTime(self.b20))

        self.b19 = QRadioButton(self)
        self.b19.setText("Altitude vs CO")
        self.b19.adjustSize()
        self.b19.move(650,450)
        self.b19.toggled.connect(lambda:self.AltitudevsCO(self.b19))

        self.b18 = QRadioButton(self)
        self.b18.setText("Altitude vs Humidity")
        self.b18.adjustSize()
        self.b18.move(450,450)
        self.b18.toggled.connect(lambda:self.AltitudevsHumidity(self.b18))

        self.b16 = QRadioButton(self)
        self.b16.setText("Altitude vs Pressure")
        self.b16.adjustSize()
        self.b16.move(250,450)
        self.b16.toggled.connect(lambda:self.AltitudevsPressure(self.b16))

        self.b17 = QRadioButton(self)
        self.b17.setText("Altitude vs Temperature")
        self.b17.adjustSize()
        self.b17.move(50,450)
        self.b17.toggled.connect(lambda:self.AltitudevsTemperature(self.b17))

        self.setGeometry(30,40,800,600)
        self.setWindowTitle("Data Preprocessing")
        self.show()

    def Preprocessing(self):
        df = pd.read_csv(self.file)
        if(self.cansat == "2"):
            self.ProcessS2(df)
        elif(self.cansat == "3"):
            self.ProcessS3(df)
    def ProcessS3(self,df):
        self.meanCO=[]
        self.meanCO2=[]
        self.meanNH=[]
        self.meanNH2=[]
        self.meanNO=[]
        self.meanNO2=[]
        self.meanH=[]
        self.meanH2=[]
        self.meanC4H10=[]
        self.meanC3H8=[]
        self.meanCH4=[]
        self.meanC2H5OH=[]
        self.meanC4H102=[]
        self.meanC3H82=[]
        self.meanCH42=[]
        self.meanC2H5OH2=[]
        self.meanTime=[]
        self.meanAcelx = []
        self.meanAcely = []
        self.meanAcelz = []
        r=0
        min = 29

        Time = df['TiempoGPS']
        Time = Time - 50000
        strTime = ["" for x in range(len(Time))]

        for i in range(len(Time)):

            date = str(Time[i])
            sim = 6 - len(date)
            if sim > 0:
                ceros = '0'
                for a in range(sim-1):
                    ceros += '0'
                date = ceros + date

            hora = date[0:2]
            minuto = date[2:4]
            segundo = date[4:6]
            strTime[i] = hora + ":" + minuto + ":" + segundo
        df['TiempoGPS'] = strTime

        vPCB = df['TempPcbI2CVital'];
        vPCB = vPCB/100

        for i in range(len(vPCB)):
            if(vPCB[i] < 0):
                vPCB[i] = vPCB[i] + 255
                vPCB[i] = vPCB[i] * -1
        df['TempPcbI2CVital'] = vPCB


        vPCB = df['TempPcbI2CGases'];
        vPCB = vPCB/100
        for i in range(len(vPCB)):
            if(vPCB[i] < 0):
                vPCB[i] = vPCB[i] + 255
                vPCB[i] = vPCB[i] * -1
        df['TempPcbI2CGases'] = vPCB

        self.Time = df['TiempoGPS']
        self.a_1 = df['AltitudGPS']
        self.a_2 = df['BAR-ALTI']
        self.co = df['CO']
        self.nh = df['NH3']
        self.no = df['NO2']
        self.h2 = df['H2']
        self.c4h10 = df['C4H10']
        self.c3h8 = df['C3H8']
        self.ch4 = df['CH4']
        self.c2h5oh = df['C2H5OH']
        self.co2 = df['CO-2']
        self.nh2 = df['NH3-2']
        self.no2 = df['NO2-2']
        self.h22 = df['H2-2']
        self.c4h102 = df['C4H10-2']
        self.c3h82 = df['C3H8-2']
        self.ch42 = df['CH4-2']
        self.c2h5oh2 = df['C2H5OH-2']
        self.t1=df['BAR-TEMP']
        self.t2=df['TempPcbI2CVital']
        self.t3=df['SHT11-TEMP']
        self.p=df['BAR-PRES']
        self.h = df['SHT11-HUME']
        self.longitud = df['Longitud*10000']
        self.latitud = df['Latitud*10000']
        self.acelx = df['ACC-X']
        self.acely = df['ACC-Y']
        self.acelz = df['ACC-Z']

        self.t1 = self.t1 / 100
        self.t3 = self.t3/100
        self.h = self.h /100
        self.longitud = self.longitud/1000
        self.latitud = self.latitud/1000

        while r < len(self.Time):

            self.meanCO.append(np.mean([np.mean(self.co[r:(r+min)]),np.mean(self.co2[r:(r+min)])]))
            self.meanNH.append(np.mean([np.mean(self.nh[r:(r+min)]),np.mean(self.nh2[r:(r+min)])]))
            self.meanNO.append(np.mean([np.mean(self.no[r:(r+min)]),np.mean(self.no2[r:(r+min)])]))
            self.meanH.append(np.mean([np.mean(self.h2[r:(r+min)]),np.mean(self.h22[r:(r+min)])]))
            self.meanC4H10.append(np.mean([np.mean(self.c4h10[r:(r+min)]),np.mean(self.c4h102[r:(r+min)])]))
            self.meanC3H8.append(np.mean([np.mean(self.c3h8[r:(r+min)]),np.mean(self.c3h82[r:(r+min)])]))
            self.meanCH4.append(np.mean([np.mean(self.ch4[r:(r+min)]),np.mean(self.ch42[r:(r+min)])]))
            self.meanC2H5OH.append(np.mean([np.mean(self.c2h5oh[r:(r+min)]),np.mean(self.c2h5oh2[r:(r+min)])]))
            self.meanAcelx.append(np.mean(self.acelx[r:(r+min)]))
            self.meanAcely.append(np.mean(self.acely[r:(r+min)]))
            self.meanAcelz.append(np.mean(self.acelz[r:(r+min)]))

            self.meanTime.append(self.Time[r])
            r+=min



    def ProcessS2(self, df):

        self.meanCO=[]
        self.meanNH=[]
        self.meanNO=[]
        self.meanH=[]
        self.meanC4H10=[]
        self.meanC3H8=[]
        self.meanCH4=[]
        self.meanC2H5OH=[]
        self.meanTime=[]
        self.meanAcelx=[]
        self.meanAcely=[]
        self.meanAcelz = []

        r=0
        min = 29

        Time = df['TiempoGPS']
        Time = Time - 50000
        strTime = ["" for x in range(len(Time))]

        for i in range(len(Time)):
            date = str(Time[i])
            sim = 6 - len(date)
            if sim > 0:
                ceros = '0'
                for a in range(sim-1):
                    ceros += '0'
                date = ceros + date

            hora = date[0:2]
            minuto = date[2:4]
            segundo = date[4:6]
            strTime[i] = hora + ":" + minuto + ":" + segundo
        df['TiempoGPS'] = strTime

        vPCB = df['TempPcbI2CVital'];
        vPCB = vPCB/100

        for i in range(len(vPCB)):
            if(vPCB[i] < 0):
                vPCB[i] = vPCB[i] + 255
                vPCB[i] = vPCB[i] * -1
        df['TempPcbI2CVital'] = vPCB

        self.Time = df['TiempoGPS']
        self.a_1 = df['AltitudGPS']
        self.a_2 = df['BAR-ALTI']
        self.co = df['CO']
        self.nh = df['NH3']
        self.no = df['NO2']
        self.h2 = df['H2']
        self.c4h10 = df['C4H10']
        self.c3h8 = df['C3H8']
        self.ch4 = df['CH4']
        self.c2h5oh = df['C2H5OH']
        self.t1=df['BAR-TEMP']
        self.t2=df['TempPcbI2CVital']
        self.t3=df['SHT11-TEMP']
        self.p=df['BAR-PRES']
        self.h = df['SHT11-HUME']
        self.longitud = df['Longitud*10000']
        self.latitud = df['Latitud*10000']
        self.acelx = df['ACC-X']
        self.acely = df['ACC-Y']
        self.acelz = df['ACC-Z']

        self.t1 = self.t1 / 100
        self.t3 = self.t3/100
        self.h = self.h /100
        self.longitud = self.longitud/1000
        self.latitud = self.latitud/1000

        while r < len(self.Time):

            self.meanCO.append(np.mean(self.co[r:(r+min)]))
            self.meanNH.append(np.mean(self.nh[r:(r+min)]))
            self.meanNO.append(np.mean(self.no[r:(r+min)]))
            self.meanH.append(np.mean(self.h[r:(r+min)]))
            self.meanC4H10.append(np.mean(self.c4h10[r:(r+min)]))
            self.meanC3H8.append(np.mean(self.c3h8[r:(r+min)]))
            self.meanCH4.append(np.mean(self.ch4[r:(r+min)]))
            self.meanC2H5OH.append(np.mean(self.c2h5oh[r:(r+min)]))
            self.meanAcelx.append(np.mean(self.acelx[r:(r+min)]))
            self.meanAcely.append(np.mean(self.acely[r:(r+min)]))
            self.meanAcelz.append(np.mean(self.acelz[r:(r+min)]))
            self.meanTime.append(self.Time[r])
            r+=min


    def PressurevsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.Time
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.p)

            plt.grid(True)
            #plt.legend(loc='best')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")
            if self.cansat == '2':
                plt.title('Simple-2 Pressure')
            elif self.cansat == '3':
                plt.title('Simple-3 Pressure')
            plt.ylabel('Pressure [hPa]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def HumidityvsTime(self, b):
        if b.isChecked() == True:
            Time_list = self.Time
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.h)

            plt.grid(True)
            #plt.legend(loc='best')

            if self.cansat == '2':
                plt.title('Simple-2 Humidity')
            elif self.cansat == '3':
                plt.title('Simple-3 Humidity')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('Humidity [%RH]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def AltitudevsTime(self, b):
        if b.isChecked() == True:
            Time_list = self.Time
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            ax.plot(dt2, self.a_1, label="GPS Altitude [A_1]")
            ax.plot(dt2, self.a_2, label="Barometer Altitude [A_2]")

            plt.grid(True)
            plt.legend(loc='best')

            if self.cansat == '2':
                plt.title('Simple-2 Altitude')
            elif self.cansat == '3':
                plt.title('Simple-3 Altitude')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('Altitude [m]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def TemperaturevsTime(self, b):
        if b.isChecked() == True:
            Time_list = self.Time
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.t1, label="T_1")
            plt.plot(dt2,self.t2, label="T_2")
            plt.plot(dt2,self.t3, label="T_3")


            plt.grid(True)
            plt.legend(loc='best')

            if self.cansat == '2':
                plt.title('Simple-2 Temperature')
            elif self.cansat == '3':
                plt.title('Simple-3 Temperature')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('Temperature [C]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def COvsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanCO)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Carbon Monoxide')
            elif self.cansat == '3':
                plt.title('Simple-3 Carbon Monoxide')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('CO [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def NO2vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanNO)



            plt.grid(True)
            #plt.legend(loc='best'))
            if self.cansat == '2':
                plt.title('Simple-2 Nitrogen Dioxide')
            elif self.cansat == '3':
                plt.title('Simple-3 Nitrogen Dioxide')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('NO2 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def NH3vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanNH)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Ammonia')
            elif self.cansat == '3':
                plt.title('Simple-3 Ammonia')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('NH3 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def H2vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanH)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Dihydrogen')
            elif self.cansat == '3':
                plt.title('Simple-3 Dihydrogen')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('H2 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def CH4vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanCH4)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Methane')
            elif self.cansat == '3':
                plt.title('Simple-3 Methane')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('CH4 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def C3H8vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanC3H8)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Propane')
            elif self.cansat == '3':
                plt.title('Simple-3 Propane')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('C3H8 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def C4H10vsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanC4H10)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Iso-butane')
            elif self.cansat == '3':
                plt.title('Simple-3 Iso-butane')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('C4H10 [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def C2H6OHvsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanC2H5OH)



            plt.grid(True)
            #plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Ethanol')
            elif self.cansat == '3':
                plt.title('Simple-3 Ethanol')

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('C2H6OH [ppm]')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()


    def DatavsTime(self,b):
        if b.isChecked() == True:
            plt.style.use('ggplot')
            Time_list = self.Time
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig = plt.figure()

            ax = fig.add_subplot(2,2,1)

            ax.plot(dt2, self.t1, label="T_1", linewidth=1.5)
            ax.plot(dt2, self.t2, label="T_2", linewidth=1.5)
            ax.plot(dt2, self.t3, label="T_3", linewidth=1.5)

            ax.legend(loc='best')
            plt.xlabel(self.TimeLabel)
            plt.ylabel("Temperature [C] "+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            ax = fig.add_subplot(2,2,2)
            axes = plt.gca()
            #axes.set_ylim([0,2000])
            ax.plot(dt2, self.a_1, label="A_1")
            ax.plot(dt2, self.a_2, label="A_2")
            ax.legend(loc='best')

            plt.xlabel(self.TimeLabel)
            #plt.title("Ammonia")
            plt.ylabel('Altitude [m] '+'S'+self.cansat)

            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            ax = fig.add_subplot(2,2,3)

            ax.plot(dt2,self.h)
            #p = df['Barometer_Pression']
            #ax.plot(dt,p[400:1810] )
            #fig.autofmt_xdate()
            #ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            #fig.title("Altitud vs Tiempo")

            plt.xlabel(self.TimeLabel)
            #plt.title("Nitric Oxide")
            plt.ylabel('RH% '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            #tikz_save("Pre.tex", extra_axis_parameters={'scaled y ticks=false'})
            ax = fig.add_subplot(2,2,4)

            ax.plot(dt2,self.p )

            #fig.autofmt_xdate()
            #ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            #fig.title("Altitud vs Tiempo")

            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('Pressure [hPa] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            #tikz_save("graph.tex", extra_axis_parameters={'scaled y ticks=false'})
            plt.show()

    def GasesvsTime_1(self,b):
        if b.isChecked() == True:

            plt.style.use('ggplot')

            fmt = '%H:%M:%S'
            tseconds = [dt.datetime.strptime(k, fmt) for k in self.meanTime]
            t=tseconds
            dt2 = [(k - t[0]).seconds for k in t]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t
            dt2

            fig = plt.figure()
            ax = fig.add_subplot(2,2,1)

            """ax.plot(dt, t1[400:1810], label="T_1", linewidth=1.5)
            ax.plot(dt, t2[400:1810], label="T_2", linewidth=1.5)
            ax.plot(dt, t3[400:1810], label="T_3", linewidth=1.5)"""
            ax.plot(dt2, self.meanCO)
            plt.ylabel("CO [ppm] "+'S'+self.cansat)
            plt.xlabel(self.TimeLabel)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            ax = fig.add_subplot(2,2,2)
            axes = plt.gca()

            """ax.plot(dt, a_1[400:1810], label="GPS Altitude [A_1]")
            ax.plot(dt, a_2[400:1810], label="BMP180 Altitude [A_2]")"""
            ax.plot(dt2, self.meanNH)


            plt.xlabel(self.TimeLabel)

            plt.ylabel('NH3 [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            ax = fig.add_subplot(2,2,3)

            ax.plot(dt2, self.meanNO)

            plt.xlabel(self.TimeLabel)

            plt.ylabel('NO2 [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            ax = fig.add_subplot(2,2,4)

            ax.plot(dt2,self.meanH,label="Simple-3")

            plt.xlabel(self.TimeLabel)


            plt.ylabel('H2 [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            plt.show()

    def GasesvsTime_2(self,b):
        if b.isChecked() == True:

            plt.style.use('ggplot')

            fmt = '%H:%M:%S'
            tseconds = [dt.datetime.strptime(k, fmt) for k in self.meanTime]
            t=tseconds
            dt2 = [(k - t[0]).seconds for k in t]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t
            dt2

            fig = plt.figure()
            ax = fig.add_subplot(2,2,1)

            """ax.plot(dt, t1[400:1810], label="T_1", linewidth=1.5)
            ax.plot(dt, t2[400:1810], label="T_2", linewidth=1.5)
            ax.plot(dt, t3[400:1810], label="T_3", linewidth=1.5)"""
            ax.plot(dt2, self.meanCH4,label="Simple-3")
            plt.ylabel("CH4 [ppm] "+'S'+self.cansat)
            plt.xlabel(self.TimeLabel)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            ax = fig.add_subplot(2,2,2)
            axes = plt.gca()

            """ax.plot(dt, a_1[400:1810], label="GPS Altitude [A_1]")
            ax.plot(dt, a_2[400:1810], label="BMP180 Altitude [A_2]")"""
            ax.plot(dt2, self.meanC4H10,label="Simple-3")


            plt.xlabel(self.TimeLabel)

            plt.ylabel('C4H10 [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            ax = fig.add_subplot(2,2,3)

            ax.plot(dt2, self.meanC3H8,label="Simple-3")

            plt.xlabel(self.TimeLabel)

            plt.ylabel('C3H8 [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            ax = fig.add_subplot(2,2,4)

            ax.plot(dt2,self.meanC2H5OH,label="Simple-3")

            plt.xlabel(self.TimeLabel)


            plt.ylabel('C2H6OH [ppm] '+'S'+self.cansat)
            plt.grid(True)

            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)

            plt.show()

    def AltitudevsPressure(self,b):
        if b.isChecked() == True:
            plt.plot(self.a_1, self.p)
            plt.title("Altitude vs Pressure")
            plt.ylabel('Pressure [hPa]')
            plt.xlabel('Altitude [m]')
            plt.grid(True)
            plt.show()

    def AcelvsTime(self,b):
        if b.isChecked() == True:
            Time_list = self.meanTime
            fmt = '%H:%M:%S'
            tseconds2 = [dt.datetime.strptime(k, fmt) for k in Time_list]
            t2=tseconds2
            dt2 = [(k - t2[0]).seconds for k in t2]
            dtmax = float(max(dt2))
            dt2 = np.array(dt2) / dtmax
            t2

            fig, ax = plt.subplots()
            plt.plot(dt2,self.meanAcelx,label="ACC-X")
            plt.plot(dt2,self.meanAcely,label="ACC-Y")
            plt.plot(dt2,self.meanAcelz,label="ACC-Z")


            plt.grid(True)
            plt.legend(loc='best')
            if self.cansat == '2':
                plt.title('Simple-2 Aceleration')
            elif self.cansat == '3':
                plt.title('Simple-3 Aceleration')
            plt.xlabel(self.TimeLabel)
            #plt.title("Dihydrogen ")

            plt.ylabel('g')
            fig.canvas.draw()

            labels = plt.xticks()
            print(type(labels[0]))
            labels = [datetime.timedelta(seconds = label * dtmax) + t2[0] for label in labels[0]]
            tlabels = [label.strftime(fmt) for label in labels]
            ax.set_xticklabels(tlabels)
            plt.xticks(rotation = 45)
            plt.show()

    def GPS(self,b):
        if b.isChecked() == True:
            df = pd.DataFrame({'Latitude': self.latitud, 'Longitude': self.longitud})

            lon = df['Longitude']
            lat = df['Latitude']
            map_hooray = folium.Map(location=[lat[0],lon[0]],
                                zoom_start = 11, tiles='stamentoner')

            # Filter the DF for rows, then columns, then remove NaNs

            heat_df = df[['Latitude', 'Longitude']]
            heat_df = heat_df.dropna(axis=0, subset=['Latitude','Longitude'])

            mag = np.array(self.co)
            mag
            maxg = np.max(mag)
            ming = np.min(mag)
            lim = ming + ((maxg-ming)/2)
            maxg
            ming
            lim
            # List comprehension to make out list of lists
            #heat_data = [[row['Latitude'],row['Longitude'],row['CO']] for index, row in heat_df.iterrows()]
            map_hooray.add_child(plugins.HeatMap(zip(lat, lon, mag), radius = 10,  gradient={.9: 'blue', .95: 'lime', 0.98: 'red'}))
            # Plot it on the map
            #HeatMap(heat_data).add_to(map_hooray)
            #map_hooray.save("mapa.html")

            view = QtWebEngineWidgets.QWebEngineView()
            url = "https://www.retrogames.cz/play_022-NES.php?language=EN"
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mapa.html"))
            local_url = QUrl.fromLocalFile(file_path)
            view.load(local_url)

            view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cansat = Cansat()
    sys.exit(app.exec_())
