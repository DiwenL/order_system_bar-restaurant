"""
Receipt class, contains Order objs list and operations in modifying the receipt
"""
from typing import *
import win32api
import win32print
import tempfile
import datetime
import os,sys
import re

class Receipt(object):

    count = 0

    def __init__(self, orders=[]) -> None:
        self.__orderList = orders  # create order list
        currentDate = datetime.datetime.now().strftime('%Y-%m-%d')  # get today's date
        self.__dataPath = "./data/%s/" % currentDate  # init today's data file path
        if not os.path.exists(self.__dataPath):  # if path not exist
            print("today's data path not exist")
            try:  # create path
                os.mkdir(self.self.__dataPath)
            except Exception as e:  # try another way to make path
                os.makedirs(self.self.__dataPath)

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


    def getOrders(self) -> List[int]:
        return self.__orderList

    def getPath(self) -> str:
        return self.__dataPath

if __name__ == "__main__":
    r = Receipt()