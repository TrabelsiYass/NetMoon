# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginui4.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
import sys
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(450, 550)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(50, 50, 370, 600))
        self.widget.setStyleSheet(u"QPushButton #pushButton,#pushButton_r{	\n"
"	background-color: #000;\n"
"	color:rgba(255, 255, 255, 210);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton#pushButton:hover ,#pushButton_r:hover{	\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#pushButton:pressed,#pushButton_r:pressed{	\n"
"	padding-left:5px;\n"
"	padding-top:5px;\n"
"	background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#pushButton_2,#pushButton_pasw, #pushButton_3, #pushButton_4, #pushButton_5{	\n"
"	background-color: rgba(0, 0, 0, 0);\n"
"	color:rgba(85, 98, 112, 255);\n"
"}\n"
"QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover,#pushButton_pasw:hover{	\n"
"	color:rgba(155, 168, 182, 220);\n"
"}\n"
"QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed,#pushButton_pasw:pressed{	\n"
"	padding-left:5px;\n"
"	padding-top:5px;"
                        "\n"
"	color:rgba(115, 128, 142, 255);\n"
"}")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 30, 300, 420))
        self.label.setStyleSheet(u"border-image: url(:/images/background.png);\n"
"border-radius:20px;")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 30, 300, 420))
        self.label_2.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.715909, stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), stop:0.835227 rgba(0, 0, 0, 75));\n"
"border-radius:20px;")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 60, 280, 390))
        self.label_3.setStyleSheet(u"background-color:rgba(0, 0, 0, 100);\n"
"border-radius:15px;")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(135, 95, 90, 40))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color:rgba(255, 255, 255, 210);")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(80, 165, 200, 40))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit.setFont(font1)
        self.lineEdit.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(80, 200, 200, 40))
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(80, 280, 200, 40))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton.setFont(font2)
        self.pushButton.setText(QCoreApplication.translate("Form", u"Log In", None))
        
        self.pushButton_r = QPushButton(self.widget)
        self.pushButton_r.setObjectName(u"pushButton_r")
        self.pushButton_r.setGeometry(QRect(80, 330, 200, 40))
        self.pushButton_r.setFont(font2)
        self.pushButton_r.setText(QCoreApplication.translate("Form", u"Sign In", None))
        
        
        self.horizontalLayoutWidget = QWidget(self.widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(105, 409, 141, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButton_pasw = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_pasw.setObjectName(u"pushButton_pasw")
        self.horizontalLayoutWidget.setGeometry(QRect(120, 370, 141, 31))
        font3 = QFont()
        font3.setFamilies([u"Social Media Circled"])
        font3.setPointSize(10)
        self.pushButton_pasw.setFont(font3)
        self.horizontalLayout.addWidget(self.pushButton_pasw)


        self.horizontalLayoutWidget2 = QWidget(self.widget)
        self.horizontalLayoutWidget2.setObjectName(u"horizontalLayoutWidget2")
        self.horizontalLayoutWidget2.setGeometry(QRect(120, 400, 141, 31))
        self.horizontalLayout2 = QHBoxLayout(self.horizontalLayoutWidget2)
        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(30, 30))

        font3 = QFont()
        font3.setFamilies([u"Social Media Circled"])
        font3.setPointSize(15)
        self.pushButton_2.setFont(font3)

        self.horizontalLayout2.addWidget(self.pushButton_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Log In", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"  User Name", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Form", u"  Password", None))
        self.pushButton_pasw.setText(QCoreApplication.translate("Form", u"Forgot Your Password ?", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Exit", None))

