from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(581, 675)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.list_attractions = QtWidgets.QListWidget(self.centralwidget)
        self.list_attractions.setGeometry(QtCore.QRect(20, 280, 541, 351))
        self.list_attractions.setObjectName("list_attractions")
        self.find_attractions = QtWidgets.QPushButton(self.centralwidget)
        self.find_attractions.setGeometry(QtCore.QRect(20, 20, 211, 91))
        self.find_attractions.setObjectName("find_attractions")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 581, 26))
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
        self.find_attractions.setText(_translate("MainWindow", "Найти достопримечательности"))
