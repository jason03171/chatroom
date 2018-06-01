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
        MainWindow.resize(341, 464)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.users = QtWidgets.QTextEdit(self.centralwidget)
        self.users.setGeometry(QtCore.QRect(10, 80, 321, 291))
        self.users.setObjectName("users")
        self.delete = QtWidgets.QPushButton(self.centralwidget)
        self.delete.setGeometry(QtCore.QRect(10, 380, 321, 31))
        self.delete.setObjectName("del")
        self.add = QtWidgets.QPushButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(10, 40, 321, 31))
        self.add.setObjectName("add")
        self.nickname = QtWidgets.QLineEdit(self.centralwidget)
        self.nickname.setGeometry(QtCore.QRect(60, 10, 101, 20))
        self.nickname.setObjectName("nickname")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(220, 10, 113, 20))
        self.password.setObjectName("password")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 61, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 341, 22))
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
        self.delete.setText(_translate("MainWindow", "Del"))
        self.add.setText(_translate("MainWindow", "Add"))
        self.label.setText(_translate("MainWindow", "Nickname"))
        self.label_2.setText(_translate("MainWindow", "Password"))

