from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
import mysql.connector
from modules.loginUi import Ui_Form  # Ensure this is the correct path to your UI file
from main import MainWindow  # Import the main application window

class MainWindow_login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.close)

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

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        mydb = self.create_connection()
        if not mydb:
            return

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}")
            self.id = int(user[0])
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def open_main_window(self):
        self.main_window = MainWindow(self.id)
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    login_window = MainWindow_login()
    login_window.setWindowFlag(Qt.FramelessWindowHint)
    login_window.setAttribute(Qt.WA_TranslucentBackground)
    login_window.show()
    app.exec()
