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
        self.__dataPath = "./data/"
        self.__orderList = orders

    def getOrders(self) -> List[int]:
        return self.__orderList

    def getPath(self) -> str:
        return self.__orderList


if __name__ == "__main__":
    r = Receipt()