from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox, QFrame
from PyQt5.QtCore import QTimer, QTime, QRect
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QMessageBox, QLCDNumber
from administrator import UiAdministratorWindow
from manager import UiManagerWindow
import sqlite3
import timeit
import sys
from constants import *
from make_and_read_documents import *
from datetime import datetime, timedelta
import socket
import sys
from threading import Thread;
import json
import network


class UiLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.password = ""
        self.ip = "0.0.0.0:5555"
        self.sockIn = network.connect_InSocket(address='0.0.0.0', port=5556)
        self.sockOut = network.connect_OutSocket(address=self.ip.split(':')[0], port=int(self.ip.split(':')[1]))
        self.time_block, self.chance = read_time()
        self.login_password_admin, self.login_password_manager, self.banned_admin = self.get_admin_manager()

    def disconnect_server(self):
        network.alive = False
        network.close_sock(self.sockIn)
        network.close_sock(self.sockOut)

    def closeEvent(self, QCloseEvent):
        self.disconnect_server()

    def get_admin_manager(self):
        msg = json.dumps({"key": "login"})
        network.sock_send(self.sockOut, msg)
        try:
            self.sockIn.settimeout(2)
            data, address = network.read_sock(self.sockIn)
            self.sockIn.settimeout(None)
        except socket.timeout:
            self.info_label.setText('Сервер отключен! Проверьте соединение')
            self.info_label.resize(self.info_label.sizeHint())
            return [{}, {}, {}]
        msg = json.loads(data)
        return msg

    def bad_try_login(self, login, password, time):
        msg = json.dumps({"key": "bad_try_login",
                          "login": str(login),
                          "password": str(password),
                          "time": str(time)})
        network.sock_send(self.sockOut, msg)
        try:
            self.sockIn.settimeout(2)
            data, address = network.read_sock(self.sockIn)
            self.sockIn.settimeout(None)
        except socket.timeout:
            self.info_label.setText('Сервер отключен! Проверьте соединение')
            self.info_label.resize(self.info_label.sizeHint())
            return [{}, {}, {}]
        msg = json.loads(data)

    def initUI(self):
        self.setGeometry(400, 400, 300, 180)
        self.setWindowTitle('Вход в систему')

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QRect(10, 140, 100, 30))
        self.lcdNumber.setFrameShape(QFrame.Box)

        self.info_label = QLabel(self)
        self.info_label.move(10, 90)
        self.info_label.resize(self.info_label.sizeHint())
        self.info_label.setStyleSheet('color: red')

        self.login = QLabel("Логин:", self)
        self.login.move(10, 10)
        self.login.resize(self.login.sizeHint())

        self.password = QLabel("Пароль:", self)
        self.password.move(10, 40)
        self.password.resize(self.password.sizeHint())

        self.login_line_edit = QLineEdit(self)
        self.login_line_edit.move(65, 10)
        self.login_line_edit.resize(200, 20)


        self.password_line_edit = QLineEdit(self)
        self.password_line_edit.move(65, 40)
        self.password_line_edit.resize(200, 20)
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        self.go_in = QPushButton("Войти", self)
        self.go_in.move(60, 60)
        self.go_in.resize(100, 30)
        self.go_in.pressed.connect(self.log_in_system)

        self.back = QPushButton("Отмена", self)
        self.back.move(150, 60)
        self.back.resize(100, 30)
        self.back.pressed.connect(lambda: self.close())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.lcdNumber.hide()

    def showTime(self):
        if self.begin == datetime.strptime(str(self.time_block[-8:]), '%H:%M:%S'):
            self.timer.stop()
            self.lcdNumber.hide()
            self.info_label.setText("Вы опять можете войти в систему")
            self.info_label.setStyleSheet('color: green')
            return
        self.begin = self.begin + timedelta(seconds=1)
        showing_time = datetime.strptime(str(self.time_block[-8:]), '%H:%M:%S') - \
                       datetime.strptime(str(self.begin.strftime('%Y-%m-%d %H:%M:%S').split()[1]),
                                       '%H:%M:%S')

        self.lcdNumber.display(str(showing_time).split()[0])

    def check_time(self, time_block):
        time_ = time_block
        now = str(list(str(datetime.now()).split("."))[0])
        date_block = str(list(str(time_block).split())[0]).split("-")
        date_now = str(list(str(now).split())[0]).split("-")
        time_block = str(list(str(time_block).split())[1]).split(":")
        time_now = str(list(str(now).split())[1]).split(":")
        if (date_block[0] > date_now[0]) or (date_block[0] >= date_now[0] and date_block[1] > date_now[1]) or (date_block[0] >= date_now[0] and date_block[1] >= date_now[1] and date_block[2] >= date_now[2]):
            if (time_block[0] > time_now[0]) or (time_block[0] >= time_now[0] and time_block[1] > time_now[1]) or (time_block[0] >= time_now[0] and time_block[1] >= time_now[1] and time_block[2] > time_now[2]):
                return time_
            else:
                return "0000-00-00 00:00:00"
        else:
            return "0000-00-00 00:00:00"

    def add_one_minute(self, time):
        date_block = str(list(str(time).split())[0]).split("-")
        time_block = str(list(str(time).split())[1]).split(":")
        if int(time_block[1]) + 1 < 60:
            time_block[1] = str(int(time_block[1]) + 1) if len(str(int(time_block[1]) + 1)) == 2 else "0" + str(int(time_block[1]) + 1)
        elif int(time_block[0]) + 1 < 24:
            time_block[0] = str(int(time_block[0]) + 1) if len(str(int(time_block[0]) + 1)) == 2 else "0" + str(int(time_block[0]) + 1)
        elif int(date_block[2]) + 1 < 31:
            date_block[2] = str(int(date_block[2]) + 1) if len(str(int(date_block[2]) + 1)) == 2 else "0" + str(int(date_block[2]) + 1)
        return f"{date_block[0]}-{date_block[1]}-{date_block[2]} {time_block[0]}:{time_block[1]}:{time_block[2]}"

    def log_in_system(self):
        login = self.login_line_edit.text()
        password = self.password_line_edit.text()
        self.time_block = self.check_time(self.time_block)
        if self.time_block[:10] != "0000-00-00":
            self.info_label.setText("Подождите вход в систему пока недоступен")
            self.info_label.resize(self.info_label.sizeHint())
            self.info_label.setStyleSheet('color: red')
            self.lcdNumber.show()
            self.turn_on_timer()
            return
        self.login_password_admin, self.login_password_manager, self.banned_admin = self.get_admin_manager()

        if self.login_password_admin == {} and self.login_password_manager == {} and self.banned_admin == {}:
            self.info_label.setText('Сервер отключен! Проверьте соединение')
            self.info_label.resize(self.info_label.sizeHint())
            self.info_label.setStyleSheet('color: red')
            return
        if login in self.login_password_admin.keys() and str(self.login_password_admin[login]) == str(password) and \
                login not in self.banned_admin.keys():
            self.disconnect_server()
            time_block = str(list(str(datetime.now()).split("."))[0])
            chance = "3"
            write_time(time_block, chance)
            self.Window = UiAdministratorWindow(login)
            self.Window.show()
            UiLoginWindow.close(self)
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Добро пожаловать")
            msg.setInformativeText("Вы вошли в систему как администратор")
            result = msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif login in self.login_password_manager.keys() and str(self.login_password_manager[login]) == str(password):
            self.disconnect_server()
            time_block = str(list(str(datetime.now()).split("."))[0])
            chance = "3"
            write_time(time_block, chance)
            self.Window = UiManagerWindow(login)
            self.Window.show()
            UiLoginWindow.close(self)
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Добро пожаловать")
            msg.setInformativeText("Вы вошли в систему как управляющий гостиницей")
            result = msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            if login in self.banned_admin.keys() and \
                    login in self.login_password_admin.keys() and self.login_password_admin[login] == password:
                if self.banned_admin[login]:
                    self.time_and_chances()
                    if self.chance != "3":
                        self.info_label.setText(f"Профиль заблокирован\nПричина: {self.banned_admin[login]}\nКоличество оставшихся попыток: {self.chance}")
                        self.bad_try_login(login, password, datetime.now())
                    else:
                        self.info_label.setText("Подождите вход в систему пока недоступен")
                        self.lcdNumber.show()
                        self.turn_on_timer()
                    self.info_label.setStyleSheet('color: red')
                    self.info_label.resize(self.info_label.sizeHint())
                else:
                    self.time_and_chances()
                    if self.chance != "3":
                        self.info_label.setText(f"Профиль заблокирован\nКоличество оставшихся попыток: {self.chance}")
                        self.bad_try_login(login, password, datetime.now())
                    else:
                        self.info_label.setText("Подождите вход в систему пока недоступен")
                        self.lcdNumber.show()
                        self.turn_on_timer()
                    self.info_label.setStyleSheet('color: red')
                    self.info_label.resize(self.info_label.sizeHint())
            else:
                self.time_and_chances()
                if self.chance != "3":
                    self.info_label.setText(f"Профиль или пароль введены неверно\nКоличество оставшихся попыток: {self.chance}")
                    self.bad_try_login(login, password, datetime.now())
                else:
                    self.info_label.setText("Подождите вход в систему пока недоступен")
                    self.lcdNumber.show()
                    self.turn_on_timer()
                self.info_label.setStyleSheet('color: red')
                self.info_label.resize(self.info_label.sizeHint())

    def time_and_chances(self):
        self.chance = str(int(self.chance) - 1)
        if self.chance == "0":
            self.time_block = self.add_one_minute(str(list(str(datetime.now()).split("."))[0]))
            self.chance = "3"
        write_time(self.time_block, self.chance)

    def turn_on_timer(self):
        self.timer.start(1000)
        self.begin = datetime.strptime(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[1]),
                                       '%H:%M:%S')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UiLoginWindow()
    MainWindow.show()
    sys.exit(app.exec())
