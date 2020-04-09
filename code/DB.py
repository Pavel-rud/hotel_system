import sqlite3
import sys
from constants import *

# download info

def get_info_about_one_admin(login):
    con = sqlite3.connect(bd)
    cur = con.cursor()
    admin = cur.execute(f"""SELECT * from administrators where логин = '{login}'""").fetchall()
    con.commit()
    con.close()
    return admin[0]

def get_hotel(login):
    con = sqlite3.connect(bd)
    cur = con.cursor()
    hotel = cur.execute(f"""SELECT * from administrators where логин = '{login}'""").fetchall()
    con.commit()
    con.close()
    print(hotel)
    return hotel[0][6]

def rooms_download():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    rooms = cur.execute("""SELECT * FROM rooms""").fetchall()
    con.close()
    return rooms

def admin_download():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    admins = cur.execute("""SELECT * FROM administrators""").fetchall()
    login_admins = [i[0] for i in admins]
    not_banned_admin = [i[0] for i in admins if i[7] != "true"]
    con.close()
    return [login_admins, admins, not_banned_admin]

def hotels_download():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    hotels = cur.execute("""SELECT * FROM hotels""").fetchall()
    name_hotels = [i[0] for i in hotels]
    con.close()
    return [name_hotels, hotels]

def download_guests():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    guests = cur.execute("""SELECT * FROM guests""").fetchall()
    con.close()
    return guests

def bad_try_download():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    bad_try = cur.execute("""SELECT * FROM bad_try_login""").fetchall()
    con.close()
    return bad_try

# for login in system
def bd_for_login():
    con = sqlite3.connect(bd)
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM administrators""").fetchall()
    login_password_admin = {}
    banned_admin = {}
    for elem in result:
        login_password_admin[elem[0]] = elem[1]
        if elem[7] == "true":
            banned_admin[elem[0]] = elem[8]
    login_password_manager = {}
    result = cur.execute("""SELECT * FROM manager""").fetchall()
    for elem in result:
        login_password_manager[elem[0]] = elem[1]
    con.close()
    return [login_password_admin, login_password_manager, banned_admin]


# add/change/delete guests
def add_guest(guest):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO guests VALUES('{guest[0]}', '{guest[1]}', '{guest[2]}', '{guest[3]}', '{guest[4]}', '{guest[5]}', '{guest[6]}', '{0}', 'false', '', '')""")
        con.commit()
        con.close()
        return True
    except:
        return False


def delete_guest(passport):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""DELETE from guests where паспортные_данные = '{passport}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def change_info_about_guest(guest):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(
            f"""UPDATE guests SET имя = '{guest[1]}', отчество = '{guest[2]}', дата_рождения = '{guest[3]}',
             пол = '{guest[4]}', номер_телефона = '{guest[5]}', паспортные_данные = '{guest[6]}' WHERE паспортные_данные = '{guest[-1]}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def check_in_hotel_guest(passport, hotel, room):  #заселние
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        kol = cur.execute(
            f"""SELECT * FROM guests WHERE паспортные_данные = '{passport}'""").fetchall()
        print(int(kol[0][7]))
        print(passport, hotel, room)
        cur.execute(
            f"""UPDATE guests SET количестве_заселений_в_Гостиницы_этой_сети = '{int(
                kol[0][7]) + 1}', проживает_на_данный_момент = 'true',
                                                 гостиница = '{hotel}', номер = '{room}' WHERE паспортные_данные = '{passport}'""")
        guest = cur.execute(f"""SELECT * from guests where паспортные_данные = '{passport}'""").fetchall()
        con.commit()
        con.close()
        return [True, guest[0]]
    except:
        return [False, []]


def mowe_out_guest(passport):  #выселение
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        guest = cur.execute(f"""SELECT * from guests where паспортные_данные = '{passport}'""").fetchall()
        cur.execute(
            f"""UPDATE guests SET проживает_на_данный_момент = 'false',
                                     гостиница = '', номер = '' WHERE паспортные_данные = '{passport}'""")
        con.commit()
        con.close()
        return [True, guest[0]]
    except:
        return [False, []]

# # add/delete/change hotel

def change_info_about_hotel(hotel):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(
            f"""UPDATE hotels SET количество_этажей = '{hotel[1]}', количество_номеров = '{hotel[2]}', страна = '{hotel[3]}', город = '{hotel[4]}',
             улица = '{hotel[5]}', дом = '{hotel[6]}' WHERE название_гостиницы = '{hotel[0]}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def add_hotel(hotel):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO hotels VALUES('{hotel[0]}', '{hotel[1]}', '{hotel[2]}', '{hotel[3]}', '{hotel[4]}', '{hotel[5]}', '{hotel[6]}')""")
        con.commit()
        con.close()
        return True
    except:
        return False

def delete_hotel(name):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""DELETE from hotels where название_гостиницы = '{name}'""")
        con.commit()
        con.close()
        return True
    except:
        return False

# add/delete/change/bann admin
def change_info_about_admin(admin):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(
            f"""UPDATE administrators SET пароль = '{admin[1]}', фамилия = '{admin[2]}', имя = '{admin[3]}', отчество = '{admin[4]}',
             номер_телефона = '{admin[5]}', гостиница = '{admin[6]}' WHERE логин = '{admin[0]}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def add_admin(admin):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO administrators VALUES('{admin[0]}', '{admin[1]}', '{admin[2]}', '{admin[3]}', '{admin[4]}', '{admin[5]}', '{admin[6]}', '', '')""")
        con.commit()
        con.close()
        return True
    except:
        return False


def delete_admin(login):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""DELETE from administrators where логин = '{login}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def bann_admin(login, reason):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(
            f"""UPDATE administrators SET заблокирован = 'true', причина_блокировки = '{reason}' WHERE логин = '{login}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


# неудачные попытки входа
def add_bad_try_login(login, password, time):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO bad_try_login(логин, пароль, время) VALUES('{login}', '{password}', '{time}')""")
        con.commit()
        con.close()
        return True
    except:
        return False

# add/delete/change rooms
def change_info_about_room(hotel, number, kol, s):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(
            f"""UPDATE rooms SET количество_комнат = '{kol}', площадь_номера = '{s}'
             where гостиница = '{hotel}' AND номер_комнаты = '{number}'""")
        con.commit()
        con.close()
        return True
    except:
        return False


def add_room(room):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO rooms VALUES('{room[0]}', '{room[1]}', '{room[2]}', '{room[3]}')""")
        con.commit()
        con.close()
        return True
    except:
        return False

def delete_room(hotel, number):
    try:
        con = sqlite3.connect(bd)
        cur = con.cursor()
        cur.execute(f"""DELETE from rooms where гостиница = '{hotel}' AND номер_комнаты = '{number}'""")
        con.commit()
        con.close()
        return True
    except:
        return False

#delete_admin("ododfsd")
#bann_admin("Admin", "lol")
#change_info_about_admin(["Admin", "Admin", "b", "asda", "b,", "ssd", "dsad", "d", ""])
#add_bad_try_login("lol", "1234", "10:44")