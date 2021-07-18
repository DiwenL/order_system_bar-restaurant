"""
"""
import datetime
import os
import sys
import re

class Order(object):
    def __init__(self, name, menu, price=-1, amount=1, comments=[],) -> None:
        super().__init__()
        self.__name = name
        self.__price = 0
        self.set_price(price)
        self.__amount = amount
        self.__comment_list = comments
        self.__menu = menu
        self.__init_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__modify_time = datetime.datetime.now().strftime('%H:%M:%S')

    def get_total(self) -> float:
        return self.__price * self.__amount

    def set_price(self,price) -> None:
        try:
            if price == -1:
                self.__menu.get_price(self.__name)
            else:
                self.__price = float(price)
        except Exception as e:
            print("Order [%s] set price FAIL",)
            print(e)
        return

    def set_amount(self, amount) -> None:
        self.__amount = amount
        return

    def set_comment(self,comment_list) -> None:
        for comment in comment_list:
            self.__comment_list.append(comment)
        return

    def get_price(self) -> float:
        return self.__price

    def get_name(self):
        return self.__name

    def get_amount(self):
        return self.__amount

    def get_comments(self):
        return self.__comment_list

    def get_detail(self):
        s = "x%i   %s\n" % (self.get_amount(), self.get_name())
        if len(self.__comment_list)!=0:
            for comment in self.__comment_list:
                s += "  --%s\n" % comment
        s += "		$%i" % self.get_total()
        return s

    def get_info(self):
        s = "%ix  %s\n        %.2f" % (self.get_amount(), self.get_name(), self.get_total())
        return s