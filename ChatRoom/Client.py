import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication
import mainwindow
import sys

class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

        #顯示歡迎訊息 向server傳nickname
        print('Welcome to chat room! ')
        nickname = input('Input your nickname : ')
        self.sock.send(nickname.encode())
        print("Now Lets Chat, ",nickname)

    def sendThreadFunc(self):
        while True:
            try:
                myword = input()
                self.sock.send(myword.encode())
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

class Qt_Window_Main(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)

def main():
    c = Client('localhost', 5550)
    th1 = threading.Thread(target=c.sendThreadFunc)
    th2 = threading.Thread(target=c.recvThreadFunc)
    threads = [th1, th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

if __name__ == "__main__":
    #main()
    app = QApplication(sys.argv)
    MainWindow = Qt_Window_Main()
    MainWindow.show()
    sys.exit(app.exec_())
