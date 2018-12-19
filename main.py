# https://qoppac.blogspot.de/2017/03/interactive-brokers-native-python-api.html
# Quandl () API Key: Cx2fdHrAxaddRisxcSzm

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize

from controller import MainWindowController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    form = MainWindowController.MainWindowClass()
    form.show()
    app.exec_()


