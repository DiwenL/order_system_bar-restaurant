"""
this modul is for connecting mysql database
created by: Diwen
"""
import pymysql
import sys


class DBConnector(object):

    def __init__(self, user, password, host="localhost", port=3306) -> None:
        super().__init__()

        self.user = user
        self.password = password
        self.host = host
        self.port = port

        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                charset='utf8')
            self.cursor = self.connection.cursor()
            self.cursor.execute("use cupar_menu")
            print("dbconnector: database connection init successfully")
        except:
            print("dbconnector: database connection init fail")
            print("dbconnector: error when init database connection: ", sys.exc_info()[0])

    def commit(self) -> None:
        self.connection.commit()
        return

    def close_cursor(self) -> None:
        self.cursor.close()
        return

    def disconnect(self) -> None:
        self.connection.close()
        return

    def get_price_food(self, name) -> float:
        self.cursor.execute("select * from FOOD where name = %s", name)
        return float(self.cursor.fetchone()[1])

    def insert_food(self, name, price) -> None:
        sql = "insert into food (name, price) value ('%s', %.2f)" %(name,price)
        self.cursor.execute(sql)
        self.commit()
        return

    def update_food(self, name, new_price) -> None:
        sql = "update food set price = %.2f where name = '%s'" % (new_price, food)
        self.connection.cursor.execute(sql)
        self.connection.commit()
        return

if __name__ == "__main__":
    print("this is db_connector's main function")
    dbc = DBConnector("root", "lidiwen0513")
    food = dbc.get_price_food("Wonton Soup")
    print(food)
