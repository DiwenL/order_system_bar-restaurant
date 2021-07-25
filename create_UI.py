import re
import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class MainUI(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setObjectName("Cupar Bar Order System")  # set window's name
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
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)  # set tab widget
        self.tabWidget.setGeometry(QtCore.QRect(920, 0, 1000, 1000))  # set tab widget size
        self.tabWidget.setFont(self.font_list[28])
        self.tabWidget.setObjectName("tab_menu")


        self.tab_list = {}
        self.toolbox_list = {}
        self.page_list = {}
        self.btn_list = {}

        self.read_ui_design()
        self.create_menu()

        self.list_receipt = QtWidgets.QListWidget(self.MainWindow)
        self.list_receipt.setGeometry(QtCore.QRect(10, 100, 400, 800))
        self.list_receipt.setObjectName("list_receipt")

        self.list_order = QtWidgets.QListWidget(self.MainWindow)
        self.list_order.setGeometry(QtCore.QRect(420, 100, 400, 800))
        self.list_order.setObjectName("list_order")

        self.btn_exit = QtWidgets.QPushButton(self.MainWindow)
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.setGeometry(QtCore.QRect(1770,1000,150,80))
        self.btn_exit.setFont(self.font_list[18])
        self.btn_exit.setText("EXIT")

        self.btn_favour = QtWidgets.QPushButton(self.MainWindow)
        self.btn_favour.setObjectName("btn_favour")
        self.btn_favour.setGeometry(QtCore.QRect(820,100,100,100))
        self.btn_favour.setFont(self.font_list[18])
        self.btn_favour.setText("酱")

        self.btn_beer_amount = QtWidgets.QPushButton(self.MainWindow)
        self.btn_beer_amount.setObjectName("btn_beer_amount")
        self.btn_beer_amount.setGeometry(QtCore.QRect(820,200,100,100))
        self.btn_beer_amount.setFont(self.font_list[18])
        self.btn_beer_amount.setText("数量")

        self.btn_add = QtWidgets.QPushButton(self.MainWindow)
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setGeometry(QtCore.QRect(10,0,200,100))
        self.btn_add.setFont(self.font_list[18])
        self.btn_add.setText("新建")

        self.btn_delete = QtWidgets.QPushButton(self.MainWindow)
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setGeometry(QtCore.QRect(210,0,200,100))
        self.btn_delete.setFont(self.font_list[18])
        self.btn_delete.setText("删除")

        self.btn_info = QtWidgets.QPushButton(self.MainWindow)
        self.btn_info.setObjectName("btn_info")
        self.btn_info.setGeometry(QtCore.QRect(420,0,200,100))
        self.btn_info.setFont(self.font_list[18])
        self.btn_info.setText("信息")

        self.btn_print = QtWidgets.QPushButton(self.MainWindow)
        self.btn_print.setObjectName("btn_print")
        self.btn_print.setGeometry(QtCore.QRect(620,0,200,100))
        self.btn_print.setFont(self.font_list[18])
        self.btn_print.setText("打印")

        self.btn_record = QtWidgets.QPushButton(self.MainWindow)
        self.btn_record.setObjectName("btn_record")
        self.btn_record.setGeometry(QtCore.QRect(10,900,200,100))
        self.btn_record.setFont(self.font_list[18])
        self.btn_record.setText("记录")

        self.btn_pay = QtWidgets.QPushButton(self.MainWindow)
        self.btn_pay.setObjectName("btn_pay")
        self.btn_pay.setGeometry(QtCore.QRect(210, 900, 200, 100))
        self.btn_pay.setFont(self.font_list[18])
        self.btn_pay.setText("付款")

        self.btn_amount_plus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_amount_plus.setObjectName("btn_amount_plus")
        self.btn_amount_plus.setGeometry(QtCore.QRect(420, 900, 100, 100))
        self.btn_amount_plus.setFont(self.font_list[18])
        self.btn_amount_plus.setText("+")

        self.btn_price_plus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_price_plus.setObjectName("btn_price_plus")
        self.btn_price_plus.setGeometry(QtCore.QRect(520, 900, 100, 100))
        self.btn_price_plus.setFont(self.font_list[18])
        self.btn_price_plus.setText("$↑")

        self.btn_price_minus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_price_minus.setObjectName("btn_price_minus")
        self.btn_price_minus.setGeometry(QtCore.QRect(620, 900, 100, 100))
        self.btn_price_minus.setFont(self.font_list[18])
        self.btn_price_minus.setText("$↓")

        self.btn_amount_minus = QtWidgets.QPushButton(self.MainWindow)
        self.btn_amount_minus.setObjectName("btn_amount_minus")
        self.btn_amount_minus.setGeometry(QtCore.QRect(720, 900, 100, 100))
        self.btn_amount_minus.setFont(self.font_list[18])
        self.btn_amount_minus.setText("-")

    def create_tabs(self, tab_name_list) -> None:
        for tab_name in tab_name_list:
            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_%s" % tab_name)
            self.tabWidget.addTab(tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab),self.translate("MainWindow",tab_name))

            toolbox = QtWidgets.QToolBox(tab)
            toolbox.setGeometry(QtCore.QRect(0, 10, 1000, 900))
            toolbox.setFont(self.font_list[28])
            toolbox.setObjectName("toolbox_%s" % tab_name)

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

            toolbox.addItem(page, "")
            toolbox.setItemText(toolbox.indexOf(page),self.translate("MainWindow",page_name))

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

        x = 0
        y = 0
        for btn_name in btn_name_list:
            btn = QtWidgets.QPushButton(page)
            btn.setGeometry(QtCore.QRect(x, y, 200, 100))
            btn.setFont(self.font_list[14])
            btn.setObjectName(btn_name)
            btn.setText(self.translate("MainWindow", btn_name))
            self.btn_list[tab_name][page_name][btn_name] = btn

            x += 200
            if x == 1000:
                x = 0
                y += 100

        return

    def read_ui_design(self) -> None:
        ui_input_path = os.getcwd() + "\\data\\ui_input\\"
        tab_list = os.listdir(ui_input_path)
        self.design = {}
        for tab_file in tab_list:
            tab_name = re.split('[.]', tab_file)[1]
            self.design[tab_name] = {}
            with open (ui_input_path+tab_file, 'r') as f:  # read data from file
                data = f.readlines()
                f.close()

            for line in data:
                if line[0] == "[":
                    page_name = re.split('[][]', line)[1]
                    self.design[tab_name][page_name] = []
                    current_page = page_name
                else:
                    self.design[tab_name][current_page].append(line.split("\n")[0])

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

    class FavourSelectionWindow(object):
        def __init__(self):
            super().__init__()
            self.FavourSelectionWindow = QtWidgets.QMainWindow()
            self.FavourSelectionWindow.setWindowTitle("酱")
            self.FavourSelectionWindow.resize(600,400)
            return

        def create_favour_btns(self):
            favour_list = ["酸甜","椒盐","buffalo","辣酱","ranch","甜辣","蜂蜜","柠檬辣椒","greek"]
            self.favour_btns = {}
            x = 0
            y = 0
            for favour in favour_list:
                btn = QtWidgets.QPushButton(self.FavourSelectionWindow)
                btn.setGeometry(QtCore.QRect(x,y,150,100))
                font = QtGui.QFont()
                font.setPointSize(18)
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

    class BeerAmountWindow(object):
        def __init__(self):
            super().__init__()
            self.BeerAmountWindow = QtWidgets.QMainWindow()
            self.BeerAmountWindow.setWindowTitle("酱")
            self.BeerAmountWindow.resize(600,400)
            return

        def create_amount_btns(self):
            amount_list = ["6","9","12","18","21","24","36","48"]
            self.amount_btns = {}
            x = 0
            y = 0
            for amount in amount_list:
                btn = QtWidgets.QPushButton(self.BeerAmountWindow)
                btn.setGeometry(QtCore.QRect(x,y,150,100))
                font = QtGui.QFont()
                font.setPointSize(18)
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.read_ui_design()

    #ui.create_tabs(["点餐","酒水","其他"])
    #ui.create_pages(["前菜","主食","肉食","蔬菜","汤类","套餐"],"点餐")
    #ui.create_button(["蛋卷2条","蛋卷5条","春节1条","春卷5条"],"点餐","前菜")
    #ui.create_button(["炒饭","炒面","捞面","上海面","新加坡面"],"点餐","主食")
    #ui.create_button(["炒饭","炒面","捞面","上海面","新加坡面"],"点餐","主食")
    #ui.create_pages(["啤酒","洋酒","预调鸡尾酒","调酒","a","b","c","d","e","f","g","h"],"酒水")
    #ui.create_button(["Kokanee","Canadian","Bud Light"],"酒水","啤酒")

    ui.create_menu()
    ui.show()

    fwindow = ui.FavourSelectionWindow()
    fwindow.create_favour_btns()

    bwindow = ui.BeerAmountWindow()
    bwindow.create_amount_btns()

    sys.exit(app.exec_())