# -*- encoding: utf-8 -*-
import socket
import threading
import datetime
from time import gmtime, strftime


class Server:

    #{ id : name }
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
                nickname = connection.recv(1024).decode()
                print(connection.fileno(), '=', nickname)

                self.UserId_Name[connection.fileno()] = nickname

                # 歡迎新使用者進入
                self.welcome(connection.fileno())

                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()

            else:
                connection.send(b'please go out!')
                connection.close()
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
                except:
                    pass

                myconnection.close()
                return


def main():
    #140.138.145.57
    s = Server('140.138.145.57', 5550)
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

