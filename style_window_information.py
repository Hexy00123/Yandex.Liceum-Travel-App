# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window2_2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window_Information(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(502, 683)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 40, 461, 791))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(190, 190, 55, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(160, 560, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab_3")
        self.inform = QtWidgets.QLabel(self.tab3)
        self.inform.setGeometry(QtCore.QRect(10, 10, 430, 570))
        self.inform.setWordWrap(True)
        self.inform.setObjectName("label")
        self.image_map = QtWidgets.QLabel(self.tab_2)
        self.image_map.setGeometry(QtCore.QRect(180, 170, 55, 16))
        self.image_map.setObjectName("image_map")
        self.adress = QtWidgets.QLabel(self.tab_2)
        self.adress.setGeometry(QtCore.QRect(20, 550, 111, 31))
        self.adress.setStyleSheet("font-size: 17px")
        self.adress.setObjectName("adress")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.addTab(self.tab3, "")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 502, 26))
        self.menubar.setObjectName("menubar")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "в избранное"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Фото"))
        self.image_map.setText(_translate("MainWindow", "TextLabel"))
        self.adress.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("MainWindow", "Описание"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Адресс"))
