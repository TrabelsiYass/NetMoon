from PySide6.QtWidgets import QDialog,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
import mysql.connector
class feedback_msg(QDialog):
    def __init__(self, id, parent=None):
        super(feedback_msg, self).__init__(parent)
        self.setWindowTitle("FeedBack")
        self.setGeometry(700, 300, 200, 100)
        self.setStyleSheet("background-color: black;")

        self.id = id

        layout = QVBoxLayout()

        self.label = QLabel(" You Can Type Your FeedBack Here : ",self)
        self.label.setStyleSheet("color : grey;")
        self.msg = QLineEdit(self)
        self.msg.setPlaceholderText("Feel Free To Message Us !")
        self.msg.setStyleSheet("background-color: grey;")
        self.msg.setPlaceholderText("Type your Message")
        self.submit = QPushButton("Submit",self)
        self.submit.setStyleSheet("background-color : grey;")
        layout.addWidget(self.label)
        layout.addWidget(self.msg)
        layout.addWidget(self.submit)

        self.setLayout(layout)

        self.submit.clicked.connect(self.rec)

    def rec(self):
        message = self.msg.text()
        if not message:
            QMessageBox.warning(None, "Input Error", "All fields are required!")
            return
        
        mydb = self.create_connection()
        cursor = mydb.cursor()
        cursor.execute('''
                INSERT INTO feedback (id_user,msg)
                VALUES (%s,%s)
            ''', (self.id,message))

            # Commit the transaction and close the connection
        mydb.commit()
        mydb.close()

        QMessageBox.information(None, "Feedback Success", "Thanks for your Feedback!")

        self.close()

        




    def create_connection(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="nmap"
            )
            return mydb
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            return None



