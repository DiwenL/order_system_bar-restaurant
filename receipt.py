"""
Receipt class, contains Order objs list and operations in modifying the receipt
"""
from typing import *
from order import *
import win32api
import win32print
import tempfile
import datetime
import os,sys
import re


class Receipt(object):

    count = 0

    def __init__(self, orders=[]) -> None:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # get today's date
        self.__dataPath = ".\\data\\receipt\\%s\\" % current_date  # init today's data file path

        # create data path if not exist
        if not os.path.exists(self.__dataPath):  # if path not exist
            print("today's data path not exist")
            try:  # create path
                os.mkdir(self.__dataPath)
            except Exception as e:  # try another way to make path
                os.makedirs(self.__dataPath)

        # calculate current receipt num
        receipt_num_list = []
        receipt_files = os.listdir(self.__dataPath)  # get today's receipts
        if len(receipt_files) == 0:  # if currently empty
            print("current no receipt")
            Receipt.count = 1
            self.__receipt_num = Receipt.count
        else:  # if there exist receipt in today's data
            for receipt_file in receipt_files:
                receipt_num_list.append(int(re.split('[#.]', receipt_file)[1]))  # append receipt num to list
            Receipt.count = max(receipt_num_list) + 1  # the max num in list is the current receipt count
            self.__receipt_num = Receipt.count

        self.receipt_dir = self.__dataPath + "\\" + "#" + str(self.__receipt_num) + ".txt"
        self.__orders = {}  # create order list
        self.__info = {"name": "", "phone": "", "pickup": ""}
        self.__payments = {"cash":0, "card":0, "emt":0}
        self.__unpaid_amount = 0
        self.__paid_amount = 0
        self.__init_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__modify_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__total = 0
        if len(orders) != 0:
            for order in orders:
                self.add_order(order)

        kinds = os.listdir(".\\data\\ui_input\\")
        for kind in kinds:
            kind = kind.split(".")[1]
            self.__orders[kind] = []

        self.store_receipt()

    def set_paid_amount(self, amount):
        self.__paid_amount = amount

    def set_unpaid_amount(self, amount):
        self.__unpaid_amount = amount

    def set_payments(self, cash_amount=0, card_amount=0, emt_amount=0):
        self.__payments["cash"] = cash_amount
        self.__payments["card"] = card_amount
        self.__payments["emt"] = emt_amount
        self.set_paid_amount(cash_amount + card_amount + emt_amount)
        self.set_unpaid_amount(self.get_total() - self.get_paid_amount())

    def set_info(self, name="", phone="", time=""):
        if name != "":
            self.__info["name"] = name
        if phone != "":
            self.__info["phone"] = phone
        if time != ":":
            self.__info["pickup"] = time
        self.store_receipt()
        return

    def add_order(self, order):
        kind = order.get_kind()
        self.__orders[kind].append(order)
        self.__total = order.get_total()
        self.__modify_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.store_receipt()
        return

    def get_order_byidx(self,index):
        idx = 0
        for kind in self.__orders:
            for order in self.__orders[kind]:
                if idx == index:
                    return order
                else:
                    idx += 1

    def store_receipt(self):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        with open(self.receipt_dir, "w") as f:

            f.write("Cupar Hotel\n")
            f.write("%s\n" % current_date)
            f.write("init: %s\n" % self.__init_time)
            f.write("modify: %s\n" % current_time)
            f.write("#" + str(self.__receipt_num) + "\n")

            for kind in self.__orders:
                f.write("[%s]\n" % kind)
                for order in self.__orders[kind]:
                    f.write("%sx%s\n" % (order.get_amount(),order.get_name()))

                    comments = order.get_comments()
                    if comments:
                        for comment in comments:
                            f.write("     -" + comment + "\n")

                    f.write("        $%.2f\n" % order.get_total())
            f.write("=================\n")

            f.write("Total   $%.2f\n" % self.get_total())

            for info in self.__info:
                if self.__info[info] != "":
                    f.write("%s : %s\n" % (info, self.__info[info]))

            f.write("[PAID] $%.2f\n" % self.get_paid_amount())

            if self.get_unpaid_amount() >= 0.01:
                f.write("[UNPAID] $%.2f\n" % self.get_unpaid_amount())

            for payment in self.__payments:
                if self.__payments[payment] != 0:
                    f.write(" -%s $%.2f\n" % (payment, self.__payments[payment]))
        f.close()

    def get_orders(self) -> dict:
        return self.__orders

    def get_receipt_num(self) -> int:
        return self.__receipt_num

    def get_total(self) -> float:
        total = 0
        for kind in self.__orders:
            for order in self.__orders[kind]:
                total += order.get_total()
        self.__unpaid_amount = total - self.__paid_amount
        return total

    def get_paid_amount(self):
        return self.__paid_amount

    def get_unpaid_amount(self):
        return self.__unpaid_amount

    def get_payments(self):
        return self.__payments

    def get_info(self):
        s = "#%i (%s) total: $%.2f" % (self.__receipt_num,self.__init_time,self.get_total())
        if self.__info["name"] != "" or self.__info["phone"] != "":
            s += "\n %s  %s" % (self.__info["name"], self.__info["phone"])
        s += "\npaid: $%.2f  unpaid: $%.2f" % (self.__paid_amount, self.__unpaid_amount)
        return s

    def get_name(self):
        return self.__info["name"]

    def get_phone(self):
        return self.__info["phone"]

    def get_pickup(self):
        return self.__info["pickup"]

    def print_file(self, file = ""):
        if file == "":
            file = self.receipt_dir

        open(file,"r")
        win32api.ShellExecute(0, "print", file, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)

    def delete_order_byidx(self, order_idx):
        idx1 = 0
        for kind in self.__orders:
            for idx2 in range(len(self.__orders[kind])):
                if idx1 == order_idx:
                    self.__orders[kind].pop(idx2)
                    print("delete success")
                    return
                idx1 += 1
        self.store_receipt()

    def __del__(self):
        if os.path.exists(self.receipt_dir):
            os.remove(self.receipt_dir)
        return


if __name__ == "__main__":
    r = Receipt()