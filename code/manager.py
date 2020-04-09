from PyQt5.QtWidgets import QApplication, QRadioButton,\
    QWidget, QFileDialog, QComboBox, QMessageBox, QButtonGroup, QListWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.Qt import QPalette
from PyQt5.QtCore import Qt
import sqlite3
from constants import *
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from make_and_read_documents import *
from datetime import datetime
from threading import Thread
import network
import json
import socket
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class UiManagerWindow(QWidget):
    def __init__(self, login):
        super().__init__()
        self.user = login
        self.admin = False
        self.ok = 0
        self.ip = "0.0.0.0:5555"
        self.sockIn = network.connect_InSocket(address='0.0.0.0', port=5556)
        self.sockOut = network.connect_OutSocket(address=self.ip.split(':')[0], port=int(self.ip.split(':')[1]))
        self.choosen_functional = ""
        self.login_admins, self.admins, self.banned_admin = [[], [], []]
        self.init_functional_buttons()
        self.initUI()
        self.hide_all_widgets()
        self.check_filter_country_on = False
        self.check_filter_city_on = False

    def check_filter_country_change(self):
        if self.check_filter_country_on:
            self.check_filter_country_on = False
        else:
            self.check_filter_country_on = True
        self.show_hotel_funtional()

    def check_filter_city_change(self):
        if self.check_filter_city_on:
            self.check_filter_city_on = False
        else:
            self.check_filter_city_on = True
        self.show_hotel_funtional()

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

    def info(self, inf, is_bad):
        self.info_label.setText(f"Инфо: {inf} ({str(datetime.now().strftime('%Y-%m-%d %H:%M').split()[1])})")
        self.info_label.resize(self.info_label.sizeHint())
        if is_bad:
            self.info_label.setStyleSheet('color: red')
        else:
            self.info_label.setStyleSheet('color: green')

    def initUI(self):
        self.setGeometry(400, 400, 900, 600)
        self.setWindowTitle('Система отеля (управляющий)')

        self.info_label = QLabel("Инфо:", self)
        self.info_label.move(150, 10)
        self.info_label.resize(self.info_label.sizeHint())
        self.info_label.setAutoFillBackground(True)
        p = self.info_label.palette()
        p.setColor(self.info_label.backgroundRole(), Qt.gray)
        self.info_label.setPalette(p)

        # Управление администраторами гостиницы

        self.login_of_admin_label = QLabel("Логин:", self)
        self.login_of_admin_label.move(10, 70)
        self.login_of_admin_label.resize(self.login_of_admin_label.sizeHint())

        self.login_of_admin_linde_edit = QLineEdit(self)
        self.login_of_admin_linde_edit.move(175, 70)
        self.login_of_admin_linde_edit.resize(200, 20)

        self.password_admin_label = QLabel("Пароль:", self)
        self.password_admin_label.move(10, 100)
        self.password_admin_label.resize(self.password_admin_label.sizeHint())

        self.password_admin_linde_edit = QLineEdit(self)
        self.password_admin_linde_edit.move(175, 100)
        self.password_admin_linde_edit.resize(200, 20)

        self.password_admin_linde_edit2 = QLineEdit(self)
        self.password_admin_linde_edit2.move(395, 100)
        self.password_admin_linde_edit2.resize(200, 20)

        self.suname_admin_label = QLabel("Фамилия:", self)
        self.suname_admin_label.move(10, 130)
        self.suname_admin_label.resize(self.suname_admin_label.sizeHint())

        self.suname_admin_linde_edit = QLineEdit(self)
        self.suname_admin_linde_edit.move(175, 130)
        self.suname_admin_linde_edit.resize(200, 20)

        self.suname_admin_linde_edit2 = QLineEdit(self)
        self.suname_admin_linde_edit2.move(395, 130)
        self.suname_admin_linde_edit2.resize(200, 20)

        self.name_admin_label = QLabel("Имя:", self)
        self.name_admin_label.move(10, 160)
        self.name_admin_label.resize(self.name_admin_label.sizeHint())

        self.name_admin_linde_edit = QLineEdit(self)
        self.name_admin_linde_edit.move(175, 160)
        self.name_admin_linde_edit.resize(200, 20)

        self.name_admin_linde_edit2 = QLineEdit(self)
        self.name_admin_linde_edit2.move(395, 160)
        self.name_admin_linde_edit2.resize(200, 20)

        self.otchestvo_admin_label = QLabel("Отчество:", self)
        self.otchestvo_admin_label.move(10, 190)
        self.otchestvo_admin_label.resize(self.otchestvo_admin_label.sizeHint())

        self.otchestvo_admin_linde_edit = QLineEdit(self)
        self.otchestvo_admin_linde_edit.move(175, 190)
        self.otchestvo_admin_linde_edit.resize(200, 20)

        self.otchestvo_admin_linde_edit2 = QLineEdit(self)
        self.otchestvo_admin_linde_edit2.move(395, 190)
        self.otchestvo_admin_linde_edit2.resize(200, 20)

        self.number_of_prhone_admin_label = QLabel("Номер телефона:", self)
        self.number_of_prhone_admin_label.move(10, 220)
        self.number_of_prhone_admin_label.resize(self.number_of_prhone_admin_label.sizeHint())

        self.number_of_prhone_admin_linde_edit = QLineEdit(self)
        self.number_of_prhone_admin_linde_edit.move(175, 220)
        self.number_of_prhone_admin_linde_edit.resize(200, 20)

        self.number_of_prhone_admin_linde_edit2 = QLineEdit(self)
        self.number_of_prhone_admin_linde_edit2.move(395, 220)
        self.number_of_prhone_admin_linde_edit2.resize(200, 20)

        self.hotel_admin_label = QLabel("Гостиница:", self)
        self.hotel_admin_label.move(10, 250)
        self.hotel_admin_label.resize(self.hotel_admin_label.sizeHint())

        self.hotel_admin_linde_edit = QLineEdit(self)
        self.hotel_admin_linde_edit.move(175, 250)
        self.hotel_admin_linde_edit.resize(200, 20)

        self.hotel_admin_linde_edit2 = QLineEdit(self)
        self.hotel_admin_linde_edit2.move(395, 250)
        self.hotel_admin_linde_edit2.resize(200, 20)

        self.admin_list = QComboBox(self)
        self.admin_list.move(390, 65)
        self.admin_list.resize(200, 30)
        self.admin_list.currentTextChanged.connect(self.update_admins)

        # self.admin_list.addItems()

        self.admin_list2 = QComboBox(self)
        self.admin_list2.move(600, 65)
        self.admin_list2.resize(200, 30)
        # self.admin_list2.addItems()

        self.add_admin = QPushButton("Зарегистрировать\nадминистратора", self)
        self.add_admin.move(175, 270)
        self.add_admin.resize(200, 50)
        self.add_admin.pressed.connect(self.addadmin)

        self.download_admin = QPushButton("Загрузить xls файл\nс администраторами", self)
        self.download_admin.move(10, 350)
        self.download_admin.resize(200, 50)
        self.download_admin.pressed.connect(self.downoladadmin)

        self.delete_admin = QPushButton("Удалить администратора", self)
        self.delete_admin.move(600, 90)
        self.delete_admin.resize(200, 30)
        self.delete_admin.pressed.connect(self.deleteadmin)

        self.remake_admin = QPushButton("Обновить информацию\nоб администраторе", self)
        self.remake_admin.move(395, 270)
        self.remake_admin.resize(200, 50)
        self.remake_admin.pressed.connect(self.change_info_admin)

        self.tableWidget_admin = QTableWidget(self)
        self.tableWidget_admin.setColumnCount(9)
        self.tableWidget_admin.move(250, 350)
        self.tableWidget_admin.resize(800, 200)
        self.tableWidget_admin.setHorizontalHeaderItem(0, QTableWidgetItem('логин'))
        self.tableWidget_admin.setHorizontalHeaderItem(1, QTableWidgetItem('пароль'))
        self.tableWidget_admin.setHorizontalHeaderItem(2, QTableWidgetItem('фамилия'))
        self.tableWidget_admin.setHorizontalHeaderItem(3, QTableWidgetItem('имя'))
        self.tableWidget_admin.setHorizontalHeaderItem(4, QTableWidgetItem('отчество'))
        self.tableWidget_admin.setHorizontalHeaderItem(5, QTableWidgetItem('номер_телефона'))
        self.tableWidget_admin.setHorizontalHeaderItem(6, QTableWidgetItem('гостиница'))
        self.tableWidget_admin.setHorizontalHeaderItem(7, QTableWidgetItem('заблокирован'))
        self.tableWidget_admin.setHorizontalHeaderItem(8, QTableWidgetItem('причина_блокировки'))

        # Гостиница

        self.number_of_hotel_label = QLabel("Номер гостиницы в сети:", self)
        self.number_of_hotel_label.move(10, 70)
        self.number_of_hotel_label.resize(self.number_of_hotel_label.sizeHint())

        self.number_of_hotel_linde_edit = QLineEdit(self)
        self.number_of_hotel_linde_edit.move(175, 70)
        self.number_of_hotel_linde_edit.resize(200, 20)

        self.level_hotel_label = QLabel("Количество этажей:", self)
        self.level_hotel_label.move(10, 100)
        self.level_hotel_label.resize(self.level_hotel_label.sizeHint())

        self.level_hotel_linde_edit = QLineEdit(self)
        self.level_hotel_linde_edit.move(175, 100)
        self.level_hotel_linde_edit.resize(200, 20)

        self.level_hotel_linde_edit2 = QLineEdit(self)
        self.level_hotel_linde_edit2.move(395, 100)
        self.level_hotel_linde_edit2.resize(200, 20)

        self.room_hotel_label = QLabel("Количество номеров:", self)
        self.room_hotel_label.move(10, 130)
        self.room_hotel_label.resize(self.room_hotel_label.sizeHint())

        self.room_hotel_linde_edit = QLineEdit(self)
        self.room_hotel_linde_edit.move(175, 130)
        self.room_hotel_linde_edit.resize(200, 20)

        self.room_hotel_linde_edit2 = QLineEdit(self)
        self.room_hotel_linde_edit2.move(395, 130)
        self.room_hotel_linde_edit2.resize(200, 20)

        self.country_hotel_label = QLabel("Страна:", self)
        self.country_hotel_label.move(10, 160)
        self.country_hotel_label.resize(self.country_hotel_label.sizeHint())

        self.country_hotel_linde_edit = QLineEdit(self)
        self.country_hotel_linde_edit.move(175, 160)
        self.country_hotel_linde_edit.resize(200, 20)

        self.country_hotel_linde_edit2 = QLineEdit(self)
        self.country_hotel_linde_edit2.move(395, 160)
        self.country_hotel_linde_edit2.resize(200, 20)

        self.city_hotel_label = QLabel("Город:", self)
        self.city_hotel_label.move(10, 190)
        self.city_hotel_label.resize(self.city_hotel_label.sizeHint())

        self.city_hotel_linde_edit = QLineEdit(self)
        self.city_hotel_linde_edit.move(175, 190)
        self.city_hotel_linde_edit.resize(200, 20)

        self.city_hotel_linde_edit2 = QLineEdit(self)
        self.city_hotel_linde_edit2.move(395, 190)
        self.city_hotel_linde_edit2.resize(200, 20)

        self.street_hotel_label = QLabel("Улица:", self)
        self.street_hotel_label.move(10, 220)
        self.street_hotel_label.resize(self.street_hotel_label.sizeHint())

        self.street_hotel_linde_edit = QLineEdit(self)
        self.street_hotel_linde_edit.move(175, 220)
        self.street_hotel_linde_edit.resize(200, 20)

        self.street_hotel_linde_edit2 = QLineEdit(self)
        self.street_hotel_linde_edit2.move(395, 220)
        self.street_hotel_linde_edit2.resize(200, 20)

        self.house_hotel_label = QLabel("Дом:", self)
        self.house_hotel_label.move(10, 250)
        self.house_hotel_label.resize(self.house_hotel_label.sizeHint())

        self.house_hotel_linde_edit = QLineEdit(self)
        self.house_hotel_linde_edit.move(175, 250)
        self.house_hotel_linde_edit.resize(200, 20)

        self.house_hotel_linde_edit2 = QLineEdit(self)
        self.house_hotel_linde_edit2.move(395, 250)
        self.house_hotel_linde_edit2.resize(200, 20)

        self.hotels_list = QComboBox(self)
        self.hotels_list.move(390, 65)
        self.hotels_list.resize(200, 30)
        self.hotels_list.currentTextChanged.connect(self.update_hotels)
        #self.hotels_list.addItems()

        self.hotels_list2 = QComboBox(self)
        self.hotels_list2.move(600, 65)
        self.hotels_list2.resize(200, 30)
        # self.hotels_list2.addItems()

        self.add_hotel = QPushButton("Создать гостиницу", self)
        self.add_hotel.move(175, 270)
        self.add_hotel.resize(200, 30)
        self.add_hotel.pressed.connect(self.addhotel)

        self.delete_hotel = QPushButton("Удалить гостиницу", self)
        self.delete_hotel.move(600, 90)
        self.delete_hotel.resize(200, 30)
        self.delete_hotel.pressed.connect(self.deletehotel)

        self.remake_hotel = QPushButton("Редактировать гостиницу", self)
        self.remake_hotel.move(395, 270)
        self.remake_hotel.resize(200, 30)
        self.remake_hotel.pressed.connect(self.change_info_hotel)

        self.label_filter = QLabel("Фильтры:", self)
        self.label_filter.move(10, 350)
        self.label_filter.resize(self.label_filter.sizeHint())

        self.label_filter_country = QLabel("Страна:", self)
        self.label_filter_country.move(10, 380)
        self.label_filter_country.resize(self.label_filter.sizeHint())

        self.box_filter_country = QComboBox(self)
        self.box_filter_country.move(60, 375)
        self.box_filter_country.resize(100, 30)

        self.check_filter_country = QCheckBox(self)
        self.check_filter_country.move(170, 380)
        self.check_filter_country.resize(self.label_filter.sizeHint())
        self.check_filter_country.stateChanged.connect(self.check_filter_country_change)

        self.label_filter_city = QLabel("Город:", self)
        self.label_filter_city.move(10, 410)
        self.label_filter_city.resize(self.label_filter.sizeHint())

        self.box_filter_city = QComboBox(self)
        self.box_filter_city.move(60, 405)
        self.box_filter_city.resize(100, 30)

        self.check_filter_city = QCheckBox(self)
        self.check_filter_city.move(170, 410)
        self.check_filter_city.resize(self.label_filter.sizeHint())
        self.check_filter_city.stateChanged.connect(self.check_filter_city_change)

        # Блокировка

        self.admins_label = QLabel("Пользователи:", self)
        self.admins_label.move(20, 70)
        self.admins_label.resize(self.admins_label.sizeHint())

        self.admins_list = QComboBox(self)
        self.admins_list.move(115, 65)
        self.admins_list.resize(200, 30)
        self.admins_list.addItems(self.login_admins)

        self.button_block = QPushButton("Заблокировать пользователя", self)
        self.button_block.move(190, 100)
        self.button_block.resize(300, 30)
        self.button_block.pressed.connect(self.block_admin)

        self.prichina = QLabel("Причина:", self)
        self.prichina.move(330, 70)
        self.prichina.resize(self.prichina.sizeHint())

        self.prichina_line_edit = QLineEdit(self)
        self.prichina_line_edit.move(400, 68)
        self.prichina_line_edit.resize(200, 20)

        self.tableWidget_hotel = QTableWidget(self)
        self.tableWidget_hotel.setColumnCount(7)
        self.tableWidget_hotel.move(250, 350)
        self.tableWidget_hotel.resize(800, 200)
        self.tableWidget_hotel.setHorizontalHeaderItem(0, QTableWidgetItem('название гостиницы'))
        self.tableWidget_hotel.setHorizontalHeaderItem(1, QTableWidgetItem('количество этажей'))
        self.tableWidget_hotel.setHorizontalHeaderItem(2, QTableWidgetItem('количество номеров'))
        self.tableWidget_hotel.setHorizontalHeaderItem(3, QTableWidgetItem('страна'))
        self.tableWidget_hotel.setHorizontalHeaderItem(4, QTableWidgetItem('город'))
        self.tableWidget_hotel.setHorizontalHeaderItem(5, QTableWidgetItem('улица'))
        self.tableWidget_hotel.setHorizontalHeaderItem(6, QTableWidgetItem('дом'))
        # неудачные попытки входа
        self.tableWidget_bt = QTableWidget(self)
        self.tableWidget_bt.setColumnCount(3)
        self.tableWidget_bt.move(10, 60)
        self.tableWidget_bt.resize(500, 400)
        self.tableWidget_bt.setHorizontalHeaderItem(0, QTableWidgetItem('Логин'))
        self.tableWidget_bt.setHorizontalHeaderItem(1, QTableWidgetItem('Пароль'))
        self.tableWidget_bt.setHorizontalHeaderItem(2, QTableWidgetItem('Время'))
        
    def init_functional_buttons(self):
        self.label_functional = QLabel("Функционал:", self)
        self.label_functional.move(10, 10)
        self.label_functional.resize(self.label_functional.sizeHint())

        self.radio_button_1 = QRadioButton("Управление администраторами гостиниц", self)
        self.radio_button_1.move(10, 30)

        self.radio_button_2 = QRadioButton("Гостиница", self)
        self.radio_button_2.move(310, 30)

        self.radio_button_3 = QRadioButton("Блокировка", self)
        self.radio_button_3.move(410, 30)

        self.radio_button_4 = QRadioButton("Просмотр неудачных попыток входа", self)
        self.radio_button_4.move(510, 30)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_1)
        self.button_group.addButton(self.radio_button_2)
        self.button_group.addButton(self.radio_button_3)
        self.button_group.addButton(self.radio_button_4)
        self.button_group.buttonClicked.connect(self.choose)

    def choose(self, button):
        self.choosen_functional = button.text()
        self.hide_all_widgets()
        if self.choosen_functional == "Блокировка":
            self.show_block_funtional()
        elif self.choosen_functional == "Гостиница":
            self.show_hotel_funtional()
        elif self.choosen_functional == "Управление администраторами гостиниц":
            self.show_admin_funtional()
        elif self.choosen_functional == "Просмотр неудачных попыток входа":
            self.show_bad_try()

    def hide_all_widgets(self):
        self.admins_label.hide()
        self.admins_list.hide()
        self.button_block.hide()
        self.prichina.hide()
        self.prichina_line_edit.hide()

        self.label_filter.hide()
        self.number_of_hotel_label.hide()
        self.number_of_hotel_linde_edit.hide()
        self.level_hotel_label.hide()
        self.level_hotel_linde_edit.hide()
        self.room_hotel_label.hide()
        self.room_hotel_linde_edit.hide()
        self.country_hotel_label.hide()
        self.country_hotel_linde_edit.hide()
        self.city_hotel_label.hide()
        self.city_hotel_linde_edit.hide()
        self.street_hotel_label.hide()
        self.street_hotel_linde_edit.hide()
        self.house_hotel_label.hide()
        self.house_hotel_linde_edit.hide()
        self.remake_hotel.hide()
        self.delete_hotel.hide()
        self.add_hotel.hide()
        self.hotels_list2.hide()
        self.hotels_list.hide()
        self.level_hotel_linde_edit2.hide()
        self.room_hotel_linde_edit2.hide()
        self.country_hotel_linde_edit2.hide()
        self.city_hotel_linde_edit2.hide()
        self.street_hotel_linde_edit2.hide()
        self.house_hotel_linde_edit2.hide()
        self.tableWidget_hotel.hide()
        self.label_filter_country.hide()
        self.box_filter_country.hide()
        self.check_filter_country.hide()
        self.label_filter_city.hide()
        self.box_filter_city.hide()
        self.check_filter_city.hide()

        self.download_admin.hide()
        self.login_of_admin_label.hide()
        self.login_of_admin_linde_edit.hide()
        self.password_admin_label.hide()
        self.password_admin_linde_edit.hide()
        self.password_admin_linde_edit2.hide()
        self.suname_admin_label.hide()
        self.suname_admin_linde_edit.hide()
        self.suname_admin_linde_edit2.hide()
        self.name_admin_label.hide()
        self.name_admin_linde_edit.hide()
        self.name_admin_linde_edit2.hide()
        self.otchestvo_admin_label.hide()
        self.otchestvo_admin_linde_edit.hide()
        self.otchestvo_admin_linde_edit2.hide()
        self.number_of_prhone_admin_label.hide()
        self.number_of_prhone_admin_linde_edit.hide()
        self.number_of_prhone_admin_linde_edit2.hide()
        self.hotel_admin_label.hide()
        self.hotel_admin_linde_edit.hide()
        self.hotel_admin_linde_edit2.hide()
        self.admin_list.hide()
        self.admin_list2.hide()
        self.add_admin.hide()
        self.delete_admin.hide()
        self.remake_admin.hide()
        self.tableWidget_admin.hide()

        self.tableWidget_bt.hide()


    def show_hotel_funtional(self):
        answer = self.send_to_server({"key": 'hotels_download'})
        if answer != "Error":
            self.name_hotel, self.hotels = answer
            hotels = self.hotels
            if self.check_filter_country_on:
                hotels = [i for i in hotels if i[3] == self.box_filter_country.currentText()]
            if self.check_filter_city_on:
                hotels = [i for i in hotels if i[4] == self.box_filter_city.currentText()]
            self.tableWidget_hotel.show()
            self.tableWidget_hotel.setRowCount(len(hotels))
            for i in range(len(hotels)):
                for j in range(7):
                    itm = QTableWidgetItem(hotels[i][j])
                    itm.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_hotel.setItem(i, j, itm)
            self.tableWidget_hotel.resizeColumnsToContents()
        self.hotels_list.clear()
        self.hotels_list.addItems(self.name_hotel)
        self.hotels_list2.clear()
        self.hotels_list2.addItems(self.name_hotel)
        self.box_filter_country.clear()
        self.box_filter_city.clear()
        self.box_filter_country.addItems([i[3] for i in self.hotels])
        self.box_filter_city.addItems([i[4] for i in self.hotels])
        hotel2 = "No"
        for i in self.hotels:
            if str(i[0]) == str(self.hotels_list.currentText()):
                hotel2 = i
        else:
            if hotel2 == "No":
                hotel2 = ['' for i in range(7)]
        hotel2 = [i if i else '' for i in hotel2]

        self.label_filter.show()
        self.label_filter_country.show()
        self.box_filter_country.show()
        self.check_filter_country.show()
        self.label_filter_city.show()
        self.box_filter_city.show()
        self.check_filter_city.show()
        self.number_of_hotel_label.show()
        self.number_of_hotel_linde_edit.show()
        self.level_hotel_label.show()
        self.level_hotel_linde_edit.show()
        self.room_hotel_label.show()
        self.room_hotel_linde_edit.show()
        self.country_hotel_label.show()
        self.country_hotel_linde_edit.show()
        self.city_hotel_label.show()
        self.city_hotel_linde_edit.show()
        self.street_hotel_label.show()
        self.street_hotel_linde_edit.show()
        self.house_hotel_label.show()
        self.house_hotel_linde_edit.show()
        self.remake_hotel.show()
        self.delete_hotel.show()
        self.add_hotel.show()
        self.hotels_list2.show()
        self.hotels_list.show()
        self.level_hotel_linde_edit2.show()
        self.level_hotel_linde_edit2.setText(str(hotel2[1]))
        self.room_hotel_linde_edit2.show()
        self.room_hotel_linde_edit2.setText(str(hotel2[2]))
        self.country_hotel_linde_edit2.show()
        self.country_hotel_linde_edit2.setText(str(hotel2[3]))
        self.city_hotel_linde_edit2.show()
        self.city_hotel_linde_edit2.setText(str(hotel2[4]))
        self.street_hotel_linde_edit2.show()
        self.street_hotel_linde_edit2.setText(str(hotel2[5]))
        self.house_hotel_linde_edit2.show()
        self.house_hotel_linde_edit2.setText(str(hotel2[6]))

    def show_admin_funtional(self):
        answer = self.send_to_server({"key": 'admin_download'})
        if answer != "Error":
            self.login_admins, self.admins, self.not_banned_admin = answer
            self.tableWidget_admin.show()
            self.tableWidget_admin.setRowCount(len(self.admins))
            for i in range(len(self.admins)):
                for j in range(9):
                    itm = QTableWidgetItem(self.admins[i][j])
                    itm.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_admin.setItem(i, j, itm)
            self.tableWidget_admin.resizeColumnsToContents()
        self.admin_list2.clear()
        self.admin_list2.addItems(self.login_admins)
        self.admin_list.clear()
        self.admin_list.addItems(self.login_admins)
        admin = "No"
        for i in self.admins:
            if str(i[0]) == str(self.admin_list.currentText()):
                admin = i
        else:
            if admin == "No":
                admin = ['' for i in range(7)]
        admin = [i if i else '' for i in admin]

        self.login_of_admin_label.show()
        self.login_of_admin_linde_edit.show()
        self.password_admin_label.show()
        self.password_admin_linde_edit.show()
        self.password_admin_linde_edit2.show()
        self.password_admin_linde_edit2.setText(str(admin[1]))
        self.suname_admin_label.show()
        self.suname_admin_linde_edit.show()
        self.suname_admin_linde_edit2.show()
        self.suname_admin_linde_edit2.setText(str(admin[2]))
        self.name_admin_label.show()
        self.name_admin_linde_edit.show()
        self.name_admin_linde_edit2.show()
        self.name_admin_linde_edit2.setText(str(admin[3]))
        self.otchestvo_admin_label.show()
        self.download_admin.show()
        self.otchestvo_admin_linde_edit.show()
        self.otchestvo_admin_linde_edit2.show()
        self.otchestvo_admin_linde_edit2.setText(str(admin[4]))
        self.number_of_prhone_admin_label.show()
        self.number_of_prhone_admin_linde_edit.show()
        self.number_of_prhone_admin_linde_edit2.show()
        self.number_of_prhone_admin_linde_edit2.setText(str(admin[5]))
        self.hotel_admin_label.show()
        self.hotel_admin_linde_edit.show()
        self.hotel_admin_linde_edit2.show()
        self.hotel_admin_linde_edit2.setText(str(admin[6]))
        self.admin_list.show()
        self.admin_list2.show()
        self.add_admin.show()
        self.delete_admin.show()
        self.remake_admin.show()

    def addadmin(self):
        login = self.login_of_admin_linde_edit.text()
        password = self.password_admin_linde_edit.text()
        surname = self.suname_admin_linde_edit.text()
        name = self.name_admin_linde_edit.text()
        father_name = self.otchestvo_admin_linde_edit.text()
        number_of_phone = self.number_of_prhone_admin_linde_edit.text()
        hotel = self.hotel_admin_linde_edit.text()
        if  login and password and surname and name and father_name and number_of_phone and hotel:
            admin = [login, password, surname, name, father_name, number_of_phone, hotel]
            admin = "|||".join(admin)
            ok = self.send_to_server({"key": "add_admin",
                                 "login": admin})
            if ok:
                self.info("Администратор успешно зарегистрирован", False)
            else:
                self.info("Администратор не был зарегистрирован", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_admin_funtional()

    def change_info_admin(self):
        login = self.admin_list.currentText()
        password = self.password_admin_linde_edit2.text()
        surname = self.suname_admin_linde_edit2.text()
        name = self.name_admin_linde_edit2.text()
        father_name = self.otchestvo_admin_linde_edit2.text()
        number_of_phone = self.number_of_prhone_admin_linde_edit2.text()
        hotel = self.hotel_admin_linde_edit2.text()
        if  login and password and surname and name and father_name and number_of_phone and hotel:
            admin = [login, password, surname, name, father_name, number_of_phone, hotel]
            admin = "|||".join(admin)
            ok = self.send_to_server({"key": "change_info_admin",
                                 "login": admin})
            if ok:
                self.info("Информация об администраторе успешно обновлена", False)
            else:
                self.info("Информация об администраторе не обновлена", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_admin_funtional()

    def addhotel(self):
        name = self.number_of_hotel_linde_edit.text()
        levels = self.level_hotel_linde_edit2.text()
        rooms = self.room_hotel_linde_edit2.text()
        country = self.country_hotel_linde_edit2.text()
        city = self.city_hotel_linde_edit2.text()
        street = self.street_hotel_linde_edit2.text()
        house = self.house_hotel_linde_edit2.text()
        if  name and levels and rooms and country and city and street and house:
            hotel = [name, levels, rooms, country, city, street, house]
            hotel = "|||".join(hotel)
            ok = self.send_to_server({"key": "add_hotel",
                                 "name": hotel})
            if ok:
                self.info("Гостиница успешно добавлена", False)
            else:
                self.info("Гостиница не была добавлена", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_hotel_funtional()

    def change_info_hotel(self):
        name = self.hotels_list.currentText()
        levels = self.level_hotel_linde_edit2.text()
        rooms = self.room_hotel_linde_edit2.text()
        country = self.country_hotel_linde_edit2.text()
        city = self.city_hotel_linde_edit2.text()
        street = self.street_hotel_linde_edit2.text()
        house = self.house_hotel_linde_edit2.text()
        if  name and levels and rooms and country and city and street and house:
            hotel = [name, levels, rooms, country, city, street, house]
            hotel = "|||".join(hotel)
            ok = self.send_to_server({"key": "change_info_hotel",
                                 "name": hotel})
            if ok:
                self.info("Информация о гостинице успешно обновлена", False)
            else:
                self.info("Информация о гостинице не обновлена", True)
        else:
            self.info("Введенные данные некорректны", True)
        self.show_hotel_funtional()

    def block_admin(self):
        admin = self.admins_list.currentText()
        reason = self.prichina_line_edit.text()
        ok = self.send_to_server({"key": "ban_admin",
                             "login": admin,
                             "reason": reason})
        if ok:
            self.info("Пользователь успешно добавлен в список заблокированных", False)
        else:
            self.info("Пользователь не добавлен в список заблокированных", True)
        self.show_block_funtional()

    def deleteadmin(self):
        admin = self.admin_list2.currentText()
        ok = self.send_to_server({"key": "delete_admin",
                             "login": admin})
        if ok:
            self.info("Администратор успешно удален", False)
        else:
            self.info("Администратор не удален", True)

        self.show_admin_funtional()

    def deletehotel(self):
        name = self.hotels_list2.currentText()
        rooms = self.send_to_server({"key": "rooms"})
        for i in rooms:
            if i[0] == name:
                self.info("Гостиница не удалена, так как она связана с номерами", True)
                return

        ok = self.send_to_server({"key": "delete_hotel",
                             "name": name})
        if ok:
            self.info("Гостиница успешно удалена", False)
        else:
            self.info("Гостиница не удалена", True)
        self.show_hotel_funtional()

    def show_block_funtional(self):
        answer = self.send_to_server({"key": 'admin_download'})
        if answer != "Error":
            self.login_admins, self.admins, self.not_banned_admin = answer
        self.admins_list.clear()
        self.admins_list.addItems(self.not_banned_admin)
        self.admins_label.show()
        self.admins_list.show()
        self.button_block.show()
        self.prichina.show()
        self.prichina_line_edit.show()

    def update_admins(self):
        admin = "No"
        for i in self.admins:
            if str(i[0]) == str(self.admin_list.currentText()):
                admin = i
        else:
            if admin == "No":
                admin = ['' for i in range(7)]
        admin = [i if i else '' for i in admin]
        self.password_admin_linde_edit2.setText(str(admin[1]))
        self.suname_admin_linde_edit2.setText(str(admin[2]))
        self.name_admin_linde_edit2.setText(str(admin[3]))
        self.otchestvo_admin_linde_edit2.setText(str(admin[4]))
        self.number_of_prhone_admin_linde_edit2.setText(str(admin[5]))
        self.hotel_admin_linde_edit2.setText(str(admin[6]))

    def update_hotels(self):
        hotel2 = "No"
        for i in self.hotels:
            if str(i[0]) == str(self.hotels_list.currentText()):
                hotel2 = i
        else:
            if hotel2 == "No":
                hotel2 = ['' for i in range(7)]
        hotel2 = [i if i else '' for i in hotel2]
        self.level_hotel_linde_edit2.setText(str(hotel2[1]))
        self.room_hotel_linde_edit2.setText(str(hotel2[2]))
        self.country_hotel_linde_edit2.setText(str(hotel2[3]))
        self.city_hotel_linde_edit2.setText(str(hotel2[4]))
        self.street_hotel_linde_edit2.setText(str(hotel2[5]))
        self.house_hotel_linde_edit2.setText(str(hotel2[6]))

    def downoladadmin(self):
        location = QFileDialog.getOpenFileName(self, 'Open file')[0]
        try:
            admins = read_info_about_administrators(location)
        except:
            self.info("Возникла ошибка при загрузке данных", True)
            return
        oks = []
        for i in admins:
            if all(i):
                admin = "|||".join(i)
                ok = self.send_to_server({"key": "add_admin",
                                          "login": admin})
                oks.append(ok)
        if all(oks):
            self.info("Информация загружена успешна", False)
        else:
            self.info("Не вся информация была загружена", True)
        self.show_admin_funtional()

    def show_bad_try(self):
        answer = self.send_to_server({"key": 'bad_try_download'})
        if answer != "Error":
            self.bad_try = answer
            self.tableWidget_bt.show()
            self.tableWidget_bt.setRowCount(len(self.bad_try))
            for i in range(len(self.bad_try)):
                for j in range(3):
                    itm = QTableWidgetItem(self.bad_try[i][j])
                    itm.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_bt.setItem(i, j, itm)
            self.tableWidget_bt.resizeColumnsToContents()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UiManagerWindow()
    MainWindow.show()
    sys.exit(app.exec())
