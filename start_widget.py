# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(430, 238)
        self.sing_up_dec_button = QtWidgets.QPushButton(Form)
        self.sing_up_dec_button.setGeometry(QtCore.QRect(130, 87, 181, 51))
        self.sing_up_dec_button.setObjectName("sing_up_dec_button")
        self.sing_in_dec_button = QtWidgets.QPushButton(Form)
        self.sing_in_dec_button.setGeometry(QtCore.QRect(130, 160, 181, 51))
        self.sing_in_dec_button.setObjectName("sing_in_dec_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 0, 391, 96))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sing_up_dec_button.setText(_translate("Form", "Регистрация пользователя"))
        self.sing_in_dec_button.setText(_translate("Form", "Вход"))
        self.label.setText(_translate("Form", "<center>Поиск достопримечательностей</center>"))
