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

        # add button

        self.button1 = QPushButton(self)
        self.button1.setText("Generate")
        self.button1.setFont(QFont('Overpass'))
        self.button1.move(100, 250)

        self.button1.clicked.connect(self.addAnime)

    def addAnime(self):
        self.setCursor(QCursor(Qt.WaitCursor))
        self.button1.setEnabled(False)
        worker = Worker(self.doAddAnime)
        worker.signals.result.connect(self.handleResult)
        self.threadpool.start(worker)

    def doAddAnime(self):
        user = self.textbox1.text()

        p_factor_data = getPFactorData(user)

        updateSheets(p_factor_data)

    def handleResult(self):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.button1.setEnabled(True)
        QMessageBox.information(
            self, "APL Alert", "Anime data added successfully!")


if __name__ == '__main__':
    import sys
    from PyQt5.QtCore import QThreadPool

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    window.threadpool = QThreadPool()

    sys.exit(app.exec_())
