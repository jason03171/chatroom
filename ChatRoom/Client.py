import socket
import threading
import mainwindow
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout
from PyQt5.QtCore import QThread, pyqtSignal


class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

        '''
        #顯示歡迎訊息 向server傳nickname
        print('Welcome to chat room! ')
        nickname = input('Input your nickname : ')
        self.sock.send(nickname.encode())
        print("Now Lets Chat, ",nickname)
        '''

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


class TutorialThread(QThread):
    getmess = pyqtSignal(int)
    c = None

    def __init__(self, c):
        QThread.__init__(self)
        self.c = c

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            try:
                self.getmess.update.emit(self.c.recvThreadFunc())
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')


class Qt_Window_Main(QMainWindow, mainwindow.Ui_MainWindow):
    c = Client('localhost', 5550)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self._tutorial_thread = TutorialThread(self.c)
        # self._tutorial_thread.brower.connect(self.settext)
        self.send.clicked.connect(self.sendmes)

        self.send.setText("send")
        self.send.clicked.connect(self.sendmes)

    def settext(self, data):
        self.brower.append(data)
        self.brower.update()

    def sendmes(self):
        self.c.sendThreadFunc(self.message.text())
        self.brower.append(self.message.text())
        self.brower.update()
        self.message.setText("")

    def start(self):
        self._tutorial_thread.start()

    def stop(self):
        self._tutorial_thread.terminate()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Qt_Window_Main()

    MainWindow.show()
    sys.exit(app.exec_())
