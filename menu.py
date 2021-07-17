"""
this modul is for getting the price from menu.txt and update the database
if database not in enviroment, then using this modul as local database
"""

import re
import os
from dbconnector import *


class Menu(object):

    def __init__(self, db_connector=None) -> None:
        super().__init__()

        self.database_connection_stat = False

        self.food_data_stat = False
        self.beer_data_stat = False
        self.wine_data_stat = False
        self.other_menu_stat = False

        self.food_menu = {}
        self.beerin_menu = {}
        self.beergo_menu = {}
        self.wine_menu = {}
        self.other_menu = {}

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

            try:
                print("menu: start data tables check")
                self.tables_check()
                print("menu: table check SUCCESSFULLY\n")
            except Exception as e:
                print(e)
                print("menu: table check FAIL\n")

            try:
                print("menu: updating price")
                self.update_database()
                print("menu: updated SUCCESSFULLY\n")
            except Exception as e:
                print(e)
                print("menu: price update FAIL\n")

        return

    def read_menu_file(self,path="") -> None:
        if path == "":
            cwd = os.getcwd()
        else:
            cwd = path

        # read food menu from file
        try:
            with open(cwd + "\\data\\menu\\food_menu.txt", "r") as f:
                foods = f.readlines()
        except Exception as e:
            print("menu: read food_menu.txt error ",e)
            return None

        unidentified = []

        for food in foods:
            food = food.split("\n")[0]
            temp = re.split('[][]', food)
            try:
                self.food_menu[temp[2]] = float(temp[3])
            except Exception as e:
                unidentified.append(food)
                print("menu: unidentified [%s]: " % food, e)
        print("menu: read food from input file completed.")
        print("[food] item: %i" % len(self.food_menu))
        print("[beerin] item: %i" % len(self.beerin_menu))
        print("[wine] item: %i" % len(self.wine_menu))
        print("[other] item: %i" % len(self.other_menu))
        print("[unidentified] item: %i\n" % len(unidentified))

        return

    def tables_check(self) -> None:

        if not self.database_connection_stat:
            print("menu: database not connected, tables check end")
            return

        try:  # check food menu
            self.connection.cursor.execute("select * from FOOD")
            self.food_data_stat = True
            print("[food] table connected SUCCESSFULLY")
        except Exception as e:
            print("[food] table connected FAIL: ",e,end="\n")

        try:  # check beer menu
            self.connection.cursor.execute("select * from BEER")
            self.beer_data_stat = True
            print("[beer] table connected SUCCESSFULLY")
        except Exception as e:
            print("[beer] table connected FAIL: ",e,end="\n")

        try:  # check wine menu
            self.connection.cursor.execute("select * from WINE")
            self.wine_data_stat = True
            print("[wine] table connected SUCCESSFULLY")
        except Exception as e:
            print("[wine] table connected FAIL: ",e,end="\n")

        try:  # check other menu
            self.connection.cursor.execute("select * from OTHER")
            self.other_menu_stat = True
            print("[other] table connected SUCCESSFULLY")
        except Exception as e:
            print("[other] table connected FAIL: ",e,end="\n")

        print("menu: tables stat: FOOD--%s BEER--%s WINE--%s OTHER--%s"%(self.food_data_stat,self.beer_data_stat,self.wine_data_stat,self.other_menu_stat))

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
        if self.food_data_stat is True:
            food_dif = {}
            food_new = {}
            for food in self.food_menu:
                try:  # check if food is in database
                    result = self.connection.get_price_food(food)  # acquire the price

                    if self.food_menu[food] != result:  # if the price from database is different from menu file
                        food_dif[food] = [result,self.food_menu[food]]  # record the different
                except:  # if the food is not in database
                    print("[%s] not in database" %food)
                    food_new[food] = self.food_menu[food]

            print("menu: food menu compare completed")
            print("%i food's price changed" % len(food_dif))
            print("%i new food" % len(food_new))

            # update new food price
            if len(food_dif) != 0:
                for food in food_dif:
                    try:
                        self.connection.update_food(food,food_dif[1])
                        print("[%s] %.2f -> %.2f updated successfully" % (food, food_dif[food][0], food_dif[food][1]))
                    except Exception as e:
                        print("update [%s] FAIL: " %food, e)

            # insert new food
            if len(food_new) != 0:
                for food in food_new:
                    try:
                        self.connection.insert_food(food,food_new[food])
                        print("new food [%s] %.2f updated successfully" % (food, food_new[food]) )
                    except Exception as e:
                        print("insert [%s] FAIL: "%food, e)

        if self.beer_data_stat is True:
            beer_dif = {}
            beer_new = {}

            for beer in self.beerin_menu:
                for kind in beer:
                    price = self.beerin_menu[kind]


            
if __name__ == "__main__":
    print("executing MENU module main function")
    db = DBConnector("root","lidiwen0513")
    menu = Menu(db)
    print(menu.database_connection_stat)
