# ------- run this file ------- #

from functions import *

while True:
    select = input("""
1.add new user
2.add new place
3.add new reservation
4.edit user information
5.show user reservation
6.search by date
7.place details
\n""")

    if select == "1":
        add_new_user()
    elif select == "2":
        add_new_place()
    elif select == "3":
        add_reservation()
    elif select == "4":
        edit_user_information()
    elif select == "5":
        show_user_reservation_info()
    elif select == "6":
        show_user_reservations_in_date_range()
    elif select == "7":
        show_place_reservations_info()
