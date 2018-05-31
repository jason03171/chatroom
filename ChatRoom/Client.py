import socket
import threading
import mainwindow
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, \
    QTextBrowser
from PyQt5.QtCore import QThread, pyqtSignal, Qt


class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

    def sendNickName(self, NickName):
        self.sock.send(NickName.encode())

    def sendThreadFunc(self, myword):
        try:
            self.sock.send(myword.encode())
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
        self.nickname.setEnabled(False)
        self.login.setEnabled(False)
        self.c.sendNickName(nickname)

        # init ReadMsgThread
        self._ReadMsgThread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Qt_Window_Main()

    MainWindow.show()
    sys.exit(app.exec_())
