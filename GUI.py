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


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.signals.result.emit(result)
        self.signals.finished.emit()


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

        # add button

        self.button1 = QPushButton(self)
        self.button1.setText("Add")
        self.button1.setFont(QFont('Overpass'))
        self.button1.move(100, 250)

        self.button1.clicked.connect(self.addAnime)

    def addAnime(self):
        worker = Worker(self.doAddAnime)
        worker.signals.result.connect(self.handleResult)
        self.threadpool.start(worker)

    def doAddAnime(self):
        user = self.textbox1.text()

        p_factor_data = getPFactorData(user)

        updateSheets(p_factor_data)

        msgBox = QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon('icon.ico'))
        msgBox.setText("Updated spreadsheet data.")
        msgBox.setWindowTitle("APL Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def handleResult(self, result):
        print(result)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
