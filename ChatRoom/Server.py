# -*- encoding: utf-8 -*-
import socket
import threading
import datetime
import serverlayout
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, \
    QTextBrowser
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from time import gmtime, strftime
from pymongo import MongoClient
from bson.objectid import ObjectId

# 通訊類型
from enum import Enum, IntEnum, unique

try:
    @unique
    class OPERATION(Enum):
        MSG = "0"
        NUMCHANGE = "1"
        #ISALIVE = "2"
        #CONNECT = "3"
        CHANGEPWD = "4"
        #PWDCHANGE = "5"
        LOGIN = "6"
except ValueError as e:
    print(e)

spliteTag = '$@~&*^$'

class Server:

    #紀錄登入的使用者id和nickname { id : nickname }
    UserId_Name = dict()

    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')
        self.mylist = list()

    def checkConnection(self):
        connection, addr = self.sock.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())

        try:
            buf = connection.recv(1024).decode()
            if buf == '1':
                # start a thread for new connection

                #紀錄使用者名稱
                token = connection.recv(1024).decode()

                _ , nickname , password = token.split(spliteTag)

                print(connection.fileno(), '=', nickname)

                self.UserId_Name[connection.fileno()] = nickname

                # 歡迎新使用者進入
                self.welcome(connection.fileno())
                self.showCount()

                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()

            else:
                connection.send(b'please go out!')
                connection.close()
        except:
            pass


    def showCount(self):
        for c in self.mylist:
            try:
                fullMessage = "SYSTEM: Online User count = {}".format(len(self.UserId_Name))
                c.send(fullMessage.encode())
            except:
                pass

    # 歡迎新使用者進入
    def welcome(self, exceptNum):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                try:
                    #名字 + 訊息
                    fullMessage = "SYSTEM: " + self.UserId_Name[exceptNum] + " in the chat room"
                    c.send(fullMessage.encode())
                except:
                    pass

    def tellAll(self, whatToSay):
        for c in self.mylist:
            try:
                c.send(whatToSay.encode())
            except:
                pass

    # send whatToSay to every except people in exceptNum
    def tellOthers(self, exceptNum, whatToSay):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                try:
                    #server時間
                    send_time = datetime.datetime.now().strftime("[%H:%M:%S]")
                    #名字 + 訊息 + 時間
                    fullMessage = self.UserId_Name[exceptNum] + ': ' + whatToSay + '\t' + send_time
                    c.send(fullMessage.encode())
                except:
                    pass

    def subThreadIn(self, myconnection, connNumber):
        self.mylist.append(myconnection)
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg)
                else:
                    pass

            except (OSError, ConnectionResetError):
                try:
                    self.mylist.remove(myconnection)
                    msg = "User " + self.UserId_Name[connNumber] + ' leave'
                    self.tellAll(msg)
                    print('Disconnected name:{} id:{}'.format(self.UserId_Name[connNumber], connNumber))

                    del self.UserId_Name[connNumber]
                    self.showCount()
                except:
                    pass

                myconnection.close()
                return


def main():
    s = Server('localhost', 5550)
    while True:
        s.checkConnection()

class Qt_Window_Main(QMainWindow, serverlayout.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.client = MongoClient('localhost', 27017)
        self.database = self.client["ChatRoom"]  # SQL: Database Name
        self.collection = self.database["user"]  # SQL: Table Name

        self.add.clicked.connect(self.adduser)

        self.delete.clicked.connect(self.deleteuser)

    def adduser(self):
        nickname = self.nickname.text()
        password = self.password.text()

        self.collection.insert_one({'uname':nickname, 'upwd':password})

    def deleteuser(self):
        self.collection.delete_one()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Qt_Window_Main()

    MainWindow.show()
    sys.exit(app.exec_())
