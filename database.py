import mysql.connector


class Connection:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="", # your username
            password="", # your password
            database=""  # your database name
        )

        self.cursor = self.mydb.cursor()
        self.create_user_table()
        self.create_place_table()
        self.create_reservation_table()

    def create_user_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS user (
                national_code VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                image BLOB NULL,
                PRIMARY KEY (national_code)
            );"""
        self.cursor.execute(sql)

    def create_place_table(self):
        sql = """
           CREATE TABLE IF NOT EXISTS place (
                place_name VARCHAR(255) NOT NULL,
                place_phone VARCHAR(255) NOT NULL,
                place_price INT NOT NULL,
                PRIMARY KEY (place_name)
           );"""
        self.cursor.execute(sql)

    def create_reservation_table(self):
        sql = """
          CREATE TABLE IF NOT EXISTS reservation (
               national_code VARCHAR(255) NOT NULL,
               place_name VARCHAR(255) NOT NULL,
               reservation_date DATE,
               PRIMARY KEY (national_code, place_name, reservation_date),
               FOREIGN KEY (national_code) REFERENCES user(national_code),
               FOREIGN KEY (place_name) REFERENCES place(place_name)
          );"""
        self.cursor.execute(sql)


db = Connection()
