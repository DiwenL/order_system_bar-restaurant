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

        self.food_data_stat = False
        self.beer_data_stat = False
        self.wine_data_stat = False
        self.other_menu_stat = False

        self.food_menu = {}
        self.beer_menu = {}
        self.wine_menu = {}
        self.other_menu = {}

        print("\nstart reading menu from input file")
        self.read_menu_file("\\input\\price.txt")

        if db_connector is None:
            self.database_connection_stat = False
        else:
            self.database_connection_stat = True
            try:
                self.connection = db_connector
                print("database connected")
                self.update_database()
                print("database updated")
            except Exception as e:
                print(e)

        return

    def read_menu_file(self, menu_path) -> None:
        cwd = os.getcwd()
        try:
            with open(cwd+menu_path, "r") as f:
                self.menu = f.readlines()
        except:
            print("read menu.txt error")
            return None

        food_count = 0
        beer_count = 0
        wine_count = 0
        other_count = 0
        unidentified_count = 0

        for item in self.menu:
            try:
                temp = re.split('[][]', item)
                if temp[1] == "food":
                    self.food_menu[temp[2]] = float(temp[3])
                    food_count += 1
                    continue
                if temp[1] == "beer":
                    self.beer_menu[temp[2]] = float(temp[3])
                    beer_count += 1
                    continue
                if temp[1] == "wine":
                    self.wine_menu[temp[2]] = float(temp[3])
                    wine_count += 1
                    continue
                if temp[1] == "other":
                    self.other_menu[temp[2]] = float(temp[3])
                    other_count += 1
                    continue
                unidentified_count += 1
                print('item "%s" not recognized' % temp[2])
            except Exception as e:
                print(e)
                unidentified_count += 1
                print('item "%s" not recognized' % item)

        print("read menu completed.")
        print("food item: %i" % food_count)
        print("beer item: %i" % beer_count)
        print("wine item: %i" % wine_count)
        print("other item: %i" % other_count)
        print("unidentified item: %i" % unidentified_count)

        return

    def update_database(self) -> None:
        """
        this function will acquire food, beer, wine, other data from database if exist
        :input: None
        :return: None
        """
        if not self.database_connection_stat:
            print("database not connected")  # if database is not connected, return
            return

        try:  # check food menu
            self.connection.cursor.execute("select * from FOOD")
            self.food_data_stat = True
        except:
            print("FOOD data acquire error")

        try:  # check beer menu
            self.connection.cursor.execute("select * from BEER")
            self.beer_data_stat = True
        except:
            print("BEER data acquire error")

        try:  # check wine menu
            self.connection.cursor.execute("select * from WINE")
            self.wine_data_stat = True
        except:
            print("WINE data acquire error")

        try:  # check other menu
            self.connection.cursor.execute("select * from OTHER")
            self.other_menu_stat = True
        except:
            print("OTHER data acquire error")

        print("data acquire stat: FOOD--%s BEER--%s WINE--%s OTHER--%s"%(self.food_data_stat,self.beer_data_stat,self.wine_data_stat,self.other_menu_stat))

        # update food database from food menu file
        if self.food_data_stat is True:
            food_diff = {}
            food_new = {}
            for food in self.food_menu:
                try:  # check if food is in database
                    result = self.connection.get_price_food(food)  # acquire the price
                    print("[%s] price acquired: %.2f " %(food,result))

                    if self.food_menu[food] != result:  # if the price from database is different from menu file
                        food_diff[food] = [result,self.food_menu[food]]  # record the different
                except:  # if the food is not in database
                    print("[%s] not in database" %food)
                    food_new[food] = self.food_menu[food]

            print("updating food database")

            print("%i food's price changed" %len(food_diff))
            for food in food_diff:
                try:
                    sql = "update food set price = %.2f where name = '%s'" %(food_diff[food][1],food)
                    self.connection.cursor.execute(sql)
                    self.connection.commit()
                    print("[%s] %.2f -> %.2f updated successfully" % (food, food_diff[food][0], food_diff[food][1]))
                except:
                    print("update [%s] fail" %food)

            print("%i new food" %len(food_new))
            for food in food_new:
                sql = "insert into food (name, price) value ('%s', %.2f)" %(food, food_new[food])
                self.connection.cursor.execute(sql)
                self.connection.commit()
                print("new food [%s] %.2f updated sccessfully" % (food, food_new[food]) )

if __name__ == "__main__":
    print("executing menu module main function")
    db = DBConnector("root","lidiwen0513")
    menu = Menu(db)
    print(menu.database_connection_stat)
