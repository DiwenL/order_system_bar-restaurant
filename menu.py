"""
this module is for getting the price from menu.txt and update the database
if database not in environment, then using this module as local database
"""

import re
import os
from dbconnector import *
from order import *


class Menu(object):

    def __init__(self, db_connector=None) -> None:
        super().__init__()

        self.database_connection_stat = False

        self.tables_stat = {}
        self.menus = {}
        print("menu: start reading menu from input file")
        self.read_menu_file()

        if db_connector is not None:
            try:
                self.connection = db_connector
                self.connection.cursor.execute("use cupar_menu")
                self.connection.commit()
                print("menu: database connected SUCCESSFULLY")
                self.database_connection_stat = True
            except Exception as e:
                print(e)
                print("menu: database connected FAIL")

            # check tables all exist
            try:
                print("menu: start data tables check")
                self.tables_check()
                print("menu: table check SUCCESSFULLY\n")
            except Exception as e:
                print(e)
                print("menu: table check FAIL\n")

            # update database
            try:
                print("menu: updating price")
                self.update_database()
                print("menu: updated SUCCESSFULLY\n")
            except Exception as e:
                print(e)
                print("menu: price update FAIL\n")
        print("database not in use")
        return

    def read_menu_file(self, path="") -> None:
        if path == "":
            cwd = os.getcwd()
        else:
            cwd = path

        path = cwd + "\\data\\ui_input\\"

        files = os.listdir(path)

        for file in files:
            menu_name = file.split('.')[1]
            self.menus[menu_name] = {}

            # read file
            try:
                with open(path + file, "r") as f:
                    lines = f.readlines()
            except Exception as e:
                print(e)

            # get price
            for line in lines:
                line = line.splitlines()[0]
                if line[0] == "[":
                    current_kind = re.split('[][]',line)[1]
                    self.menus[menu_name][current_kind] = {}
                    continue
                try:
                    name_cn, name_en, price = re.split('[|$]', line)
                except:
                    temp = re.split('[$]',line)
                    name_cn, name_en, price = temp[0], temp[0], temp[1]

                self.menus[menu_name][current_kind][name_cn] = {}
                self.menus[menu_name][current_kind][name_cn]["name_en"] = name_en
                self.menus[menu_name][current_kind][name_cn]["price"] = price

            print("menu: read [%s] completed." % file)

        return

    def tables_check(self) -> None:

        if not self.database_connection_stat:
            print("menu: database not connected, tables check end")
            return

        for menu in self.menus_name:
            try:  # check menus
                self.connection.cursor.execute("select * from %s" % menu)
                self.tables_stat[menu] = True
                print("[%s] table test SUCCESSFULLY" % menu)
            except Exception as e:
                print("[%s] table connected FAIL: " % menu, e, end="\n")

        return

    def update_database(self) -> None:
        """
        this function will acquire food, beer, wine, other data from database if exist
        :input: None
        :return: None
        """
        if not self.database_connection_stat:
            print("menu: database not connected, database update end")  # if database is not connected, return
            return

        # update food database from food menu file
        for menu in self.menus_name:
            if self.tables_stat[menu]:
                dif = {}
                new = {}

                for item in self.menus[menu]:
                    try:  # check if food is in database
                        result = self.connection.get_price_food(item)  # acquire the price

                        if self.menus[menu][item] != result:  # if the price from database is different from menu file
                            dif[item] = [result, self.menus[menu][item]]  # record the different
                    except Exception as e:  # if the food is not in database
                        print("[%s] not in %s table" % (item, menu))
                        new[item] = self.menus[menu][item]

                print("menu: [%s] menu compare completed" % menu)
                print("%i [%s] price changed" % (len(dif), menu))
                print("%i new [%s]" % (len(new), menu))

                # update new food price
                if len(dif) != 0:
                    for item in dif:
                        try:
                            self.connection.update_food(menu, item, dif[1])
                            self.connection.commit()
                            print("[%s] %.2f -> %.2f updated successfully" % (item, dif[item][0], dif[item][1]))
                        except Exception as e:
                            print("update [%s] FAIL: " % item, e)

                # insert new food
                if len(new) != 0:
                    for item in new:
                        try:
                            self.connection.insert_food(menu, item, new[item])
                            self.connection.commit()
                            print("new %s [%s] $%.2f updated successfully" % (menu, item, new[item]))
                        except Exception as e:
                            print("insert [%s] FAIL: " % item, e)

        return

    def get_price(self, name, kind) -> float:
        if self.database_connection_stat:
            try:
                price = self.connection.get_price(name, kind)
            except Exception as e:
                print("menu: get price for [%s] from database [%s] FAIL: " % (name, kind), e)
                price = -1
            return price
        else:  # using local menu data
            for menu in self.menus[kind]:
                if name in self.menus[kind][menu]:
                    price = float(self.menus[kind][menu][name]["price"])
                    return price
            print("menu: get price for [%s] from local [%s] FAIL" % (name, kind))
            price = -1
            return price

if __name__ == "__main__":
    print("executing MENU module main function")
    db = DBConnector("root", "lidiwen0513")
    menu = Menu()
