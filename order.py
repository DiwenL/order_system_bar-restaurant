"""
"""
import datetime
import os
import sys
import re
import math


class Order(object):
    def __init__(self, name, kind, menu, price=-1, amount=1, comments=[]) -> None:
        super().__init__()
        self.__name = name
        self.__kind = kind
        self.__menu = menu
        self.__price = 0
        self.__price_range = None
        self.__amount = amount
        self.set_price(price)
        self.__total = self.__price * self.__amount
        self.__comment_list = []

    def get_total(self) -> float:
        return self.__total

    def set_price(self, price) -> None:
        if price == -1:
            name = self.get_name()
            kind = self.get_kind()
            temp = self.__menu.get_price(name, kind)
            if type(temp) == list:
                self.__price_range = temp

                if self.__amount < self.__price_range[0]:
                    self.__amount = self.__price_range[0]

                price_gradient = (self.__price_range[3] - self.__price_range[2]) / (
                        self.__price_range[1] - self.__price_range[0])
                self.__total = math.ceil(
                    price_gradient * (self.__amount - self.__price_range[0]) + self.__price_range[2])
                self.__price = self.__total / self.__amount
            else:
                self.__price = float(temp)
        else:
            self.__price = float(price)
        return

    def set_amount(self, amount) -> None:
        self.__amount = amount
        if self.__price_range is None:
            self.__total = self.__price * self.__amount
        else:
            self.set_price(-1)

    def set_total(self, total) -> None:
        self.__total = total

    def add_comment(self, comment) -> None:
        self.__comment_list.append(comment)
        return

    def get_kind(self):
        return self.__kind

    def get_price(self) -> float:
        return self.__price

    def get_price_range(self):
        return self.__price_range

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
        s1 = "[%s] %ix %s" % (self.get_kind(), self.get_amount(), self.get_name())
        s2 = "$%.2f" % self.get_total()
        s = s1.ljust(25) + s2.rjust(8)
        for comment in self.__comment_list:
            s += "\n                     -%s" % comment
        return s
