from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time
import os
from create_UI import *
from receipt import *
from order import *
from menu import *


class Main(QMainWindow, MainUI):

    def __init__(self):
        super(Main, self).__init__()
        self.menu = Menu()

        # init list for receipt
        self.unfinished_receipts = []
        self.finished_receipts = []

        self.fwindow = self.FavourSelectionWindow()  # init favour selection window
        self.fwindow.create_favour_btns()

        self.bwindow = self.BeerAmountWindow()  # init beer amount selection window
        self.bwindow.create_amount_btns()

        self.iwindow = self.InfoWindow()
        self.iwindow.show_customers()
        self.iwindow.btn_confirm.clicked.connect(self.btn_info_confirm_clicked)
        self.iwindow.btn_add.clicked.connect(self.btn_add_info_clicked)
        self.iwindow.list_info.clicked.connect(self.list_info_clicked)
        self.iwindow.text_search.textChanged.connect(self.text_search_changed)

        self.pwindow = self.PayWindow()
        self.pwindow.btn_cash.toggled.connect(self.btn_cash_toggled)
        self.pwindow.btn_card.toggled.connect(self.btn_card_toggled)
        self.pwindow.btn_emt.toggled.connect(self.btn_emt_toggled)
        self.pwindow.line_cash.textChanged.connect(self.pwindow.update_unpaid)
        self.pwindow.line_card.textChanged.connect(self.pwindow.update_unpaid)
        self.pwindow.line_emt.textChanged.connect(self.pwindow.update_unpaid)
        self.pwindow.btn_confirm.clicked.connect(self.btn_pay_confirm_clicked)
        self.pwindow.btn_cancel.clicked.connect(self.pwindow.close)

        self.cwindow = self.CommentWindow()
        self.cwindow.line_comment.returnPressed.connect(self.btn_comment_confirm_clicked)
        self.cwindow.btn_comment_confirm.clicked.connect(self.btn_comment_confirm_clicked)

        # connect default UI btns
        self.btn_new.clicked.connect(self.btn_new_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)
        self.btn_info.clicked.connect(self.btn_info_clicked)
        self.btn_print.clicked.connect(self.btn_print_clicked)
        self.btn_record.clicked.connect(self.btn_record_clicked)
        self.btn_pay.clicked.connect(self.btn_pay_clicked)
        self.btn_info.clicked.connect(self.btn_info_clicked)
        self.btn_amount_plus.clicked.connect(self.btn_amount_plus_clicked)
        self.btn_amount_minus.clicked.connect(self.btn_amount_minus_clicked)
        self.btn_price_plus.clicked.connect(self.btn_price_plus_clicked)
        self.btn_price_minus.clicked.connect(self.btn_price_minus_clicked)

        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        self.btn_favour.clicked.connect(self.btn_favour_clicked)
        self.btn_beer_amount.clicked.connect(self.btn_beer_amount_clicked)
        self.btn_delete_order.clicked.connect(self.btn_delete_order_clicked)
        self.btn_comment.clicked.connect(self.btn_comment_clicked)

        self.list_receipt.clicked.connect(self.list_receipt_clicked)

        self.tab_names = self.design.keys()
        self.color_list = [QColor(255, 126, 0, 40),QColor(255, 0, 125, 40),
                           QColor(126, 255, 0, 40),QColor(126, 0, 255, 40),
                           QColor(0, 126, 255, 40),QColor(0, 255, 126, 40)]
        self.colors = {}
        idx = 0
        for name in self.design.keys():
            self.colors[name] = self.color_list[idx]
            idx += 1

        # connect order btns
        for tab_name in self.btn_list.keys():
            tab = self.btn_list[tab_name]
            for page_name in tab:
                page = tab[page_name]
                for btn_name in page:
                    btn = page[btn_name]
                    btn.tab_name = tab_name
                    btn.clicked.connect(lambda ch,btn = btn: self.add_order(btn.text(),btn.tab_name))

        for amount_name in self.bwindow.amount_btns:
            btn = self.bwindow.amount_btns[amount_name]
            self.bwindow.amount_btns[amount_name].clicked.connect(lambda ch,btn = btn: self.set_beer_amount(btn.text()))

        for favour_name in self.fwindow.favour_btns:
            btn = self.fwindow.favour_btns[favour_name]
            self.fwindow.favour_btns[favour_name].clicked.connect(lambda ch,btn = btn: self.add_favour(btn.text()))

    def btn_add_info_clicked(self):
        name = self.iwindow.text_name.text()
        phone = self.iwindow.text_phone.text()

    def text_search_changed(self):
        try:
            text = self.iwindow.text_search.text()
            self.iwindow.show_customers(text)
        except Exception as e:
            print(e)

    def btn_comment_confirm_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return

        comment = self.cwindow.line_comment.text()
        self.current_order.add_comment(comment)
        self.update_order(self.current_order_idx)
        self.cwindow.close()
        return

    def set_beer_amount(self,amount):
        self.update_current_selected()
        if self.current_order_idx == -1:
            self.bwindow.close()
            return

        self.current_order.set_amount(int(amount))
        self.update_receipt(self.current_receipt_idx)
        self.update_order(self.current_order_idx)
        self.bwindow.close()

    def add_favour(self, favour):
        self.update_current_selected()
        if self.current_order_idx == -1:
            self.fwindow.close()
            return
        try:
            self.current_order.add_comment(favour)
            self.update_receipt(self.current_receipt_idx)
            self.update_order(self.current_order_idx)
            self.fwindow.close()
        except Exception as e:
            print(e)

    def btn_info_confirm_clicked(self):
        try:
            name = self.iwindow.text_name.text()
            phone = self.iwindow.text_phone.text()
            time = self.iwindow.text_time.text()

            self.update_current_selected()
            if self.current_receipt_idx == -1:
                return

            self.current_receipt.set_info(name,phone,time)
            self.iwindow.close()
            self.update_receipt(self.current_receipt_idx)
        except Exception as e:
            print(e)

    def btn_add_info_clicked(self):
        try:
            name = self.iwindow.text_name.text()
            phone_temp = self.iwindow.text_phone.text()
            phone = ['', '', '']
            _, phone[0], _, phone[1], phone[2] = re.split('[()-]',phone_temp)

            if name == "" or phone == "(___)-___-___":
                return
            if name in self.iwindow.customers:
                return

            self.iwindow.add_customers(name, phone)
        except Exception as e:
            print(e)

    def btn_cash_toggled(self):
        if self.pwindow.line_cash.isVisible():
            self.pwindow.line_cash.setVisible(False)
            self.pwindow.line_cash.setText("$")
        else:
            self.pwindow.line_cash.setVisible(True)
            self.pwindow.line_cash.setText("$%.2f" % self.pwindow.unpaid)

    def btn_card_toggled(self):
        if self.pwindow.line_card.isVisible():
            self.pwindow.line_card.setVisible(False)
            self.pwindow.line_card.setText("$")
        else:
            self.pwindow.line_card.setVisible(True)
            self.pwindow.line_card.setText("$%.2f" % self.pwindow.unpaid)

    def btn_emt_toggled(self):
        if self.pwindow.line_emt.isVisible():
            self.pwindow.line_emt.setVisible(False)
            self.pwindow.line_emt.setText("$")
        else:
            self.pwindow.line_emt.setVisible(True)
            self.pwindow.line_emt.setText("$%.2f" % self.pwindow.unpaid)

    def btn_pay_confirm_clicked(self):
        self.update_current_selected()
        if self.current_receipt_idx == -1:
            return

        if self.pwindow.line_cash.isVisible():
            cash = self.pwindow.line_cash.text().split("$")[1]
            if cash == ".":
                cash = 0
            else:
                cash = float(cash)
        else:
            cash = 0

        if self.pwindow.line_card.isVisible():
            card = self.pwindow.line_card.text().split("$")[1]
            if card == ".":
                card = 0
            else:
                card = float(card)
        else:
            card = 0

        if self.pwindow.line_emt.isVisible():
            emt = self.pwindow.line_emt.text().split("$")[1]
            if emt == ".":
                emt = 0
            else:
                emt = float(emt)
        else:
            emt = 0

        self.pwindow.unpaid = self.pwindow.total - cash - card - emt
        self.current_receipt.set_payments(cash, card, emt)
        self.update_receipt(self.current_receipt_idx)

        if self.pwindow.unpaid >= 0.01:
            self.iwindow.show()

        self.pwindow.close()
        print(self.current_receipt.get_payments())
        return

    def add_order(self,name,kind):
        if self.list_receipt.count() == 0:
            print("currently no receipt")
            return
        self.update_current_selected()

        try:
            od = Order(name,kind,self.menu)
            self.current_receipt.add_order(od)
            self.show_receipt(self.current_receipt)
        except Exception as e:
            print(e)
        self.update_receipt(self.current_receipt_idx)
        return

    def update_receipt(self, receipt_idx):
        self.unfinished_receipts[receipt_idx].store_receipt()
        self.list_receipt.item(receipt_idx).setText('---------------------------------------\n%s\n---------------------------------------' % self.unfinished_receipts[receipt_idx].get_info())
        return

    def update_order(self, order_idx):
        self.update_current_selected()
        if self.current_receipt_idx == -1:
            return
        text = self.current_receipt.get_order_byidx(order_idx).get_info()
        self.list_order.item(order_idx).setText('\n%s\n' % text)

    def show_receipt(self, receipt):
        self.clear_list_order()
        orders = receipt.get_orders()
        if len(orders) == 0:
            return

        for kind in orders:
            if len(orders[kind]) == 0:
                continue
            color = self.colors[kind]
            for order in orders[kind]:
                item = "\n%s\n" % order.get_info()
                self.list_order.addItem(item)
                self.list_order.item(self.list_order.count()-1).setBackground(color)

    def list_receipt_clicked(self):
        self.update_current_selected()
        if self.current_receipt_idx == -1:
            return
        self.show_receipt(self.current_receipt)
        return

    def list_info_clicked(self):
        current_info = self.iwindow.list_info.currentItem().text()
        name,phone = current_info.split("\n")
        self.iwindow.text_name.setText(name)
        self.iwindow.text_phone.setText(phone)
        return

    def clear_list_receipt(self):
        count = self.list_receipt.count()
        for i in range(count):
            self.list_receipt.takeItem(0)
        return

    def clear_list_order(self):
        count = self.list_order.count()
        for i in range(count):
            self.list_order.takeItem(0)
        return

    def update_current_selected(self):
        self.current_receipt_idx = self.list_receipt.currentRow()
        self.current_order_idx = self.list_order.currentRow()
        if self.current_receipt_idx == -1:
            self.current_receipt = None
            self.current_order = None
            return
        if self.current_order_idx == -1:
            self.current_receipt = self.unfinished_receipts[self.current_receipt_idx]
            self.current_order = None
            return
        self.current_receipt = self.unfinished_receipts[self.current_receipt_idx]
        self.current_order = self.current_receipt.get_order_byidx(self.current_order_idx)

    def btn_new_clicked(self):
        try:
            receipt = Receipt([])
            self.unfinished_receipts.append(receipt)

            receipt_info = receipt.get_info()
            self.list_receipt.addItem('---------------------------------------\n%s\n---------------------------------------' % receipt_info)

            self.show_receipt(receipt)
        except  Exception as e:
            print(e)
        self.list_receipt.setCurrentRow(self.list_receipt.count()-1)
        return

    def btn_delete_clicked(self):
        if self.list_receipt.count() == 0:  # if current no receipt
            return
        try:
            self.update_current_selected()  # update current receipt & order selected
            receipt = self.unfinished_receipts.pop(self.current_receipt_idx)  # pop receipt from list
            self.list_receipt.takeItem(self.current_receipt_idx)  # take receipt from UI
            del receipt
            count = self.list_receipt.count()
                    
            if count == 0:  # if no receipt after delete
                self.clear_list_order()  # clear order UI
                return
            if count == self.current_receipt_idx:  # if deleted receipt is last receipt
                self.current_receipt_idx -= 1  # show privious receipt
            else:
                self.list_receipt.setCurrentRow(self.current_receipt_idx)  # select the next receipt
                self.show_receipt(self.unfinished_receipts[self.current_receipt_idx])  # show the next receipt
        except Exception as e:
            print(e)
        return

    def btn_info_clicked(self):
        self.update_current_selected()
        try:
            if self.current_receipt_idx != -1:
                self.iwindow.text_name.setText(self.current_receipt.get_name())
                self.iwindow.text_phone.setText(self.current_receipt.get_phone())
                self.iwindow.text_time.setText(self.current_receipt.get_pickup())
        except Exception as e:
            print(e)

        self.iwindow.show()
        return

    def btn_print_clicked(self):
        self.update_current_selected()
        if self.current_receipt_idx == -1:
            return
        self.current_receipt.print_file()
        return

    def btn_record_clicked(self):
        self.update_current_selected()
        if self.current_receipt_idx == -1:
            return

        try:
            self.finished_receipts.append(self.unfinished_receipts.pop(self.current_receipt_idx))
            self.list_receipt.takeItem(self.current_receipt_idx)
            self.clear_list_order()
            if self.list_receipt.count() == 0:
                return
            if self.list_receipt.count() == self.current_receipt_idx:
                self.show_receipt(self.unfinished_receipts[self.current_receipt_idx-1])
            else:
                self.show_receipt(self.unfinished_receipts[self.current_receipt_idx])
        except Exception as e:
            print(e)
        return

    def btn_pay_clicked(self):
        self.update_current_selected()
        if self.current_receipt_idx != -1:
            payments = self.current_receipt.get_payments()
            total = self.current_receipt.get_total()
            unpaid = self.current_receipt.get_unpaid_amount()
            self.pwindow.set_context(total, unpaid, payments["cash"], payments["card"], payments["emt"])
            print("Current total$%.2f unpaid$%.2f" % (self.pwindow.total, self.pwindow.unpaid))
            self.pwindow.show()

        return

    def btn_amount_plus_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1 or self.current_receipt_idx == -1:
            return
        self.current_order.set_amount(self.current_order.get_amount() + 1)
        self.update_order(self.current_order_idx)
        self.update_receipt(self.current_receipt_idx)
        return

    def btn_amount_minus_clicked(self):
        self.update_current_selected()  # update receipt & order selected
        if self.current_order_idx == -1 or self.current_receipt_idx == -1:  # if no receipt & order exist, return
            return

        if self.current_order.get_amount() == 1:  # if current order amount is 1, then delete the order
            self.list_order.takeItem(self.current_order_idx)  # take order from order UI
            self.current_receipt.delete_order_byidx(self.current_order_idx)  # delete order form receipt
            del self.current_order
            self.show_receipt(self.current_receipt)  # refresh the order UI

        else:  # if current order has amount >1
            self.current_order.set_amount(self.current_order.get_amount() - 1)
            self.update_order(self.current_order_idx)  # update current order

        self.update_receipt(self.current_receipt_idx)  # refresh receipt UI
        return

    def btn_price_plus_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return

        try:
            self.current_order.set_total(self.current_order.get_total()+1)
            self.update_order(self.current_order_idx)
            self.update_receipt(self.current_receipt_idx)
        except Exception as e:
            print(e)
        return

    def btn_price_minus_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return

        try:
            if self.current_order.get_total() < 1:
                self.current_order.set_total(0)
            else:
                self.current_order.set_total(self.current_order.get_total() - 1)
            self.update_order(self.current_order_idx)
            self.update_receipt(self.current_receipt_idx)
        except Exception as e:
            print(e)
        return

    def btn_delete_order_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return

        self.current_receipt.delete_order_byidx(self.current_order_idx)
        self.update_receipt(self.current_receipt_idx)
        self.show_receipt(self.current_receipt)

    def btn_comment_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return

        self.cwindow.show()

    def btn_exit_clicked(self):
        try:
            reply = QMessageBox.question(self, "Exit 退出", "Sure to exit?\n确认退出？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
        except Exception as e:
            print(e)

        if reply == QMessageBox.Yes:
            self.MainWindow.close()

        return

    def btn_favour_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return
        self.fwindow.show()
        return

    def btn_beer_amount_clicked(self):
        self.update_current_selected()
        if self.current_order_idx == -1:
            return
        self.bwindow.show()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Main()
    myWin.MainWindow.showFullScreen()
    myWin.MainWindow.show()
    sys.exit(app.exec_())
