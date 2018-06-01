import socket
import threading
import mainwindow
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, \
    QTextBrowser
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# 通訊類型
from enum import Enum, IntEnum, unique

try:
    @unique
    class OPERATION(Enum):
        MSG = "0"
        NUMCHANGE = "1"
        ISALIVE = "2"
        CONNECT = "3"
        CHANGEPWD = "4"
        PWDCHANGE = "5"
        LOGIN = "6"
except ValueError as e:
    print(e)

spliteTag = '$@~&*^$'


class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

    def sendNickName(self, NickName, password):
        token = spliteTag.join([OPERATION.LOGIN, NickName, password])
        self.sock.send(token.encode())

    def sendThreadFunc(self, myword):
        try:
            token = spliteTag.join([OPERATION.MSG, myword])
            self.sock.send(token.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')

    def recvThreadFunc(self):
        try:
            otherword = self.sock.recv(1024)  # socket.recv(recv_size)  # print(otherword.decode())
            return otherword.decode()
        except ConnectionAbortedError:
            print('Server closed this connection!')


        except ConnectionResetError:
            print('Server is closed!')

    def sendNewPassword(self, newPassowrd):
        token = spliteTag.join([OPERATION.PWDCHANGE, newPassowrd])
        self.sock.send(token.encode())

class ReadMsgThread(QThread):
    getMsg = pyqtSignal(str)
    c = None

    def __init__(self, c):
        QThread.__init__(self)
        self.c = c

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            try:
                msg = self.c.recvThreadFunc()
                self.getMsg.emit(msg)
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')


class Qt_Window_Main(QMainWindow, mainwindow.Ui_MainWindow):
    c = Client('localhost', 5550)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self._ReadMsgThread = ReadMsgThread(self.c)
        self._ReadMsgThread.getMsg.connect(self.onRecvMsg)

        self.send.clicked.connect(self.sendMsg)

        self.login.clicked.connect(self.onLogin)

        self.update.clicked.connect(self.onUpdatePassword)

    def onRecvMsg(self, data):
        self.brower.append(data)
        # 字置左
        cursor = self.brower.textCursor()
        blockFormat = cursor.blockFormat()
        blockFormat.setAlignment(Qt.AlignLeft)

        cursor.mergeBlockFormat(blockFormat)
        self.brower.setTextCursor(cursor)

        self.brower.update()

    def sendMsg(self):
        # 忽略空字串
        if self.message.text().isspace() or len(self.message.text()) == 0:
            self.message.setText("")
            return

        self.c.sendThreadFunc(self.message.text())

        self.brower.append(self.message.text() + ":You")

        # 字置右
        cursor = self.brower.textCursor()
        blockFormat = cursor.blockFormat()
        blockFormat.setAlignment(Qt.AlignRight)

        cursor.mergeBlockFormat(blockFormat)
        self.brower.setTextCursor(cursor)

        self.brower.update()

        self.message.setText("")

    def onLogin(self):
        nickname = self.nickname.text()
        password = self.password.text()

        self.nickname.setEnabled(False)
        self.password.setEnabled(False)
        self.login.setEnabled(False)
        self.c.sendNickName(nickname, password)

        # init ReadMsgThread
        self._ReadMsgThread.start()

    def onUpdatePassword(self):
        if self.change.text().isspace() or len(self.change.text()) == 0:
            self.change.setText("")
            return

        newPassWord = self.change.text()
        self.c.sendNewPassword(newPassWord)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Qt_Window_Main()

    MainWindow.show()
    sys.exit(app.exec_())
