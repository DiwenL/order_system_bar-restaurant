import re
import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize
import qtawesome as qta


class MainUI(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setWindowTitle("Cupar Bar Order System")  # set window's name
        self.MainWindow.resize(1920, 1080)  # set windows size
        self.translate = QtCore.QCoreApplication.translate

        self.font_list = []
        for i in range(1, 31):
            font = QtGui.QFont()
            font.setFamily("Microsoft JhengHei UI")
            font.setPointSize(i)
            self.font_list.append(font)

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)  # set main widget
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('''QWidget#centralwidget{background: azure}''')
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)  # set tab widget
        self.tabWidget.setGeometry(QtCore.QRect(920, 20, 1000, 9800))  # set tab widget size
        self.tabWidget.setFont(self.font_list[28])
        self.tabWidget.setObjectName("tab_menu")
        self.tabWidget.setStyleSheet('''QTabWidget::pane{
                                                         border-top: 4px dotted;
                                                         position: absolute;
                                                         top: -1.5em} 
                                        QTabWidget::tab-bar{
                                                            alignment: center;}
                                        QTabBar::tab{
                                                     background: azure;
                                                     min-width: 150px;
                                                     text-align:center;}
                                        QTabBar::tab:selected{
                                                     border-top: 2px solid;
                                                     border-left: 2px solid;
                                                     border-right: 2px solid;
                                                     border-bottom: none}
                                        QTabBar::tab:!selected{
                                                     border-bottom: 2px solid;
                                                     border-top: none;
                                                     border-left: none;
                                                     border-right: none;}''')

        self.tab_list = {}
        self.toolbox_list = {}
        self.page_list = {}
        self.btn_list = {}

        self.read_ui_design()

        self.tab_names = self.design.keys()

        try:
            cwd = os.getcwd()
            with open(cwd + "/data/init.txt", encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                if "菜单颜色" in line:
                    line = line.split(":")[1]
                    colors = re.split("[|]", line)
                    self.color_list_str = []
                    for color in colors:
                        self.color_list_str.append("rgb%s" % color)
        except Exception as e:
            print(e)
            self.color_list_str = ["rgb(255, 126, 0, 40)", "rgb(255, 0, 125, 40)",
                                   "rgb(126, 255, 0, 40)", "rgb(126, 0, 255, 40)",
                                   "rgb(0, 126, 255, 40)", "rgb(0, 255, 126, 40)"]
        self.colors_str = {}
        idx = 0
        for name in self.design.keys():
            if idx > len(self.color_list_str):
                idx = 0
            self.colors_str[name] = self.color_list_str[idx]
            idx += 1

        self.create_menu()

        self.list_receipt = QtWidgets.QListWidget(self.MainWindow)
        self.list_receipt.setGeometry(QtCore.QRect(20, 100, 400, 800))
        self.list_receipt.setObjectName("list_receipt")
        self.list_receipt.setFont(self.font_list[12])
        self.list_receipt.setStyleSheet('''QListView{background: azure;
                                                     border: none;}
                                           QListView::item{
                                                     color: black;
                                                     min-height: 100px;
                                                     text-align: right;
                                                     border:none}
                                           QListView::item:selected{
                                                     border-left: 2px solid;
                                                     border-top: 2px solid;
                                                     border-bottom: 2px solid;
                                                     border-top-left-radius: 20px;
                                                     border-bottom-left-radius: 20px;
                                                     border-right: none;
                                                     background: azure;
                                                     }
                                           QListView::item:!selected{
                                                     border-right: 2px solid;
                                                     }
                                           QListView::item:selected:active{
                                                     border-right: none;}
                                           QListView::item:selected!:active{
                                                     border-right: none}''')

        self.list_order = QtWidgets.QListWidget(self.MainWindow)
        self.list_order.setGeometry(QtCore.QRect(420, 100, 400, 800))
        self.list_order.setObjectName("list_order")
        self.list_order.setFont(self.font_list[12])
        self.list_order.setStyleSheet('''QListView{background: azure;
                                                   border: none;
                                                   border-right: 2px solid}
                                         QListView::item{
                                                   min-height: 100px;}''')

        self.btn_exit = QtWidgets.QPushButton(self.MainWindow)
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.setGeometry(QtCore.QRect(1770, 1000, 150, 80))
        self.btn_exit.setFont(self.font_list[18])
        self.btn_exit.setText("EXIT")
        self.btn_exit.setStyleSheet('''QPushButton{border: none; color: none}''')

        self.btn_favour = QtWidgets.QPushButton(self.MainWindow)
        self.btn_favour.setObjectName("btn_favour")
        self.btn_favour.setGeometry(QtCore.QRect(820, 100, 100, 100))
        self.btn_favour.setFont(self.font_list[18])
        self.btn_favour.setText("酱")
        self.btn_favour.setStyleSheet('''QPushButton{padding-top:40px;
                                                     border: none;
                                                     color: none;
                                                     border-bottom: 2px solid;}''')

        self.btn_beer_amount = QtWidgets.QPushButton(self.MainWindow)
        self.btn_beer_amount.setObjectName("btn_beer_amount")
        self.btn_beer_amount.setGeometry(QtCore.QRect(820, 200, 100, 100))
        self.btn_beer_amount.setFont(self.font_list[18])
        self.btn_beer_amount.setText("数量")
        self.btn_beer_amount.setStyleSheet('''QPushButton{padding-top:40px;
                                                          border: none;
                                                          color: none;
                                                          border-bottom: 2px solid;}''')

        self.btn_delete_order = QtWidgets.QPushButton(self.MainWindow)
        self.btn_delete_order.setObjectName("btn_beer_amount")
        self.btn_delete_order.setGeometry(QtCore.QRect(820, 300, 100, 100))
        self.btn_delete_order.setFont(self.font_list[18])
        self.btn_delete_order.setText("删除")
        self.btn_delete_order.setStyleSheet('''QPushButton{padding-top:40px;
                                                           border: none;
                                                           color: none;
                                                           border-bottom: 2px solid;}''')

        self.btn_comment = QtWidgets.QPushButton(self.MainWindow)
        self.btn_comment.setObjectName("btn_beer_amount")
        self.btn_comment.setGeometry(QtCore.QRect(820, 400, 100, 100))
        self.btn_comment.setFont(self.font_list[18])
        self.btn_comment.setText("备注")
        self.btn_comment.setStyleSheet('''QPushButton{padding-top:40px;
                                                      border: none;
                                                      color: none;
                                                      border-bottom: 2px solid;}''')

        self.btn_new = QtWidgets.QPushButton(self.MainWindow)
        self.btn_new.setObjectName("btn_add")
        self.btn_new.setGeometry(QtCore.QRect(10, 0, 200, 100))
        self.btn_new.setFont(self.font_list[18])
        self.btn_new.setText("新建")
        self.btn_new.setStyleSheet('''QPushButton{border: none; color: none;}''')
        self.btn_new.setIcon(qta.icon("fa.plus-square-o", color="black"))
        self.btn_new.setIconSize(QSize(40, 40))

        self.btn_delete = QtWidgets.QPushButton(self.MainWindow)
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setGeometry(QtCore.QRect(210, 0, 200, 100))
        self.btn_delete.setFont(self.font_list[18])
        self.btn_delete.setText("删除")
        self.btn_delete.setStyleSheet('''QPushButton{border: none; color: none}''')
        self.btn_delete.setIcon(qta.icon("fa.trash-o", color="black"))
        self.btn_delete.setIconSize(QSize(40, 40))

        self.btn_info = QtWidgets.QPushButton(self.MainWindow)
        self.btn_info.setObjectName("btn_info")
        self.btn_info.setGeometry(QtCore.QRect(420, 0, 200, 100))
        self.btn_info.setFont(self.font_list[18])
        self.btn_info.setText("信息")
        self.btn_info.setStyleSheet('''QPushButton{border: none; color: none}''')
        self.btn_info.setIcon(qta.icon("fa.info", color="black"))
        self.btn_info.setIconSize(QSize(40, 40))

        self.btn_print = QtWidgets.QPushButton(self.MainWindow)
        self.btn_print.setObjectName("btn_print")
        self.btn_print.setGeometry(QtCore.QRect(620, 0, 200, 100))
        self.btn_print.setFont(self.font_list[18])
        self.btn_print.setText("打印")
        self.btn_print.setStyleSheet('''QPushButton{border: none; color: none}''')
        self.btn_print.setIcon(qta.icon("fa.print", color="black"))
        self.btn_print.setIconSize(QSize(40, 40))

        self.btn_record = QtWidgets.QPushButton(self.MainWindow)
        self.btn_record.setObjectName("btn_record")
        self.btn_record.setGeometry(QtCore.QRect(210, 900, 200, 100))
        self.btn_record.setFont(self.font_list[18])
        self.btn_record.setText("完成")
        self.btn_record.setStyleSheet('''QPushButton{border: none; color: none}''')
        self.btn_record.setIcon(qta.icon("fa.file-o", color="black"))
        self.btn_record.setIconSize(QSize(40, 40))

        self.btn_pay = QtWidgets.QPushButton(self.MainWindow)
        self.btn_pay.setObjectName("btn_pay")
        self.btn_pay.setGeometry(QtCore.QRect(10, 900, 200, 100))
        self.btn_pay.setFont(self.font_list[18])
        self.btn_pay.setText("付款")
        self.btn_pay.setStyleSheet('''QPushButton{border: none; color: none}''')
        self.btn_pay.setIcon(qta.icon("fa.money", color="black"))
        self.btn_pay.setIconSize(QSize(40, 40))

        self.btn_amount_plus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_amount_plus.setObjectName("btn_amount_plus")
        self.btn_amount_plus.setGeometry(QtCore.QRect(420, 900, 100, 100))
        self.btn_amount_plus.setFont(self.font_list[18])
        self.btn_amount_plus.setText("+")
        self.btn_amount_plus.setStyleSheet('''QPushButton{border: none; color: none; border-right: 2px solid}''')

        self.btn_price_plus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_price_plus.setObjectName("btn_price_plus")
        self.btn_price_plus.setGeometry(QtCore.QRect(520, 900, 100, 100))
        self.btn_price_plus.setFont(self.font_list[18])
        self.btn_price_plus.setText("$↑")
        self.btn_price_plus.setStyleSheet('''QPushButton{border: none; color: none; border-right: 2px solid}''')

        self.btn_price_minus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_price_minus.setObjectName("btn_price_minus")
        self.btn_price_minus.setGeometry(QtCore.QRect(620, 900, 100, 100))
        self.btn_price_minus.setFont(self.font_list[18])
        self.btn_price_minus.setText("$↓")
        self.btn_price_minus.setStyleSheet('''QPushButton{border: none; color: none; border-right: 2px solid}''')

        self.btn_amount_minus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_amount_minus.setObjectName("btn_amount_minus")
        self.btn_amount_minus.setGeometry(QtCore.QRect(720, 900, 100, 100))
        self.btn_amount_minus.setFont(self.font_list[18])
        self.btn_amount_minus.setText("-")
        self.btn_amount_minus.setStyleSheet('''QPushButton{border: none; color: none}''')

    def create_tabs(self, tab_name_list) -> None:
        for tab_name in tab_name_list:
            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_%s" % tab_name)
            self.tabWidget.addTab(tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab), self.translate("MainWindow", "%s" % tab_name))

            toolbox = QtWidgets.QToolBox(tab)
            toolbox.setGeometry(QtCore.QRect(0, 50, 1000, 850))
            toolbox.setFont(self.font_list[28])
            toolbox.setObjectName("toolbox_%s" % tab_name)
            toolbox.setStyleSheet('''QToolBox::tab{
                                                   background: azure; 
                                                   border-left: 2px solid;}
                                     QToolBox::tab:selected{
                                                            border-bottom: 2px solid;
                                                            border-top: 2px solid;
                                                            border-top-left-radius: 30px;
                                                            border-bottom-left-radius: 30px;}''')

            self.tab_list[tab_name] = tab
            self.toolbox_list[tab_name] = toolbox
            self.page_list[tab_name] = {}
            self.btn_list[tab_name] = {}

        return

    def create_pages(self, page_name_list, tab_name) -> None:
        if len(page_name_list) == 0:
            return

        try:
            toolbox = self.toolbox_list[tab_name]
        except Exception as e:
            print(e)
            return

        for page_name in page_name_list:
            page = QtWidgets.QWidget()
            page.setGeometry(QtCore.QRect(0, 0, 1000, 405))
            page.setObjectName(page_name)
            page.setStyleSheet('''QWidget{background: azure}''')
            toolbox.addItem(page, "")
            toolbox.setItemText(toolbox.indexOf(page), self.translate("MainWindow", page_name))

            self.page_list[tab_name][page_name] = page
            self.btn_list[tab_name][page_name] = {}

        return

    def create_button(self, btn_name_list, tab_name, page_name) -> None:
        if len(btn_name_list) == 0:
            return
        if len(btn_name_list) > 20:
            print("btn list out of range")
            return

        try:
            page = self.page_list[tab_name][page_name]
        except Exception as e:
            print(e)
            return

        x = 5
        y = 0
        for btn_name in btn_name_list:
            btn = QtWidgets.QPushButton(page)
            btn.setGeometry(QtCore.QRect(x, y, 190, 90))
            btn.setFont(self.font_list[14])
            btn.setObjectName(btn_name)
            btn.setText(btn_name)
            self.btn_list[tab_name][page_name][btn_name] = btn

            stylesheet = "border-radius: 10px; border: 2px solid; background-color:%s" % self.colors_str[tab_name]
            btn.setStyleSheet(stylesheet)
            x += 200
            if x == 1005:
                x = 5
                y += 100

        return

    def read_ui_design(self) -> None:
        ui_input_path = os.getcwd() + "\\data\\ui_input\\"
        tab_list = os.listdir(ui_input_path)
        self.design = {}
        for tab_file in tab_list:
            tab_name = re.split('[.]', tab_file)[1]
            self.design[tab_name] = {}
            with open(ui_input_path + tab_file, 'r', encoding='utf-8') as f:  # read data from file
                data = f.readlines()
                f.close()

            for line in data:
                if line[0] == "[":
                    page_name = re.split('[][]', line)[1]
                    self.design[tab_name][page_name] = []
                    current_page = page_name
                else:
                    self.design[tab_name][current_page].append(line.split("|")[0])

    def create_menu(self):
        tabs = list(self.design.keys())
        self.create_tabs(tabs)
        for tab in self.design:
            pages = list(self.design[tab].keys())
            self.create_pages(pages, tab)
            for page in self.design[tab]:
                btns = self.design[tab][page]
                self.create_button(btns, tab, page)
        return

    def show(self):
        self.MainWindow.show()

    class FavourSelectionWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.favour_btns = {}
            self.FavourSelectionWindow = QtWidgets.QMainWindow()
            self.FavourSelectionWindow.setWindowTitle("酱 Favours")
            self.FavourSelectionWindow.resize(600, 400)
            return

        def create_favour_btns(self):
            try:
                cwd = os.getcwd()
                with open(cwd + "/data/init.txt",encoding='utf-8') as f:
                    lines = f.readlines()
                for line in lines:
                    if "酱料" in line:
                        favours = line.split("\n")[0].split(",")
                        favour_list = favours[1:]
            except Exception as e:
                print(e)
                favour_list = ["酸甜", "椒盐", "buffalo", "辣酱", "ranch", "甜辣", "蜂蜜", "柠檬辣椒", "greek"]

            x = 0
            y = 0
            for favour in favour_list:
                btn = QtWidgets.QPushButton(self.FavourSelectionWindow)
                btn.setGeometry(QtCore.QRect(x, y, 150, 100))
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setFamily("Microsoft JhengHei UI")
                btn.setFont(font)
                btn.setObjectName(favour)
                btn.setText(favour)
                self.favour_btns[favour] = btn

                x += 150
                if x == 600:
                    x = 0
                    y += 100

        def show(self):
            self.FavourSelectionWindow.show()

        def close(self):
            self.FavourSelectionWindow.close()

    class BeerAmountWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.amount_btns = {}
            self.BeerAmountWindow = QtWidgets.QMainWindow()
            self.BeerAmountWindow.setWindowTitle("数量 Amount")
            self.BeerAmountWindow.resize(600, 400)
            self.BeerAmountWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            return

        def create_amount_btns(self):
            try:
                cwd = os.getcwd()
                with open(cwd + "/data/init.txt",encoding='utf-8') as f:
                    lines = f.readlines()
                for line in lines:
                    if "数量" in line:
                        amounts = line.split("\n")[0].split(",")
                        amount_list = amounts[1:]
            except Exception as e:
                print(e)
                amount_list = ["6", "9", "12", "15", "18", "24", "48"]

            x = 0
            y = 0
            for amount in amount_list:
                btn = QtWidgets.QPushButton(self.BeerAmountWindow)
                btn.setGeometry(QtCore.QRect(x, y, 150, 100))
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setFamily("Microsoft JhengHei UI")
                btn.setFont(font)
                btn.setObjectName(amount)
                btn.setText(amount)
                self.amount_btns[amount] = btn

                x += 150
                if x == 600:
                    x = 0
                    y += 100

        def show(self):
            self.BeerAmountWindow.show()

        def close(self):
            self.BeerAmountWindow.close()

    class InfoWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.file_path = os.getcwd() + "\\data\\customers.txt"
            self.InfoWindow = QtWidgets.QMainWindow()
            self.InfoWindow.setWindowTitle("顾客信息 Customer Infomation")
            self.InfoWindow.resize(900, 600)
            self.InfoWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

            self.customers = {}

            font = QtGui.QFont()
            font.setPointSize(18)
            font.setFamily("Microsoft JhengHei UI")

            self.label_customer_name = QtWidgets.QLabel(self.InfoWindow)
            self.label_customer_name.setGeometry(QtCore.QRect(50, 50, 300, 50))
            self.label_customer_name.setText("名字 Name:")
            self.label_customer_name.setFont(font)

            self.label_customer_phone = QtWidgets.QLabel(self.InfoWindow)
            self.label_customer_phone.setGeometry(QtCore.QRect(50, 150, 300, 50))
            self.label_customer_phone.setText("电话 Phone:")
            self.label_customer_phone.setFont(font)

            self.label_customer_time = QtWidgets.QLabel(self.InfoWindow)
            self.label_customer_time.setGeometry(QtCore.QRect(50, 250, 300, 50))
            self.label_customer_time.setText("取餐时间 Time:")
            self.label_customer_time.setFont(font)

            self.text_name = QtWidgets.QLineEdit(self.InfoWindow)
            self.text_name.setGeometry(QtCore.QRect(50, 100, 300, 50))
            self.text_name.setFont(font)

            self.text_phone = QtWidgets.QLineEdit(self.InfoWindow)
            self.text_phone.setGeometry(QtCore.QRect(50, 200, 300, 50))
            self.text_phone.setFont(font)
            self.text_phone.setInputMask("(000)-000-0000;_")

            self.text_time = QtWidgets.QLineEdit(self.InfoWindow)
            self.text_time.setGeometry(QtCore.QRect(50, 300, 300, 50))
            self.text_time.setFont(font)
            self.text_time.setInputMask("00:00")

            self.text_search = QtWidgets.QLineEdit(self.InfoWindow)
            self.text_search.setGeometry(QtCore.QRect(400, 30, 450, 50))
            self.text_search.setFont(font)

            self.list_info = QtWidgets.QListWidget(self.InfoWindow)
            self.list_info.setGeometry(QtCore.QRect(400, 100, 450, 400))
            self.list_info.setFont(font)

            self.btn_add = QtWidgets.QPushButton(self.InfoWindow)
            self.btn_add.setGeometry(QtCore.QRect(200, 450, 100, 50))
            self.btn_add.setText("添加")
            self.btn_add.setFont(font)

            self.btn_confirm = QtWidgets.QPushButton(self.InfoWindow)
            self.btn_confirm.setGeometry(QtCore.QRect(50, 450, 100, 50))
            self.btn_confirm.setText("确定")
            self.btn_confirm.setFont(font)
            return

        def close(self):
            self.InfoWindow.close()

        def show(self):
            self.InfoWindow.show()

        def search(self, temp):
            result = {}

            for name in self.customers:
                if temp.lower() in name.lower():
                    result[name] = self.customers[name]
                    continue
                for num in self.customers[name]:
                    if temp in num:
                        result[name] = self.customers[name]
            return result

        def add_customers(self, name, phone):
            self.customers[name] = phone
            self.list_info.addItem("%s\n(%s)-%s-%s" % (name, phone[0], phone[1], phone[2]))

            with open(self.file_path, 'w',encoding='utf-8') as w:
                names = list(self.customers.keys())
                names.sort()
                for name in names:
                    phone = self.customers[name]
                    w.write("%s:%s-%s-%s\n" % (name, phone[0], phone[1], phone[2]))

        def read_customers(self):
            with open(self.file_path, 'r',encoding='utf-8') as f:
                lines = f.readlines()
                f.close()
            for line in lines:
                name, phone = line.split("\n")[0].split(":")
                self.customers[name] = phone.split("-")

        def show_customers(self, temp=""):
            self.read_customers()
            self.list_info.clear()
            if temp != "":
                customers = self.search(temp)
            else:
                customers = self.customers
            for customer in customers:
                phone = self.customers[customer]
                self.list_info.addItem("%s\n(%s)-%s-%s" % (customer, phone[0], phone[1], phone[2]))
            return

    class PayWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.total = 0
            self.unpaid = 0
            self.PayWindow = QtWidgets.QMainWindow()
            self.PayWindow.setWindowTitle("付款信息 Payment")
            self.PayWindow.resize(600, 700)
            self.PayWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

            font = QtGui.QFont()
            font.setPointSize(18)
            font.setFamily("Microsoft JhengHei UI")

            self.label_total_title = QtWidgets.QLabel(self.PayWindow)
            self.label_total_title.setGeometry(QtCore.QRect(50, 30, 200, 50))
            self.label_total_title.setText("总额 Total: ")
            self.label_total_title.setFont(font)

            self.label_total_amount = QtWidgets.QLabel(self.PayWindow)
            self.label_total_amount.setGeometry(QtCore.QRect(353, 30, 150, 50))
            self.label_total_amount.setText("$")
            self.label_total_amount.setFont(font)

            self.btn_cash = QtWidgets.QPushButton(self.PayWindow)
            self.btn_cash.setGeometry(QtCore.QRect(50, 100, 150, 50))
            self.btn_cash.setText("现金 Cash")
            self.btn_cash.setFont(font)
            self.btn_cash.setCheckable(True)

            self.btn_card = QtWidgets.QPushButton(self.PayWindow)
            self.btn_card.setGeometry(QtCore.QRect(50, 170, 150, 50))
            self.btn_card.setText("刷卡 Card")
            self.btn_card.setFont(font)
            self.btn_card.setCheckable(True)

            self.btn_emt = QtWidgets.QPushButton(self.PayWindow)
            self.btn_emt.setGeometry(QtCore.QRect(50, 240, 150, 50))
            self.btn_emt.setText("E-transfer")
            self.btn_emt.setFont(font)
            self.btn_emt.setCheckable(True)

            self.label_divided_line = QtWidgets.QLabel(self.PayWindow)
            self.label_divided_line.setGeometry(QtCore.QRect(50, 300, 400, 50))
            self.label_divided_line.setText("-------------------------------------")
            self.label_divided_line.setFont(font)

            self.label_unpaid_title = QtWidgets.QLabel(self.PayWindow)
            self.label_unpaid_title.setGeometry(QtCore.QRect(50, 330, 400, 50))
            self.label_unpaid_title.setText("未付款 Unpaid:")
            self.label_unpaid_title.setFont(font)

            self.label_unpaid_amount = QtWidgets.QLabel(self.PayWindow)
            self.label_unpaid_amount.setGeometry(QtCore.QRect(353, 330, 400, 50))
            self.label_unpaid_amount.setText("$")
            self.label_unpaid_amount.setFont(font)

            self.btn_cashback = QtWidgets.QPushButton(self.PayWindow)
            self.btn_cashback.setGeometry(QtCore.QRect(50, 420, 150, 50))
            self.btn_cashback.setText("Cashback")
            self.btn_cashback.setFont(font)
            self.btn_cashback.setCheckable(True)

            self.line_cashback = QtWidgets.QLineEdit(self.PayWindow)
            self.line_cashback.setGeometry(350, 420, 150, 50)
            self.line_cashback.setFont(font)
            self.line_cashback.setInputMask("$000.00")
            self.line_cashback.setVisible(False)

            self.line_cash = QtWidgets.QLineEdit(self.PayWindow)
            self.line_cash.setGeometry(350, 100, 150, 50)
            self.line_cash.setFont(font)
            self.line_cash.setInputMask("$00.00")
            self.line_cash.setVisible(False)

            self.line_card = QtWidgets.QLineEdit(self.PayWindow)
            self.line_card.setGeometry(350, 170, 150, 50)
            self.line_card.setFont(font)
            self.line_card.setInputMask("$00.00")
            self.line_card.setVisible(False)

            self.line_emt = QtWidgets.QLineEdit(self.PayWindow)
            self.line_emt.setGeometry(350, 240, 150, 50)
            self.line_emt.setFont(font)
            self.line_emt.setInputMask("$00.00")
            self.line_emt.setVisible(False)

            self.btn_confirm = QtWidgets.QPushButton(self.PayWindow)
            self.btn_confirm.setGeometry(60, 520, 210, 100)
            self.btn_confirm.setFont(font)
            self.btn_confirm.setText("确认 Confirm")

            self.btn_cancel = QtWidgets.QPushButton(self.PayWindow)
            self.btn_cancel.setGeometry(330, 520, 210, 100)
            self.btn_cancel.setFont(font)
            self.btn_cancel.setText("取消 Cancel")
            return

        def update_unpaid(self):
            if self.line_cash.isVisible():
                cash = self.line_cash.text().split("$")[1]
                if cash == ".":
                    cash = 0
                else:
                    cash = float(cash)
            else:
                cash = 0

            if self.line_card.isVisible():
                card = self.line_card.text().split("$")[1]
                if card == ".":
                    card = 0
                else:
                    card = float(card)
            else:
                card = 0

            if self.line_emt.isVisible():
                emt = self.line_emt.text().split("$")[1]
                if emt == ".":
                    emt = 0
                else:
                    emt = float(emt)
            else:
                emt = 0

            self.unpaid = self.total - cash - card - emt
            if self.unpaid < 0:
                self.unpaid = 0
            self.label_unpaid_amount.setText("$%.2f" % self.unpaid)

        def set_context(self, total, unpaid, cash=0, card=0, emt=0, cashback=0):
            if total >= 100:  # set input mask if total over $100
                self.line_cash.setInputMask("$000.00")
                self.line_card.setInputMask("$000.00")
                self.line_emt.setInputMask("$000.00")

            if cash != 0:
                self.line_cash.setVisible(True)
                self.btn_cash.setChecked(True)
                self.line_cash.setText("%.2f" % cash)
            else:
                self.line_cash.setVisible(False)
                self.btn_cash.setChecked(False)

            if card != 0:
                self.line_card.setVisible(True)
                self.btn_card.setChecked(True)
                self.line_card.setText("%.2f" % card)
            else:
                self.line_card.setVisible(False)
                self.btn_card.setChecked(False)

            if emt != 0:
                self.line_emt.setVisible(True)
                self.btn_emt.setChecked(True)
                self.line_emt.setText("%.2f" % emt)
            else:
                self.line_emt.setVisible(False)
                self.btn_emt.setChecked(False)

            if cashback != 0:
                self.line_cashback.setVisible(True)
                self.btn_cashback.setCheckable(True)
                self.line_cashback.setText("%.2f" % cashback)
            else:
                self.line_cashback.setVisible(False)
                self.btn_cashback.setCheckable(False)

            self.total = total
            self.unpaid = unpaid
            self.label_total_amount.setText("$%.2f" % total)
            self.label_unpaid_amount.setText("$%.2f" % unpaid)

        def show(self):
            self.PayWindow.show()

        def close(self):
            if self.btn_cash.isChecked():
                self.btn_cash.setChecked(False)
            if self.btn_card.isChecked():
                self.btn_card.setChecked(False)
            if self.btn_emt.isChecked():
                self.btn_emt.setChecked(False)
            if self.btn_cashback.isChecked():
                self.btn_cashback.setCheckable(False)
            self.PayWindow.close()

    class CommentWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.CommentWindow = QtWidgets.QMainWindow()
            self.CommentWindow.setWindowTitle("备注 Comment")
            self.CommentWindow.resize(600, 400)

            font = QtGui.QFont()
            font.setPointSize(18)
            font.setFamily("Microsoft JhengHei UI")

            self.line_comment = QtWidgets.QLineEdit(self.CommentWindow)
            self.line_comment.setGeometry(QtCore.QRect(100, 100, 400, 80))
            self.line_comment.setFont(font)

            self.btn_comment_confirm = QtWidgets.QPushButton(self.CommentWindow)
            self.btn_comment_confirm.setGeometry(QtCore.QRect(200, 250, 200, 100))
            self.btn_comment_confirm.setFont(font)
            self.btn_comment_confirm.setText("Confirm 确认")

        def show(self):
            self.line_comment.setText("")
            self.CommentWindow.show()

        def close(self):
            self.CommentWindow.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.read_ui_design()
    ui.create_menu()
    ui.show()

    fwindow = ui.FavourSelectionWindow()
    fwindow.create_favour_btns()

    bwindow = ui.BeerAmountWindow()
    bwindow.create_amount_btns()

    sys.exit(app.exec_())
