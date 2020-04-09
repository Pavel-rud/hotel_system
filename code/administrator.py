from PyQt5.QtWidgets import QApplication, QRadioButton,\
    QWidget, QFileDialog, QComboBox, QMessageBox, QButtonGroup, QCheckBox
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QListWidget
import sqlite3
from constants import *
import sys
from threading import Thread
import network
import json
import socket
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.Qt import QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from datetime import datetime
from make_and_read_documents import *

# todo: ещё не весь функционал готов, надо доделать


class UiAdministratorWindow(QWidget):
    def __init__(self, login):
        super().__init__()
        self.ip = "0.0.0.0:5555"
        self.sockIn = network.connect_InSocket(address='0.0.0.0', port=5556)
        self.sockOut = network.connect_OutSocket(address=self.ip.split(':')[0], port=int(self.ip.split(':')[1]))
        self.table_guests_size = 0
        self.initUI()
        self.init_functional_buttons()
        self.choosen_functional = ""
        self.hide_all_widgets()
        self.user = login
        self.hotel = self.send_to_server({"key": "get_hotel",
                                          "login": login})
        print(self.hotel)

    def info(self, inf, is_bad):
        self.info_label.setText(f"Инфо: {inf} ({str(datetime.now().strftime('%Y-%m-%d %H:%M').split()[1])})")
        self.info_label.resize(self.info_label.sizeHint())
        if is_bad:
            self.info_label.setStyleSheet('color: red')
        else:
            self.info_label.setStyleSheet('color: green')


    def send_to_server(self, msg):
        msg = json.dumps(msg)
        network.sock_send(self.sockOut, msg)
        try:
            self.sockIn.settimeout(2)
            data, address = network.read_sock(self.sockIn)
            self.sockIn.settimeout(None)
        except socket.timeout:
            self.info('Сервер отключен! Проверьте соединение', True)
            return "Error"
        msg = json.loads(data)
        return msg

    def disconnect_server(self):
        # network.sock_send(self.sockOut, json.dumps({"key": "login"}))
        network.alive = False
        network.close_sock(self.sockIn)
        network.close_sock(self.sockOut)

    def closeEvent(self, QCloseEvent):
        self.disconnect_server()

    def initUI(self):
        self.setGeometry(400, 400, 1200, 600)
        self.setWindowTitle('Система отеля (админ)')

        self.info_label = QLabel("Инфо:", self)
        self.info_label.move(150, 10)
        self.info_label.resize(self.info_label.sizeHint())
        self.info_label.setAutoFillBackground(True)
        p = self.info_label.palette()
        p.setColor(self.info_label.backgroundRole(), Qt.gray)
        self.info_label.setPalette(p)

        # Постояльцы

        self.tableWidget_guests = QTableWidget(self)
        self.tableWidget_guests.setColumnCount(12)
        self.tableWidget_guests.move(10, 360)
        self.tableWidget_guests.resize(950, 200)
        self.tableWidget_guests.setHorizontalHeaderItem(0, QTableWidgetItem(''))
        self.tableWidget_guests.setHorizontalHeaderItem(1, QTableWidgetItem('фамилия'))
        self.tableWidget_guests.setHorizontalHeaderItem(2, QTableWidgetItem('имя'))
        self.tableWidget_guests.setHorizontalHeaderItem(3, QTableWidgetItem('отчество'))
        self.tableWidget_guests.setHorizontalHeaderItem(4, QTableWidgetItem('дата_рождения'))
        self.tableWidget_guests.setHorizontalHeaderItem(5, QTableWidgetItem('пол'))
        self.tableWidget_guests.setHorizontalHeaderItem(6, QTableWidgetItem('номер_телефона'))
        self.tableWidget_guests.setHorizontalHeaderItem(7, QTableWidgetItem('паспортные_данные'))
        self.tableWidget_guests.setHorizontalHeaderItem(8, QTableWidgetItem('количестве_заселений_в_Гостиницы_этой_сети'))
        self.tableWidget_guests.setHorizontalHeaderItem(9, QTableWidgetItem('проживает_на_данный_момент'))
        self.tableWidget_guests.setHorizontalHeaderItem(10, QTableWidgetItem('гостиница'))
        self.tableWidget_guests.setHorizontalHeaderItem(11, QTableWidgetItem('номер'))

        self.suname_guest_label = QLabel("Фамилия:", self)
        self.suname_guest_label.move(10, 70)
        self.suname_guest_label.resize(self.suname_guest_label.sizeHint())

        self.suname_guest_linde_edit = QLineEdit(self)
        self.suname_guest_linde_edit.move(175, 70)
        self.suname_guest_linde_edit.resize(200, 20)

        self.name_guest_label = QLabel("Имя:", self)
        self.name_guest_label.move(10, 100)
        self.name_guest_label.resize(self.name_guest_label.sizeHint())

        self.name_guest_linde_edit = QLineEdit(self)
        self.name_guest_linde_edit.move(175, 100)
        self.name_guest_linde_edit.resize(200, 20)

        self.name_guest_linde_edit2 = QLineEdit(self)
        self.name_guest_linde_edit2.move(395, 100)
        self.name_guest_linde_edit2.resize(200, 20)

        self.otchestvo_guest_label = QLabel("Отчество:", self)
        self.otchestvo_guest_label.move(10, 130)
        self.otchestvo_guest_label.resize(self.otchestvo_guest_label.sizeHint())

        self.otchestvo_guest_linde_edit = QLineEdit(self)
        self.otchestvo_guest_linde_edit.move(175, 130)
        self.otchestvo_guest_linde_edit.resize(200, 20)

        self.otchestvo_guest_linde_edit2 = QLineEdit(self)
        self.otchestvo_guest_linde_edit2.move(395, 130)
        self.otchestvo_guest_linde_edit2.resize(200, 20)

        self.date_of_birthday_of_guest_label = QLabel("Дата рождения:", self)
        self.date_of_birthday_of_guest_label.move(10, 160)
        self.date_of_birthday_of_guest_label.resize(self.date_of_birthday_of_guest_label.sizeHint())

        self.date_of_birthday_of_guest_linde_edit = QLineEdit(self)
        self.date_of_birthday_of_guest_linde_edit.move(175, 160)
        self.date_of_birthday_of_guest_linde_edit.resize(200, 20)

        self.date_of_birthday_guest_linde_edit2 = QLineEdit(self)
        self.date_of_birthday_guest_linde_edit2.move(395, 160)
        self.date_of_birthday_guest_linde_edit2.resize(200, 20)

        self.gender_guest_label = QLabel("Пол:", self)
        self.gender_guest_label.move(10, 190)
        self.gender_guest_label.resize(self.gender_guest_label.sizeHint())

        self.gender_guest_linde_edit = QLineEdit(self)
        self.gender_guest_linde_edit.move(175, 190)
        self.gender_guest_linde_edit.resize(200, 20)

        self.gender_guest_linde_edit2 = QLineEdit(self)
        self.gender_guest_linde_edit2.move(395, 190)
        self.gender_guest_linde_edit2.resize(200, 20)

        self.number_of_prhone_guest_label = QLabel("Номер телефона:", self)
        self.number_of_prhone_guest_label.move(10, 220)
        self.number_of_prhone_guest_label.resize(self.number_of_prhone_guest_label.sizeHint())

        self.number_of_prhone_guest_linde_edit = QLineEdit(self)
        self.number_of_prhone_guest_linde_edit.move(175, 220)
        self.number_of_prhone_guest_linde_edit.resize(200, 20)

        self.number_of_prhone_guest_linde_edit2 = QLineEdit(self)
        self.number_of_prhone_guest_linde_edit2.move(395, 220)
        self.number_of_prhone_guest_linde_edit2.resize(200, 20)

        self.seria_of_passport_guest_label = QLabel("Паспортные данные:", self)
        self.seria_of_passport_guest_label.move(10, 250)
        self.seria_of_passport_guest_label.resize(self.seria_of_passport_guest_label.sizeHint())

        self.seria_of_passport_guest_linde_edit = QLineEdit(self)
        self.seria_of_passport_guest_linde_edit.move(175, 250)
        self.seria_of_passport_guest_linde_edit.resize(200, 20)

        self.seria_of_passport_guest_linde_edit2 = QLineEdit(self)
        self.seria_of_passport_guest_linde_edit2.move(395, 250)
        self.seria_of_passport_guest_linde_edit2.resize(200, 20)

        self.guest_list = QComboBox(self)
        self.guest_list.move(390, 65)
        self.guest_list.resize(200, 30)
        self.guest_list.currentTextChanged.connect(self.updateguests)
        # self.guest_list.addItems()

        self.guest_list2 = QComboBox(self)
        self.guest_list2.move(600, 65)
        self.guest_list2.resize(200, 30)
        # self.guest_list2.addItems()

        self.add_guest = QPushButton("Зарегистрировать\nпостояльца", self)
        self.add_guest.move(175, 280)
        self.add_guest.resize(200, 50)
        self.add_guest.pressed.connect(self.addguest)

        self.delete_guest = QPushButton("Удалить постояльца", self)
        self.delete_guest.move(600, 90)
        self.delete_guest.resize(200, 30)
        self.delete_guest.pressed.connect(self.deleteguest)

        self.creat_csv_for_many_guest = QPushButton("Экспортировать данные\n о постояльцах в csv", self)
        self.creat_csv_for_many_guest.move(980, 360)
        self.creat_csv_for_many_guest.resize(200, 50)
        self.creat_csv_for_many_guest.pressed.connect(self.csv_guests)

        self.remake_guest = QPushButton("Обновить информацию\nо постояльце", self)
        self.remake_guest.move(395, 280)
        self.remake_guest.resize(200, 50)
        self.remake_guest.pressed.connect(self.remakeguest)

        # Номера Гостиницы

        self.number_hotel_label = QLabel("Номер комнаты в общежитии:", self)
        self.number_hotel_label.move(10, 70)
        self.number_hotel_label.resize(self.number_hotel_label.sizeHint())

        self.number_hotel_linde_edit = QLineEdit(self)
        self.number_hotel_linde_edit.move(205, 70)
        self.number_hotel_linde_edit.resize(200, 20)

        self.rooms_hotel_label = QLabel("Количество комнат:", self)
        self.rooms_hotel_label.move(10, 100)
        self.rooms_hotel_label.resize(self.rooms_hotel_label.sizeHint())

        self.rooms_hotel_linde_edit = QLineEdit(self)
        self.rooms_hotel_linde_edit.move(205, 100)
        self.rooms_hotel_linde_edit.resize(200, 20)

        self.rooms_hotel_linde_edit2 = QLineEdit(self)
        self.rooms_hotel_linde_edit2.move(425, 100)
        self.rooms_hotel_linde_edit2.resize(200, 20)

        self.s_of_rooms_label = QLabel("Площадь номера:", self)
        self.s_of_rooms_label.move(10, 130)
        self.s_of_rooms_label.resize(self.s_of_rooms_label.sizeHint())

        self.s_of_rooms_linde_edit = QLineEdit(self)
        self.s_of_rooms_linde_edit.move(205, 130)
        self.s_of_rooms_linde_edit.resize(200, 20)
             
        self.s_of_rooms_linde_edit2 = QLineEdit(self)
        self.s_of_rooms_linde_edit2.move(425, 130)
        self.s_of_rooms_linde_edit2.resize(200, 20)

        self.hotel_room_list = QComboBox(self)
        self.hotel_room_list.move(420, 65)
        self.hotel_room_list.resize(200, 30)
        self.hotel_room_list.currentTextChanged.connect(self.update_rooms)
        # self.guest_list.addItems()

        self.hotel_room2 = QComboBox(self)
        self.hotel_room2.move(630, 65)
        self.hotel_room2.resize(200, 30)
        # self.guest_list2.addItems()

        self.add_room = QPushButton("Зарегистрировать\nномер", self)
        self.add_room.move(205, 150)
        self.add_room.resize(200, 50)
        self.add_room.pressed.connect(self.addroom)

        self.delete_room = QPushButton("Удалить номер", self)
        self.delete_room.move(630, 90)
        self.delete_room.resize(200, 30)
        self.delete_room.pressed.connect(self.deleteroom)

        self.remake_room = QPushButton("Обновить информацию\nо номере", self)
        self.remake_room.move(425, 150)
        self.remake_room.resize(200, 50)
        self.remake_room.pressed.connect(self.change_info_about_room)

        self.tableWidget_room = QTableWidget(self)
        self.tableWidget_room.setColumnCount(4)
        self.tableWidget_room.move(10, 230)
        self.tableWidget_room.resize(800, 200)
        self.tableWidget_room.setHorizontalHeaderItem(0, QTableWidgetItem('гостиница'))
        self.tableWidget_room.setHorizontalHeaderItem(1, QTableWidgetItem('номер комнаты'))
        self.tableWidget_room.setHorizontalHeaderItem(2, QTableWidgetItem('количество комнат'))
        self.tableWidget_room.setHorizontalHeaderItem(3, QTableWidgetItem('площадь номера'))
        # Заселение

        self.room_zaselenie_lbl = QLabel("Номер:", self)
        self.room_zaselenie_lbl.move(510, 70)
        self.room_zaselenie_lbl.resize(self.room_zaselenie_lbl.sizeHint())

        self.room_zaselenie = QComboBox(self)
        self.room_zaselenie.move(580, 65)
        self.room_zaselenie.resize(200, 30)

        self.guest1 = QLabel("Постоялец:", self)
        self.guest1.move(10, 70)
        self.guest1.resize(self.guest1.sizeHint())

        self.guest_list_zaselenie = QComboBox(self)
        self.guest_list_zaselenie.move(90, 65)
        self.guest_list_zaselenie.resize(400, 30)
        # self.guest_list_zaselenie.addItems()


        self.guest_zaselenie = QPushButton("Заселить постояльца\nи распечатать документ", self)
        self.guest_zaselenie.move(90, 100)
        self.guest_zaselenie.resize(200, 50)
        self.guest_zaselenie.pressed.connect(self.zaselenie)

        # Выселение

        self.guest2 = QLabel("Постоялец:", self)
        self.guest2.move(10, 70)
        self.guest2.resize(self.guest2.sizeHint())

        self.guest_list_vysylenie = QComboBox(self)
        self.guest_list_vysylenie.move(90, 65)
        self.guest_list_vysylenie.resize(400, 30)
        # self.guest_list_vysylenie.addItems()

        self.guest_vysylenie = QPushButton("Выселить постояльца\nи распечатать документ", self)
        self.guest_vysylenie.move(90, 100)
        self.guest_vysylenie.resize(200, 50)
        self.guest_vysylenie.pressed.connect(self.vysilenie)

    def init_functional_buttons(self):
        self.label_functional = QLabel("Функционал:", self)
        self.label_functional.move(10, 10)
        self.label_functional.resize(self.label_functional.sizeHint())

        self.radio_button_1 = QRadioButton("Постояльцы", self)
        self.radio_button_1.move(10, 30)

        self.radio_button_2 = QRadioButton("Номера Гостиницы", self)
        self.radio_button_2.move(120, 30)

        self.radio_button_3 = QRadioButton("Заселение", self)
        self.radio_button_3.move(275, 30)

        self.radio_button_4 = QRadioButton("Выселение", self)
        self.radio_button_4.move(375, 30)


        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_1)
        self.button_group.addButton(self.radio_button_2)
        self.button_group.addButton(self.radio_button_3)
        self.button_group.addButton(self.radio_button_4)
        self.button_group.buttonClicked.connect(self.choose)

    def choose(self, button):
        self.choosen_functional = button.text()
        self.hide_all_widgets()
        if self.choosen_functional == "Постояльцы":
            self.show_postoyalcy_functional()
        elif self.choosen_functional == "Номера Гостиницы":
            self.show_rooms_of_hotel_functional()
        elif self.choosen_functional == "Заселение":
            self.show_zaselenie_functional()
        elif self.choosen_functional == "Выселение":
            self.show_vysilenie_functional()

    def show_postoyalcy_functional(self):
        answer = self.send_to_server({"key": "guests"})
        if answer != "Error":
            self.guests = answer
            admin = self.send_to_server({"key": "get_info_about_one_admin",
                                         "login": self.user})
            guests = []
            for i in self.guests:
                guests.append(i)

            self.tableWidget_guests.show()
            self.tableWidget_guests.setRowCount(len(guests))
            self.table_guests_size = len(guests)
            for i in range(len(guests)):
                for j in range(12):
                    if j != 0:
                        itm = QTableWidgetItem(str(guests[i][j - 1]))
                        itm.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.tableWidget_guests.setItem(i, j, itm)
                    else:
                        self.tableWidget_guests.setCellWidget(i, j, QCheckBox())

            self.tableWidget_guests.resizeColumnsToContents()

        guests = []
        for i in self.guests:
            guests.append(" ".join([str(j) for j in i][:7]))

        self.guest_list.clear()
        self.guest_list.addItems(guests)
        self.guest_list2.clear()
        self.guest_list2.addItems(guests)

        guest_choosen = self.guest_list.currentText()

        self.tableWidget_guests.show()
        self.suname_guest_label.show()
        self.suname_guest_linde_edit.show()
        self.name_guest_label.show()
        self.name_guest_linde_edit.show()
        self.name_guest_linde_edit2.show()
        self.otchestvo_guest_label.show()
        self.otchestvo_guest_linde_edit.show()
        self.otchestvo_guest_linde_edit2.show()
        self.date_of_birthday_of_guest_label.show()
        self.date_of_birthday_of_guest_linde_edit.show()
        self.date_of_birthday_guest_linde_edit2.show()
        self.gender_guest_label.show()
        self.gender_guest_linde_edit.show()
        self.gender_guest_linde_edit2.show()
        self.number_of_prhone_guest_label.show()
        self.number_of_prhone_guest_linde_edit.show()
        self.number_of_prhone_guest_linde_edit2.show()
        self.seria_of_passport_guest_label.show()
        self.seria_of_passport_guest_linde_edit.show()
        self.seria_of_passport_guest_linde_edit2.show()
        self.guest_list.show()
        self.guest_list2.show()
        self.add_guest.show()
        self.delete_guest.show()
        self.remake_guest.show()
        self.tableWidget_guests.show()
        self.creat_csv_for_many_guest.show()
        try:
            self.name_guest_linde_edit2.setText(guest_choosen.split()[1])
            self.number_of_prhone_guest_linde_edit2.setText(guest_choosen.split()[5])
            self.gender_guest_linde_edit2.setText(guest_choosen.split()[4])
            self.date_of_birthday_guest_linde_edit2.setText(guest_choosen.split()[3])
            self.otchestvo_guest_linde_edit2.setText(guest_choosen.split()[2])
            self.seria_of_passport_guest_linde_edit2.setText(guest_choosen.split()[6])
        except:
            pass

    def deleteroom(self):
        number = self.hotel_room2.currentText()
        hotel = list(self.send_to_server({"key": "get_info_about_one_admin",
                                     "login": self.user}))[6]
        guests = self.send_to_server({"key": "guests"})
        try:
            for i in guests:
                if i[9] == hotel and i[10] == number and i[8] == "true":
                    self.info("Номер не был удален, так как он занят", True)
                    return

            ok = self.send_to_server({"key": "delete_room",
                                      "hotel": hotel,
                                      "number": number})
            if ok:
                self.info("Номер успешно удален", False)
            else:
                self.info("Номер не был удален", True)
        except:
            self.info("Номер не был удален", True)
        self.show_rooms_of_hotel_functional()

    def addroom(self):
        hotel = list(self.send_to_server({"key": "get_info_about_one_admin",
                                          "login": self.user}))[6]
        number = self.number_hotel_linde_edit.text()
        kol_rooms = self.rooms_hotel_linde_edit.text()
        s = self.s_of_rooms_linde_edit.text()
        if  hotel and number and kol_rooms and s:
            ok = self.send_to_server({"key": "add_room",
                                      "hotel": hotel,
                                      "number": number,
                                      "rooms": kol_rooms,
                                      "s": s})
            if ok:
                self.info("Номер успешно добавлен", False)
            else:
                self.info("Номер не был добавлен", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_rooms_of_hotel_functional()


    def change_info_about_room(self):
        hotel = list(self.send_to_server({"key": "get_info_about_one_admin",
                                          "login": self.user}))[6]
        number = self.hotel_room_list.currentText()
        kol_rooms = self.rooms_hotel_linde_edit2.text()
        s = self.s_of_rooms_linde_edit2.text()
        if hotel and number and kol_rooms and s:
            ok = self.send_to_server({"key": "change_info_about_room",
                                      "hotel": hotel,
                                      "number": number,
                                      "rooms": kol_rooms,
                                      "s": s})
            if ok:
                self.info("Информация о номере изменена", False)
            else:
                self.info("Информация о номере не изменена", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_rooms_of_hotel_functional()

    def show_rooms_of_hotel_functional(self):
        answer = self.send_to_server({"key": 'rooms'})
        if answer != "Error":
            rooms_ = answer
            admin = self.send_to_server({"key": "get_info_about_one_admin",
                                         "login": self.user})
            self.rooms = []
            for i in rooms_:
                if admin[6] == i[0]:
                    self.rooms.append(i)
            self.tableWidget_room.show()
            self.tableWidget_room.setRowCount(len(self.rooms))
            print(self.rooms)
            for i in range(len(self.rooms)):
                for j in range(4):
                    itm = QTableWidgetItem(str(self.rooms[i][j]))
                    itm.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_room.setItem(i, j, itm)
            self.tableWidget_room.resizeColumnsToContents()
        print(self.rooms)
        self.hotel_room_list.clear()
        self.hotel_room_list.addItems([str(i[1]) for i in self.rooms])
        self.hotel_room2.clear()
        self.hotel_room2.addItems([str(i[1]) for i in self.rooms])
        room = "No"
        for i in self.rooms:
            if str(i[1]) == str(self.hotel_room_list.currentText()):
                room = i
        else:
            if room == "No":
                room = ['' for i in range(5)]
        room = [i if i else '' for i in room]

        self.number_hotel_label.show()
        self.number_hotel_linde_edit.show()
        self.rooms_hotel_label.show()
        self.rooms_hotel_linde_edit.show()
        self.rooms_hotel_linde_edit2.show()
        self.s_of_rooms_label.show()
        self.s_of_rooms_linde_edit.show()
        self.s_of_rooms_linde_edit2.show()
        self.hotel_room_list.show()
        self.hotel_room2.show()
        self.add_room.show()
        self.delete_room.show()
        self.remake_room.show()
        try:
            self.s_of_rooms_linde_edit2.setText(str(room[3]))
            self.rooms_hotel_linde_edit2.setText(str(room[2]))
        except:
            pass

    def show_zaselenie_functional(self):
        answer = self.send_to_server({"key": "guests"})
        if answer != "Error":
            self.guests = answer
        answer = self.send_to_server({"key": "rooms"})
        if answer != "Error":
            self.room = answer

        guests = []
        for i in self.guests:
            if i[8] != "true":
                guests.append(" ".join([str(j) for j in i][:7]))
        rooms = []
        admin = self.send_to_server({"key": "get_info_about_one_admin",
                                     "login": self.user})
        print(self.room)
        for i in self.room:
            if admin[6] == i[0]:
                rooms.append(i[1])

        self.room_zaselenie.clear()
        self.room_zaselenie.addItems(rooms)
        self.guest_list_zaselenie.clear()
        self.guest_list_zaselenie.addItems(guests)
        self.guest1.show()
        self.guest_list_zaselenie.show()
        self.guest_zaselenie.show()
        self.room_zaselenie_lbl.show()
        self.room_zaselenie.show()

    def zaselenie(self):
        try:
            admin = self.send_to_server({"key": "get_info_about_one_admin",
                                         "login": self.user})
            if list(str(self.guest_list_zaselenie.currentText())):
                passport = list(str(self.guest_list_zaselenie.currentText()).split())[6]
            ok = self.send_to_server({"key": "check_in_hotel_guest",
                                        "passport": passport,
                                        "hotel": admin[6],
                                        "room": self.room_zaselenie.currentText()})
            print(ok)
            if ok[0]:
                location = QFileDialog.getSaveFileName(self, 'Save file', '')[0]
                guest = ok[1]
                try:
                    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[0])
                    admin_and_guest(guest[0], guest[1], guest[2], guest[9], guest[10], admin[2], admin[3], admin[4], date, "Заселение", location)
                    self.info("Постоялец заселён", False)
                except:
                    self.info("Постоялец заселён, но при формировании документа произошла ошибка", True)
            else:
                self.info("Постоялец не был заселён", True)
            self.show_zaselenie_functional()
        except:
            print("error")
            self.show_zaselenie_functional()

    def vysilenie(self):
        try:
            if list(str(self.guest_list_vysylenie.currentText()).split()):
                passport = list(str(self.guest_list_vysylenie.currentText()).split())[6]
            ok = self.send_to_server({"key": "mowe_out_guest",
                                         "passport": passport})
            if ok[0]:
                location = QFileDialog.getSaveFileName(self, 'Save file', '')[0]
                guest = ok[1]
                admin = self.send_to_server({"key": "get_info_about_one_admin",
                                             "login": self.user})
                try:
                    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[0])
                    admin_and_guest(guest[0], guest[1], guest[2], guest[9], guest[10], admin[2], admin[3], admin[4], date, "Выселение", location)
                    self.info("Постоялец выселен", False)
                except:
                    self.info("Постоялец выселен, но при формировании документа произошла ошибка", True)
            else:
                self.info("Постоялец не был выселен", True)
            self.show_vysilenie_functional()
        except:
            self.show_vysilenie_functional()

    def show_vysilenie_functional(self):
        answer = self.send_to_server({"key": "guests"})
        print(answer)
        if answer != "Error":
            self.guests = []
            for i in answer:
                if i[9] == self.hotel:
                    self.guests.append(i)

        guests = []
        for i in self.guests:
            print(i)
            guests.append(" ".join([str(j) for j in i][:7]))

        self.guest_list_vysylenie.clear()
        self.guest_list_vysylenie.addItems(guests)
        self.guest2.show()
        self.guest_list_vysylenie.show()
        self.guest_vysylenie.show()

    def hide_all_widgets(self):
        self.suname_guest_label.hide()
        self.suname_guest_linde_edit.hide()
        self.name_guest_label.hide()
        self.name_guest_linde_edit.hide()
        self.name_guest_linde_edit2.hide()
        self.otchestvo_guest_label.hide()
        self.otchestvo_guest_linde_edit.hide()
        self.otchestvo_guest_linde_edit2.hide()
        self.date_of_birthday_of_guest_label.hide()
        self.date_of_birthday_of_guest_linde_edit.hide()
        self.date_of_birthday_guest_linde_edit2.hide()
        self.gender_guest_label.hide()
        self.gender_guest_linde_edit.hide()
        self.gender_guest_linde_edit2.hide()
        self.number_of_prhone_guest_label.hide()
        self.number_of_prhone_guest_linde_edit.hide()
        self.number_of_prhone_guest_linde_edit2.hide()
        self.seria_of_passport_guest_label.hide()
        self.seria_of_passport_guest_linde_edit.hide()
        self.seria_of_passport_guest_linde_edit2.hide()
        self.guest_list.hide()
        self.guest_list2.hide()
        self.add_guest.hide()
        self.delete_guest.hide()
        self.tableWidget_guests.hide()
        self.remake_guest.hide()
        self.creat_csv_for_many_guest.hide()

        self.number_hotel_label.hide()
        self.number_hotel_linde_edit.hide()
        self.rooms_hotel_label.hide()
        self.rooms_hotel_linde_edit.hide()
        self.rooms_hotel_linde_edit2.hide()
        self.s_of_rooms_label.hide()
        self.s_of_rooms_linde_edit.hide()
        self.s_of_rooms_linde_edit2.hide()
        self.hotel_room_list.hide()
        self.hotel_room2.hide()
        self.add_room.hide()
        self.delete_room.hide()
        self.remake_room.hide()
        self.tableWidget_room.hide()

        self.room_zaselenie_lbl.hide()
        self.room_zaselenie.hide()
        self.guest1.hide()
        self.guest_list_zaselenie.hide()
        self.guest_zaselenie.hide()

        self.guest2.hide()
        self.guest_list_vysylenie.hide()
        self.guest_vysylenie.hide()

    def update_rooms(self):
        answer = self.send_to_server({"key": 'rooms'})
        if answer != "Error":
            rooms_ = answer
            admin = self.send_to_server({"key": "get_info_about_one_admin",
                                         "login": self.user})
            self.rooms = []
            for i in rooms_:
                if admin[6] == i[0]:
                    self.rooms.append(i)
        print(self.rooms)
        room = "No"
        for i in self.rooms:
            if str(i[1]) == str(self.hotel_room_list.currentText()):
                room = i
        else:
            if room == "No":
                room = ['' for i in range(5)]
        room = [i if i else '' for i in room]
        self.rooms_hotel_linde_edit2.setText(str(room[2]))
        self.s_of_rooms_linde_edit2.setText(str(room[3]))

    def updateguests(self):
        guest_choosen = self.guest_list.currentText()
        try:
            self.name_guest_linde_edit2.setText(guest_choosen.split()[1])
            self.otchestvo_guest_linde_edit2.setText(guest_choosen.split()[2])
            self.date_of_birthday_guest_linde_edit2.setText(guest_choosen.split()[3])
            self.gender_guest_linde_edit2.setText(guest_choosen.split()[4])
            self.number_of_prhone_guest_linde_edit2.setText(guest_choosen.split()[5])
            self.seria_of_passport_guest_linde_edit2.setText(guest_choosen.split()[6])
        except:
            pass

    def deleteguest(self):
        guests = self.send_to_server({"key": "guests"})
        try:
            passport = self.guest_list2.currentText().split()[6]
            for i in guests:
                if i[6] == passport and i[8] == "true":
                    print(i, passport)
                    self.info("Постоялец не был удален, так как он проживает в отеле", True)
                    return

            ok = self.send_to_server({"key": "delete_guest",
                                      "passport": passport})
            if ok:
                self.info("Постоялец успешно удален", False)
            else:
                self.info("Постоялец не был удален", True)
        except:
            self.info("Постоялец не был удален", True)
        self.show_postoyalcy_functional()

    def addguest(self):
        suname = self.suname_guest_linde_edit.text()
        name = self.name_guest_linde_edit.text()
        otchestvo = self.otchestvo_guest_linde_edit.text()
        data = self.date_of_birthday_of_guest_linde_edit.text()
        gender = self.gender_guest_linde_edit.text()
        number_phone = self.number_of_prhone_guest_linde_edit.text()
        passport = self.seria_of_passport_guest_linde_edit.text()
        if suname and name and otchestvo and data and gender and number_phone and passport:
            ok = self.send_to_server({"key": "add_guest",
                                      "suname": suname,
                                      "name": name,
                                      "otchestvo": otchestvo,
                                      "data": data,
                                      "gender": gender,
                                      "number_phone": number_phone,
                                      "passport": passport})
            if ok:
                self.info("Постоялец успешно добавлен", False)
            else:
                self.info("Постоялец не был добавлен", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_postoyalcy_functional()


    def remakeguest(self):
        name = self.name_guest_linde_edit2.text()
        otchestvo = self.otchestvo_guest_linde_edit2.text()
        data = self.date_of_birthday_guest_linde_edit2.text()
        gender = self.gender_guest_linde_edit2.text()
        number_phone = self.number_of_prhone_guest_linde_edit2.text()
        passport = self.seria_of_passport_guest_linde_edit2.text()
        if name and otchestvo and data and gender and number_phone and passport:
            try:
                passportnow = self.guest_list.currentText().split()[6]
            except:
                passportnow = ""
            ok = self.send_to_server({"key": "change_info_about_guest",
                                      "name": name,
                                      "otchestvo": otchestvo,
                                      "data": data,
                                      "gender": gender,
                                      "number_phone": number_phone,
                                      "passport": passport,
                                      "passportnow": passportnow})
            if ok:
                self.info("Информация о постояльце успешно обновлена", False)
            else:
                self.info("Информация о постояльце не обновлена", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_postoyalcy_functional()

    def csv_guests(self):
        location = QFileDialog.getSaveFileName(self, 'Save file', '')[0]
        #print(guests, location)
        guests = []
        for i in range(self.table_guests_size):
            if self.tableWidget_guests.cellWidget(i, 0).checkState():
                guests.append([self.tableWidget_guests.item(i, j).text() for j in range(1, 9)])
        print(guests, location)
        try:
            if location:
                info_about_guests(guests, location)
                self.info("Документ сохранён", False)
            else:
                self.info("Укажите путь сохранения", True)
        except:
            self.info("При формировании документа произошла ошибка", True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UiAdministratorWindow()
    MainWindow.show()
    sys.exit(app.exec())
