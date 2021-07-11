"""
this modul is for getting the price from menu.txt and update the database
if database not in enviroment, then using this modul as local database
"""

import re

class Menu(object):

    def __init__(self, db_connector=None) -> None:
        super().__init__()

        self.food_data_stat = False
        self.beer_data_stat = False
        self.wine_data_stat = False

        self.food_menu = {}
        self.beer_menu = {}
        self.wine_menu = {}
        self.other_menu = {}

        if db_connector is None:
            self.database_connection_stat = False
        else:
            self.database_connection_stat = True
            try:
                self.connection = db_connector
                self.update_database()
            except:
                print("database connection error")
        return

    def read_menu_file(self,menu_path) -> None:
        try:
            with open(menu_path,"r") as f:
                self.menu = f.readlines()
        except:
            print("read menu.txt error")
            return None

        for item in self.menu:
            temp = re.split('[][]', item)
            if temp[1] == "food":
                self.food_menu[temp[2]] = temp[3]
                continue
            if temp[1] == "beer":
                self.beer_menu[temp[2]] = temp[3]
                continue
            if temp[1] == "wine":
                self.wine_menu[temp[2]] = temp[3]
                continue
            if temp[1] == "other":
                self.wine_menu[temp[2]] = temp[3]
        return

    def update_database(self) -> None:
        if not self.database_connection_stat:
            print("database not connected")
            return

        try:
            self.connection.cursor.execute("select * from FOOD")
            food_data = self.connection.cursor.fetchall()
            self.food_data_stat = True
        except:
            print("FOOD database acquire error")

        try:
            self.connection.cursor.execute("select * from BEER")
            beer_data = self.connection.cursor.fetchall()
            self.beer_data_stat = True
        except:
            print("FOOD database acquire error")

        try:
            self.connection.cursor.execute("select * from WINE")
            wine_data = self.connection.cursor.fetchall()
            self.wine_data_stat = True
        except:
            print("FOOD database acquire error")

if __name__ == "__main__":
    print("executing menu modul")
    menu = Menu()
    menu.read_menu_file("abc")
    print(menu.database_connection_stat)
    print(menu.food_menu)