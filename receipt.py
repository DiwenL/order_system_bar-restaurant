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
        self.__orders = {}  # create order list
        self.__info = {"name": "", "phone": "", "pickup": "", "pay": ""}
        self.__init_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__modify_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__total = 0
        if len(orders) != 0:
            for order in orders:
                self.add_order(order)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # get today's date
        self.__dataPath = ".\\data\\receipt\\%s\\" % current_date  # init today's data file path

        kinds = os.listdir(".\\data\\ui_input\\")
        for kind in kinds:
            kind = kind.split(".")[1]
            self.__orders[kind] = []
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
                receipt_num_list.append(int(re.split('[#.]',receipt_file)[1]))  # append receipt num to list
            Receipt.count = max(receipt_num_list) + 1  # the max num in list is the current receipt count
            self.__receipt_num = Receipt.count

        self.store_receipt()

    def set_info(self,name = None,phone = "",time = "",pay = ""):
        if name != "":
            self.__info["name"] = name
        if phone != "":
            self.__info["phone"] = phone
        if time != "":
            self.__info["time"] = time
        if pay != "":
            self.__info["pay"] = pay
        return


    def add_order(self, order):
        kind = order.get_kind()
        self.__orders[kind].append(order)
        self.__total += order.get_total()
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
        receipt_dir = self.__dataPath + "\\" + "#" + str(self.__receipt_num) + ".txt"

        with open(receipt_dir, "w") as f:

            f.write("Cupar Hotel\n")
            f.write(current_date + " " + current_time + "\n")
            f.write("#" + str(self.__receipt_num) + "\n")

            total = 0
            for kind in self.__orders:
                f.write("=================\n")
                f.write("[%s]" % kind)
                for order in self.__orders[kind]:
                    f.write("%sx    %s\n          $%.2f" % (order.get_amount(),order.get_name(),order.get_total()))

                    comments = order.get_comments()
                    if comments:
                        for comment in comments:
                            f.write("     -" + comment + "\n")

                    f.write("        $%.2f\n" % order.get_total())
                    f.write("-----------------\n")

            f.write("Total   $%.2f\n" % self.__total)

            for info in self.__info:
                if self.__info[info] is not None:
                    f.write("%s : %s" % (info, self.__info[info]))

        f.close()

    def get_orders(self) -> dict:
        return self.__orders

    def get_receipt_num(self) -> int:
        return self.__receipt_num

    def get_total(self) -> float:
        if len(self.__orders.keys()) == 0:
            return 0

        total = 0
        for kind in self.__orders:
            for order in self.__orders[kind]:
                total += order.get_total()
        return total

    def get_info(self):
        s = "#%i (%s) total: $%.2f" % (self.__receipt_num,self.__init_time,self.get_total())
        if self.__info["name"] != "" or self.__info["phone"] != "":
            s += "\n %s  %s" % (self.__info["name"], self.__info["phone"])

        return s

    def delete_order_byidx(self,orderIdx):
        idx1 = 0
        for kind in self.__orders:
            for idx2 in range(len(self.__orders[kind])):
                if idx1 == orderIdx:
                    self.__orders[kind].pop(idx2)
                    print("delete success")
                    return
                idx1 += 1

    def __del__(self):
        receipt_dir = self.__dataPath + "\\" + "#" + str(self.__receipt_num) + ".txt"
        if os.path.exists(receipt_dir):
            os.remove(receipt_dir)
        return

if __name__ == "__main__":
    r = Receipt()