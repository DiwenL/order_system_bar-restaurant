import sys
import time
from PyQt5.QtCore import *
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from create_UI import *
from receipt import *
from order import *


class Main(QMainWindow, MainUI):

    def __init__(self):
        super(Main, self).__init__()

        # init favour selection window
        self.fwindow = self.FavourSelectionWindow()
        self.fwindow.create_favour_btns()

        # init beer amount selection window
        self.bwindow = self.BeerAmountWindow()
        self.bwindow.create_amount_btns()

        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        self.btn_favour.clicked.connect(self.btn_favour_clicked)
        self.btn_beer_amount.clicked.connect(self.btn_beer_amount_clicked)
        for btn_name in self.fwindow.favour_btns:
            btn = self.fwindow.favour_btns[btn_name]
            btn.clicked.connect(lambda ch,btn = btn: print("clicked-->%s" % btn.text()))


    def btn_exit_clicked(self):
        try:
            reply = QMessageBox.question(self, "Exit", "Sure to exit?", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
        except Exception as e:
            print(e)

        if reply == QMessageBox.Yes:
            self.MainWindow.close()

        return

    def btn_favour_clicked(self):
        self.fwindow.show()
        return

    def btn_beer_amount_clicked(self):
        self.bwindow.show()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Main()
    myWin.MainWindow.showFullScreen()
    myWin.MainWindow.show()

    sys.exit(app.exec_())
