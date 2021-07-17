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

