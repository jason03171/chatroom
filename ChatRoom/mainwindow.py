# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 31))
        self.label.setObjectName("label")
        self.nickname = QtWidgets.QLineEdit(self.centralwidget)
        self.nickname.setGeometry(QtCore.QRect(80, 40, 131, 31))
        self.nickname.setObjectName("nickname")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(360, 40, 101, 31))
        self.login.setStyleSheet("")
        self.login.setObjectName("login")
        self.brower = QtWidgets.QTextBrowser(self.centralwidget)
        self.brower.setGeometry(QtCore.QRect(20, 120, 441, 351))
        self.brower.setObjectName("brower")
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(20, 530, 441, 23))
        self.send.setObjectName("send")
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(20, 480, 441, 41))
        self.message.setObjectName("message")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(230, 40, 113, 31))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.count = QtWidgets.QLabel(self.centralwidget)
        self.count.setGeometry(QtCore.QRect(20, 10, 431, 21))
        self.count.setObjectName("count")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 51, 31))
        self.label_3.setObjectName("label_3")
        self.change = QtWidgets.QLineEdit(self.centralwidget)
        self.change.setGeometry(QtCore.QRect(170, 79, 171, 31))
        self.change.setObjectName("change")
        self.update = QtWidgets.QPushButton(self.centralwidget)
        self.update.setGeometry(QtCore.QRect(360, 80, 101, 31))
        self.update.setObjectName("update")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Nick Name"))
        self.login.setText(_translate("MainWindow", "Login"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.count.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "變更密碼"))
        self.update.setText(_translate("MainWindow", "Update Password"))

