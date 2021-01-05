from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import os
import json
from pFactor import getPFactorData, getRelations
from sheets import updateSheets

class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 

        title = "Anime Priority List"
        self.setWindowTitle(title) 
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(810, 290, 300, 350) 
        self.setFixedSize(320, 300)
        self.UiComponents() 
        self.show()

    def UiComponents(self):
        
        # anilist user label
        
        self.label1 = QLabel(self)
        self.label1.setText("AniList User")
        self.label1.setFont(QFont('Overpass'))
        self.label1.move(1, -1)
        self.label1.setAlignment(Qt.AlignCenter)
        
        # anilist user input
        
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(20, 20)
        self.textbox1.resize(280,25)
        
        # sheet id label
        
        self.label2 = QLabel(self)
        self.label2.setText("Spreadsheet ID")
        self.label2.setFont(QFont('Overpass'))
        self.label2.move(8, 48)
        self.label2.setAlignment(Qt.AlignCenter)
        
        # sheet id input
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 70)
        self.textbox2.resize(280,25)
        
        # raw data label
        
        self.label3 = QLabel(self)
        self.label3.setText("Sheet Name")
        self.label3.setFont(QFont('Overpass'))
        self.label3.move(2, 98)
        self.label3.setAlignment(Qt.AlignCenter)
        
        # raw data input
        
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(20, 120)
        self.textbox3.resize(280,25)
        
        # start button
        
        self.button1 = QPushButton('Start', self)
        self.button1.move(20,200)
        self.button1.setGeometry(20, 200, 160, 30)
        
        self.button1.clicked.connect(self.APLGui)
        
        # save
        
        self.button2 = QPushButton('Save data', self)
        self.button2.move(200,160)
        
        self.button2.clicked.connect(self.saveCreds)
        
        # clear
        
        self.button3 = QPushButton('Clear data', self)
        self.button3.move(200,200)
        
        self.button3.clicked.connect(self.clearCreds)
        
        # credentials
        
        self.label4 = QLabel(self)
        self.label4.setText("credentials.json:")
        self.label4.setFont(QFont('Overpass', 10))
        self.label4.move(20, 160)
        self.label4.setAlignment(Qt.AlignCenter)
        
        self.label5 = QLabel(self)
        self.label5.setText("Not Found")
        self.label5.setStyleSheet("color: red;")
        self.label5.setFont(QFont('Overpass', 10))
        self.label5.move(100, 160)
        self.label5.setAlignment(Qt.AlignCenter)
        
        if os.path.exists('userdata.json'):
            with open('userdata.json') as f:
                data = json.load(f)
            
            anilist = data["Anilist"]
            spreadsheet = data["Spreadsheet"]
            sheet = data["Sheet"]
            
            self.textbox1.setText(anilist)
            self.textbox2.setText(spreadsheet)
            self.textbox3.setText(sheet)
        
        self.show()
        
        while not os.path.exists('credentials.json'):
            QApplication.processEvents()
            time.sleep(0.01)
        
        if os.path.exists('credentials.json'):
            QApplication.processEvents()
            self.label5.setStyleSheet("color: green;")
            self.label5.setText("Found")
            self.label5.move(100, 160)
        
    def APLGui(self):

        user = self.textbox1.text()
        sheetId = self.textbox2.text()
        sheetName = self.textbox3.text()
        
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon('icon.ico'))
        msgBox.setText("Updated spreadsheet data.")
        msgBox.setWindowTitle("APL Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        
        
        if os.path.exists('userdata.json'):
            with open('userdata.json') as f:
                data = json.load(f)
            
            user = data["Anilist"]
            sheetId = data["Spreadsheet"]
            sheetName = data["Sheet"]

        QApplication.processEvents()
        time.sleep(0.5)
        
        p_factor_data = getPFactorData(user)
        
        QApplication.processEvents()
        time.sleep(0.5)

        updateSheets(sheetId, sheetName, p_factor_data)
        
        msgBox.exec()
        
    def saveCreds(self):
        
        pre = {"Anilist": self.textbox1.text(), "Spreadsheet": self.textbox2.text(), "Sheet": self.textbox3.text()}
        jsonData = json.dumps(pre)
        
        with open("userdata.json", "w") as userdata:
           userdata.write(jsonData)
           
    def clearCreds(self):
        if os.path.exists("userdata.json"):
            os.remove("userdata.json")
            self.textbox1.setText("")
            self.textbox2.setText("")
            self.textbox3.setText("")
        else:
            print("File doesn't exist")
    
App = QApplication(sys.argv) 
window = Window()
sys.exit(App.exec())