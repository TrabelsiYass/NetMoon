from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtCore import QSize, QRect, QCoreApplication, QMetaObject
from PySide6.QtGui import QFont

class Ui_RegisterForm(object):
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
"QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5{	\n"
"	background-color: rgba(0, 0, 0, 0);\n"
"	color:rgba(85, 98, 112, 255);\n"
"}\n"
"QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover{	\n"
"	color:rgba(155, 168, 182, 220);\n"
"}\n"
"QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed{	\n"
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
        font1 = QFont()
        font1.setPointSize(10)
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
        self.lineEdit_fullname = QLineEdit(self.widget)
        self.lineEdit_fullname.setObjectName(u"lineEdit_fullname")
        self.lineEdit_fullname.setGeometry(QRect(80, 130, 200, 40))
        self.lineEdit_fullname.setFont(font1)
        self.lineEdit_fullname.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        
        self.lineEdit_pseudo = QLineEdit(self.widget)
        self.lineEdit_pseudo.setObjectName(u"lineEdit_pseudo")
        self.lineEdit_pseudo.setGeometry(QRect(80, 165, 200, 40))
        self.lineEdit_pseudo.setFont(font1)
        self.lineEdit_pseudo.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        
        self.lineEdit_email = QLineEdit(self.widget)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setGeometry(QRect(80, 200, 200, 40))
        self.lineEdit_email.setFont(font1)
        self.lineEdit_email.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        
        self.lineEdit_password = QLineEdit(self.widget)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setGeometry(QRect(80, 235, 200, 40))
        self.lineEdit_password.setFont(font1)
        self.lineEdit_password.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(80, 280, 200, 40))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton.setFont(font2)
        self.pushButton.setText(QCoreApplication.translate("Form", u"Sign In", None))

        label_5 = QLabel(self.widget)
        label_5.setObjectName(u"label_5")
        label_5.setGeometry(QRect(91, 370, 191, 21))
        label_5.setStyleSheet(u"color:rgba(255, 255, 255, 140);")

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(30, 30))
        self.pushButton_2.setGeometry(QRect(160, 410, 200, 40))
        font3 = QFont()
        font3.setFamilies([u"Social Media Circled"])
        font3.setPointSize(15)
        self.pushButton_2.setFont(font3)

        
        pushButton_r = QPushButton(self.widget)
        pushButton_r.setObjectName(u"pushButton_r")
        pushButton_r.setGeometry(QRect(80, 330, 200, 40))
        pushButton_r.setFont(font2)
        pushButton_r.setText(QCoreApplication.translate("Form", u"Log In", None))

        self.label_5 = label_5
        self.pushButton_r = pushButton_r

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
                self.label.setText("")
                self.label_2.setText("")
                self.label_3.setText("")
                self.label_4.setText(QCoreApplication.translate("Form", u"Sign In", None))
                self.lineEdit_fullname.setPlaceholderText(QCoreApplication.translate("Form", u"  Full Name", None))
                self.lineEdit_pseudo.setPlaceholderText(QCoreApplication.translate("Form", u"  Pseudo", None))
                self.lineEdit_email.setPlaceholderText(QCoreApplication.translate("Form", u"  Email", None))
                self.lineEdit_password.setPlaceholderText(QCoreApplication.translate("Form", u"  Password", None))
                self.label_5.setText(QCoreApplication.translate("Form", u"You have an Account ? Log in", None))
                self.pushButton_2.setText(QCoreApplication.translate("Form", u"Exit", None))
