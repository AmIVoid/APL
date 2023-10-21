import json
import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QCursor
from pFactor import getPFactorData
from sheets import updateSheets


class WorkerSignals(QObject):
    result = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        result = self.fn()
        self.signals.result.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anime Priority List v2")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(810, 290, 300, 350)
        self.setFixedSize(320, 300)

        # title label

        self.label1 = QLabel(self)
        self.label1.setText("AniList User")
        self.label1.setFont(QFont('Overpass'))
        self.label1.move(1, -1)
        self.label1.setAlignment(Qt.AlignCenter)

        # anilist user input

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(20, 20)
        self.textbox1.resize(280, 25)

        # sheet id label

        self.label2 = QLabel(self)
        self.label2.setText("Spreadsheet ID")
        self.label2.setFont(QFont('Overpass'))
        self.label2.move(8, 48)
        self.label2.setAlignment(Qt.AlignCenter)

        # sheet id input

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 70)
        self.textbox2.resize(280, 25)

        # generate button

        self.button1 = QPushButton(self)
        self.button1.setText("Generate")
        self.button1.setFont(QFont('Overpass'))
        self.button1.move(20, 170)
        self.button1.resize(160, 40)

        self.button1.clicked.connect(self.addAnime)

        # save

        self.button2 = QPushButton('Save data', self)
        self.button2.move(200, 160)

        self.button2.clicked.connect(self.saveCreds)

        # clear

        self.button3 = QPushButton('Clear data', self)
        self.button3.move(200, 200)

        self.button3.clicked.connect(self.clearCreds)

        if os.path.exists('userdata.json'):
            with open('userdata.json') as f:
                data = json.load(f)

            anilist = data["Anilist"]
            spreadsheet = data["Spreadsheet"]

            self.textbox1.setText(anilist)
            self.textbox2.setText(spreadsheet)

    def addAnime(self):
        self.setCursor(QCursor(Qt.WaitCursor))
        self.button1.setEnabled(False)
        worker = Worker(self.doAddAnime)
        worker.signals.result.connect(self.handleResult)
        self.threadpool.start(worker)

    def doAddAnime(self):
        user = self.textbox1.text()
        sheetId = self.textbox2.text()

        p_factor_data = getPFactorData(user)

        updateSheets(p_factor_data, sheetId)

    def handleResult(self):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.button1.setEnabled(True)
        QMessageBox.information(
            self, "APL Alert", "Anime data added successfully!")

    def saveCreds(self):

        pre = {"Anilist": self.textbox1.text(
        ), "Spreadsheet": self.textbox2.text()}
        jsonData = json.dumps(pre)

        with open("userdata.json", "w") as userdata:
            userdata.write(jsonData)

    def clearCreds(self):

        if os.path.exists("userdata.json"):
            os.remove("userdata.json")
            self.textbox1.setText("")
            self.textbox2.setText("")
        else:
            print("File doesn't exist")


if __name__ == '__main__':
    import sys
    from PyQt5.QtCore import QThreadPool

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    window.threadpool = QThreadPool()

    sys.exit(app.exec_())
