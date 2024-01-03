from database import db
from datetime import datetime, timedelta


def add_new_user():
    first_name = input("enter a first_name: ")
    last_name = input("enter a last_name: ")
    national_code = input("enter a national code")

    db.cursor.execute("""
        INSERT INTO user(first_name, last_name, national_code)
        VALUES (%s, %s, %s)""",
                      (first_name, last_name, national_code)
                      )
    db.mydb.commit()
    print("new user added successfully!")


def add_new_place():
    name = input("enter place name: ")
    phone = input("Enter place phone number: ")
    price = int(input("Enter place price: "))

    db.cursor.execute("""
        INSERT INTO place(place_name, place_phone, place_price)
        VALUES (%s, %s, %s)""",
                      (name, phone, price)
                      )
    db.mydb.commit()
    print("new place added seccessfully!")


def add_reservation():
    user = input("enter national code for reservation: ")
    place_name = input("Enter place name for reservation: ")
    reservation_date = datetime.now()

    db.cursor.execute("""
        INSERT INTO reservation (national_code, place_name, reservation_date)
        VALUES (%s, %s, %s)""",
                      (user, place_name, reservation_date)
                      )
    db.mydb.commit()
    print("new reservation seccessfully created")


def edit_user_information():
    national_code = input("enter your national code: ")

    new_first_name = input("Enter new first name: ")
    new_last_name = input("Enter new last name: ")

    db.cursor.execute("""
    UPDATE user SET
    first_name = %s,
    last_name = %s
    """, (
        new_first_name,
        new_last_name
    ))
    db.mydb.commit()
    print("update user seccessfully!")


def show_user_reservation_info():
    national_code = input("Enter the national code: ")

    # Select user information
    db.cursor.execute("""
        SELECT first_name, last_name, image
        FROM user
        WHERE national_code = %s
    """, (national_code,))
    user_info = db.cursor.fetchone()

    if user_info:
        print(f"User Information:")
        print(f"Name: {user_info[0]} {user_info[1]}")
        print(f"Image: {user_info[2]}")
    else:
        print("User not found!")
        return

    db.cursor.execute("""
        SELECT place_name, COUNT(reservation_date) AS reservation_count
        FROM reservation
        WHERE national_code = %s
        GROUP BY place_name
    """, (national_code,))

    reservations_info = db.cursor.fetchall()

    if reservations_info:
        print("\nReservations:")
        for place_info in reservations_info:
            print(f"Place: {place_info[0]}, Reservation Count: {place_info[1]}")
    else:
        print("No reservations found for this user.")


def show_user_reservations_in_date_range():
    national_code = input("Enter the national code: ")

    try:
        start_date_str = input("Enter the start date (YYYY-MM-DD): ") #2023-01-01
        end_date_str = input("Enter the end date (YYYY-MM-DD): ") #2023-01-02

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use the format YYYY-MM-DD.")
        return

    db.cursor.execute("""
        SELECT place_name, reservation_date
        FROM reservation
        WHERE national_code = %s AND reservation_date BETWEEN %s AND %s
    """, (national_code, start_date, end_date))

    reservations_info = db.cursor.fetchall()

    if reservations_info:
        print("\nReservations in the Date Range:")
        for place_info in reservations_info:
            print(f"Place: {place_info[0]}, Reservation Date: {place_info[1]}")
    else:
        print("No reservations found for this user in the specified date range.")


def show_place_reservations_info():
    place_name = input("Enter the place name: ")

    db.cursor.execute("""
        SELECT u.first_name, u.last_name, r.place_name, r.reservation_date, p.place_price
        FROM reservation r
        JOIN user u ON r.national_code = u.national_code
        JOIN place p ON r.place_name = p.place_name
        WHERE r.place_name = %s
    """, (place_name,))

    reservations_info = db.cursor.fetchall()

    if reservations_info:
        print("\nReservations Information for the Specified Place:")
        total_cost_by_user = {}

        for row in reservations_info:
            first_name, last_name, place_name, reservation_date, place_price = row
            total_cost_by_user.setdefault((first_name, last_name), 0)
            total_cost_by_user[(first_name, last_name)] += place_price

        for user, total_cost in total_cost_by_user.items():
            print(f"User: {user[0]} {user[1]}, Total Cost: {total_cost}")
    else:
        print(f"No reservations found for the specified place: {place_name}")
