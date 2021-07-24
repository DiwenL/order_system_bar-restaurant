import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Create_UI(object):
    def setupUI(self,MainWindow):
        MainWindow.setObjectName("Cupar Bar Order System")  # set window's name
        MainWindow.resize(1920, 1080)  # set windows size

        self.translate = QtCore.QCoreApplication.translate

        self.font_list = []
        for i in range(1, 31):
            font = QtGui.QFont()
            font.setPointSize(i)
            self.font_list.append(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)  # set main widget
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)  # set tab widget
        self.tabWidget.setGeometry(QtCore.QRect(920, 0, 1000, 1000))  # set tab widget size
        self.tabWidget.setFont(self.font_list[24])
        self.tabWidget.setObjectName("tab_menu")


        self.tab_list = {}
        self.toolbox_list = {}
        self.page_list = {}
        self.btn_list = {}

    def create_tabs(self, tab_name_list) -> None:
        for tab_name in tab_name_list:
            tab = QtWidgets.QWidget()
            tab.setObjectName("tab_%s" % tab_name)
            self.tabWidget.addTab(tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab),self.translate("MainWindow",tab_name))

            toolbox = QtWidgets.QToolBox(tab)
            toolbox.setGeometry(QtCore.QRect(0, 10, 1000, 900))
            toolbox.setFont(self.font_list[20])
            toolbox.setObjectName("toolbox_%s" % tab_name)

            self.tab_list[tab_name] = tab
            self.toolbox_list[tab_name] = toolbox
            self.page_list[tab_name] = {}
            self.btn_list[tab_name] = {}

        return

    def create_pages(self, page_name_list, tab_name):
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
                y += 200

        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Create_UI()
    ui.setupUI(MainWindow)
    ui.create_tabs(["点餐","酒水","其他"])
    ui.create_pages(["前菜","主食","肉食","蔬菜","汤类","套餐"],"点餐")
    ui.create_button(["蛋卷2条","蛋卷5条","春节1条","春卷5条"],"点餐","前菜")
    ui.create_button(["炒饭","炒面","捞面","上海面","新加坡面"],"点餐","主食")
    ui.create_button(["炒饭","炒面","捞面","上海面","新加坡面"],"点餐","主食")
    ui.create_pages(["啤酒","洋酒","预调鸡尾酒","调酒","a","b","c","d","e","f","g","h"],"酒水")
    ui.create_button(["Kokanee","Canadian","Bud Light"],"酒水","啤酒")
    MainWindow.show()
    sys.exit(app.exec_())