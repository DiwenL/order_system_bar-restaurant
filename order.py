"""
"""
import datetime
import os
import sys
import re


class Order(object):
    def __init__(self, name, kind, menu, price=-1, amount=1, comments=[]) -> None:
        super().__init__()
        self.__name = name
        self.__kind = kind
        self.__menu = menu
        self.__price = 0
        self.set_price(price)
        self.__amount = amount
        self.__comment_list = comments

    def get_total(self) -> float:
        return self.__price * self.__amount

    def set_price(self, price) -> None:
        if price == -1:
            name = self.get_name()
            kind = self.get_kind()
            self.__price = self.__menu.get_price(name, kind)
        else:
            self.__price = float(price)
        return

    def set_amount(self, amount) -> None:
        self.__amount = amount
        return

    def set_comment(self, comment_list) -> None:
        for comment in comment_list:
            self.__comment_list.append(comment)
        return

    def get_kind(self):
        return self.__kind

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
        if len(self.__comment_list) != 0:
            for comment in self.__comment_list:
                s += "  --%s\n" % comment
        s += "		$%i" % self.get_total()
        return s

    def get_info(self):
        s1 = "[%s] %ix %s" % (self.get_kind(),self.get_amount(), self.get_name())
        s2 = "$%.2f" %  self.get_total()
        s = s1.ljust(25) + s2.rjust(8)
        return s
