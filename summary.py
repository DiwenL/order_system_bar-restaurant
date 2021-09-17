import os
import sys
import datetime
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QCalendarWidget


class SummaryWindow(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setWindowTitle("End of day summary 日结算")  # set window's name
        self.MainWindow.resize(900, 600)  # set windows size

        self.cwindow = CalendarWindow()
        self.cwindow.calwindow.clicked[QDate].connect(self.date_clicked)

        self.summary = Summary()
        self.summary.summarize()

        # font list
        self.font_list = []
        for i in range(1, 31):
            font = QtGui.QFont()
            font.setFamily("Microsoft JhengHei UI")
            font.setPointSize(i)
            self.font_list.append(font)

        self.btn_select_date = QtWidgets.QPushButton(self.MainWindow)
        self.btn_select_date.setObjectName("btn_select_date")
        self.btn_select_date.setText("Select date\n选择日期")
        self.btn_select_date.setGeometry(QtCore.QRect(50, 50, 200, 100))
        self.btn_select_date.setFont(self.font_list[20])
        self.btn_select_date.clicked.connect(self.btn_select_date_clicked)

        self.btn_show_details = QtWidgets.QPushButton(self.MainWindow)
        self.btn_show_details.setObjectName("btn_show_details")
        self.btn_show_details.setText("Receipt Details  小票详情")
        self.btn_show_details.setGeometry(QtCore.QRect(50, 450, 500, 100))
        self.btn_show_details.setFont(self.font_list[20])
        self.btn_show_details.clicked.connect(self.summary.write_summary)

        self.lable_date = QtWidgets.QLabel(self.MainWindow)
        self.lable_date.setObjectName("lable_date")
        self.current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.lable_date.setText(self.current_date)
        self.lable_date.setGeometry(QtCore.QRect(400, 50, 250, 100))
        self.lable_date.setFont(self.font_list[20])

        self.lable_cash_title = QtWidgets.QLabel(self.MainWindow)
        self.lable_cash_title.setObjectName("lable_cash_title")
        self.lable_cash_title.setGeometry(QtCore.QRect(50, 200, 300, 50))
        self.lable_cash_title.setText("Cash 现金:")
        self.lable_cash_title.setFont(self.font_list[20])

        self.lable_card_title = QtWidgets.QLabel(self.MainWindow)
        self.lable_card_title.setObjectName("lable_card_title")
        self.lable_card_title.setGeometry(QtCore.QRect(50, 250, 300, 50))
        self.lable_card_title.setText("Card 刷卡:")
        self.lable_card_title.setFont(self.font_list[20])

        self.lable_unpaid_title = QtWidgets.QLabel(self.MainWindow)
        self.lable_unpaid_title.setObjectName("lable_unpaid_title")
        self.lable_unpaid_title.setGeometry(QtCore.QRect(50, 300, 300, 50))
        self.lable_unpaid_title.setText("Unpaid 未付款: ")
        self.lable_unpaid_title.setFont(self.font_list[20])

        self.lable_cashback_title = QtWidgets.QLabel(self.MainWindow)
        self.lable_cashback_title.setObjectName("lable_cashback_title")
        self.lable_cashback_title.setGeometry(QtCore.QRect(50, 350, 300, 50))
        self.lable_cashback_title.setText("Cashback 返现: ")
        self.lable_cashback_title.setFont(self.font_list[20])

        self.lable_cash_amount = QtWidgets.QLabel(self.MainWindow)
        self.lable_cash_amount.setObjectName("lable_cash_amount")
        self.lable_cash_amount.setGeometry(QtCore.QRect(400, 200, 400, 50))
        self.lable_cash_amount.setText("cash amount")
        self.lable_cash_amount.setFont(self.font_list[20])

        self.lable_card_amount = QtWidgets.QLabel(self.MainWindow)
        self.lable_card_amount.setObjectName("lable_card_amount")
        self.lable_card_amount.setGeometry(QtCore.QRect(400, 250, 400, 50))
        self.lable_card_amount.setText("card amount")
        self.lable_card_amount.setFont(self.font_list[20])

        self.lable_unpaid_amount = QtWidgets.QLabel(self.MainWindow)
        self.lable_unpaid_amount.setObjectName("lable_unpaid_amount")
        self.lable_unpaid_amount.setGeometry(QtCore.QRect(400, 300, 400, 50))
        self.lable_unpaid_amount.setText("unpaid amount")
        self.lable_unpaid_amount.setFont(self.font_list[20])

        self.lable_cashback_amount = QtWidgets.QLabel(self.MainWindow)
        self.lable_cashback_amount.setObjectName("lable_cashback_amount")
        self.lable_cashback_amount.setGeometry(QtCore.QRect(400, 350, 400, 50))
        self.lable_cashback_amount.setText("cashback amount")
        self.lable_cashback_amount.setFont(self.font_list[20])

        self.show_result()

    def btn_select_date_clicked(self):
        self.cwindow.show()

    def date_clicked(self):
        self.summary.date = self.cwindow.calwindow.selectedDate().toString("yyyy-MM-dd")
        self.lable_date.setText(self.summary.date)
        self.summary.summarize(self.summary.date)
        self.show_result()

    def show_result(self):
        cash = "$%.2f     总单数: %i" % (self.summary.cash_total, self.summary.cash_receipt_amount)
        self.lable_cash_amount.setText(cash)
        card = "$%.2f     总单数: %i" % (self.summary.card_total, self.summary.card_receipt_amount)
        self.lable_card_amount.setText(card)
        unpaid = "$%.2f     总单数: %i" % (self.summary.unpaid_total, self.summary.unpaid_receipt_amount)
        self.lable_unpaid_amount.setText(unpaid)
        cashback = "$%.2f     总单数: %i" % (self.summary.cashback_total, self.summary.cashback_receipt_amount)
        self.lable_cashback_amount.setText(cashback)

    def show(self):
        self.MainWindow.show()

    def close(self):
        self.MainWindow.close()


class Summary:
    def __init__(self):

        self.path = os.getcwd()  # get current work dir
        current_hour = datetime.datetime.now().strftime('%H')  # get current hour
        if int(current_hour) < 6:  # if after midnight, but still count as the same day
            today = datetime.date.today()
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            self.date = yesterday.strftime('%Y-%m-%d')
        else:
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')

    def summarize(self, date=""):
        try:
            data_dir = self.path + '/data/receipt/' + self.date + '/'
            file_list = os.listdir(data_dir)
        except Exception as e:
            print(e)

        if date != "":
            try:
                data_dir = self.path + '/data/receipt/' + date + '/'
                file_list = os.listdir(data_dir)
            except Exception as e:
                print(e)

        cash_total_amount = 0
        card_total_amount = 0
        unpaid_total_amount = 0
        cashback_total_amount = 0
        cash_count = 0
        card_count = 0
        unpaid_count = 0
        cashback_count = 0
        unpaid_dic = {}
        cash_dic = {}
        card_dic = {}
        cashback_dic = {}

        try:
            for file_name in file_list:
                with open(data_dir + file_name) as f:
                    lines = f.readlines()
                    f.close()

                for line in lines:
                    if "#" in line:
                        receipt_num = int(line.split("#")[1])

                    if "[" in line:
                        temp = re.split("[][]", line)

                        if temp[1] == 'PAID':
                            paid_mount = float(temp[2].split("$")[1])
                            continue

                        if temp[1] == "UNPAID":
                            unpaid_count += 1
                            unpaid_amount = float(line.split("$")[1])
                            unpaid_dic[receipt_num] = unpaid_amount
                            unpaid_total_amount += unpaid_amount

                        if temp[1] == "CASHBACK":
                            cashback_count += 1
                            cashback_amount = float(line.split("$")[1])
                            cashback_dic[receipt_num] = cashback_amount
                            cashback_total_amount += cashback_amount

                    if "cash" in line:
                        cash_count += 1
                        cash_amount = float(line.split("$")[1])
                        cash_total_amount += cash_amount
                        cash_dic[receipt_num] = cash_amount

                    if "card" in line:
                        card_count += 1
                        card_amount = float(line.split("$")[1])
                        card_total_amount += card_amount
                        card_dic[receipt_num] = card_amount

            keys = list(cash_dic.keys())
            keys.sort()

            keys = list(card_dic.keys())
            keys.sort()

            keys = list(unpaid_dic.keys())
            keys.sort()
        except Exception as e:
            print(e)

        self.cash_dic = cash_dic
        self.card_dic = card_dic
        self.unpaid_dic = unpaid_dic
        self.cashback_dic = cashback_dic

        self.cash_total = cash_total_amount
        self.card_total = card_total_amount
        self.unpaid_total = unpaid_total_amount
        self.cashback_total = cashback_total_amount

        self.cash_receipt_amount = cash_count
        self.card_receipt_amount = card_count
        self.unpaid_receipt_amount = unpaid_count
        self.cashback_receipt_amount = cashback_count

    def write_summary(self):

        output_dir = ".\\data\\summary\\"
        # create data path if not exist
        if not os.path.exists(output_dir):  # if path not exist
            print("today's data path not exist")
            try:  # create path
                os.mkdir(output_dir)
            except Exception as e:  # try another way to make path
                os.makedirs(output_dir)

        path = output_dir+self.date+".txt"
        with open(path, "w") as f:
            f.write("Cupar Hotel\n")
            f.write("Summary of %s\n" % self.date)
            f.write("[CASH] 现金总额\ntotal amount: $%.2f\n" % self.cash_total)
            for key in self.cash_dic:
               f.write("#%i $%.2f\n" % (key, self.cash_dic[key]))

            f.write("[CARD] 刷卡总额\ntotal amount: $%.2f\n" % self.card_total)
            for key in self.card_dic:
               f.write("#%i $%.2f\n" % (key, self.card_dic[key]))

            f.write("[UNPAID] 未付款总额\ntotal amount: $%.2f\n" % self.unpaid_total)
            for key in self.unpaid_dic:
               f.write("#%i $%.2f\n" % (key, self.unpaid_dic[key]))

            f.write("[CASHBACK] 返现总额\ntotal amount: $%.2f\n" % self.cashback_total)
            for key in self.cashback_dic:
                f.write("#%i $%.2f\n" % (key, self.cashback_dic[key]))

        os.startfile(path)


class CalendarWindow(QWidget):
    def __init__(self):
        super(CalendarWindow, self).__init__()

        self.selected_date = ""

        self.setGeometry(100,100,400,350)
        self.setWindowTitle("select date 选择日期")

        self.calwindow = QCalendarWidget(self)
        self.calwindow.setMinimumDate(QDate(2021, 1, 1))
        self.calwindow.setMaximumDate(QDate(3000, 1, 1))
        self.calwindow.setGridVisible(True)
        self.calwindow.move(20, 20)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = SummaryWindow()
    window.show()

    sys.exit(app.exec_())
