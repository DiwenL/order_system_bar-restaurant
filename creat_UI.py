import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Creat_UI(object):
    def setupUI(self,MainWindow):
        MainWindow.setObjectName("Cupar Bar Order System")  # set window's name
        MainWindow.resize(1920, 1080)  # set windows size

        _translate = QtCore.QCoreApplication.translate

        self.font_list = []
        for i in range(1, 31):
            font = QtGui.QFont()
            font.setPointSize(i)
            self.font_list.append(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)  # set main widget
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)  # set tab widget
        self.tabWidget.setGeometry(QtCore.QRect(920, 0, 1000, 1000))  # set tab widget size
        self.tabWidget.setFont(self.font_list[24])
        self.tabWidget.setObjectName("tab_menu")

        self.tab_list = {}
        self.toolbox_list = {}

    def creat_tabs(self,menu_list) -> None:
        for menu in menu_list:
            tab = QtWidgets.QWidget()
            name = "tab_%s" % menu
            tab.setObjectName(name)
            self.tab_list[name] = tab
        return