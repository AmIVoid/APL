from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import os
import json
from pFactor import getPFactorData
from sheets import updateSheets


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()

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
        self.textbox1.resize(280, 25)

        # start button

        self.button1 = QPushButton('Start', self)
        self.button1.move(20, 200)
        self.button1.setGeometry(20, 200, 280, 30)

        self.button1.clicked.connect(self.APLGui)

        self.show()

    def APLGui(self):

        user = self.textbox1.text()

        msgBox = QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon('icon.ico'))
        msgBox.setText("Updated spreadsheet data.")
        msgBox.setWindowTitle("APL Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)

        p_factor_data = getPFactorData(user)

        updateSheets(p_factor_data)

        msgBox.exec()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
