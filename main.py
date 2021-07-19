import sys
import time
from PyQt5.QtCore import forcepoint, right
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from order_system_UI import *
from receipt import *
from order import *

class Main(QMainWindow, Ui_Form):

    def __init__(self, parent=True):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.btnLis1 = [self.btn1_1, self.btn1_2, self.btn1_3,
                        self.btn1_4, self.btn1_5, self.btn1_6,
                        self.btn1_7, self.btn1_8, self.btn1_9,
                        self.btn1_10, self.btn1_11]

        self.btnLis2 = [self.btn2_1, self.btn2_2, self.btn2_3,
                        self.btn2_4, self.btn2_5, self.btn2_6,
                        self.btn2_7, self.btn2_8, self.btn2_9,
                        self.btn2_10, self.btn2_11, self.btn2_12]

        self.btnLis3 = [self.btn3_1, self.btn3_2, self.btn3_3,
                        self.btn3_4, self.btn3_5, self.btn3_6,
                        self.btn3_7, self.btn3_8, self.btn3_9,
                        self.btn3_10, self.btn3_11, self.btn3_12]

        self.btnLis4 = [self.btn4_1, self.btn4_2, self.btn4_3,
                        self.btn4_4, self.btn4_5, self.btn4_6,
                        self.btn4_7, self.btn4_8, self.btn4_9,
                        self.btn4_10, self.btn4_11, self.btn4_12]

        # init btns checkable -> True and visible -> False
        for btn_lis in [self.btnLis1, self.btnLis2,
                        self.btnLis3, self.btnLis4]:
            for btn in btn_lis:
                btn.setCheckable(True)
                btn.setVisible(False)

        # setting font for Order list & Receipt list
        self.list_order.setFont(self.font)
        self.list_receipt.setFont(self.font)
