"""
"""
import datetime
import os
import sys
import re

class Order(object):
    PRICE_FILE = './input/price.txt'
    def __init__(self, name, price, amount=1, comments=[]) -> None:
        super().__init__()
        self.__name = name
        self.__price = price
        self.__amount = amount
        self.__comment_list = comments
        self.__init_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.__modify_time = datetime.datetime.now().strftime('%H:%M:%S')

    def get_total():
        return self.__price * self.__amount

    def read_price(self) -> None:
        
        with open(Order.PRICE_FILE,"r") as f:
            lines = f.readlines()
        
        self.foods = {}
        self.beers = {}
        self.wines = {}

        try:
            for line in lines:
                info = re.split("[][]",line)
                if info[1] == "food":
                    self.foods[info[2]] = float(info[3])
                    continue
                elif info[1] == "beer":
                    self.beers[info[2]] = float(info[3])
                    continue
                elif info[1] == "wine":
                    self.wines[info[2]] = float(info[3])
                    continue
        except:
            print("./input/price.txt file error, please check the file then retry ")

        return 


if __name__ == "__main__":
    o = Order("kokanee",6,3)
    o.read_price()
    print(o.foods)
    print(o.beers)
    print(o.wines)
    