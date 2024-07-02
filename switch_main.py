from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PySide6.QtGui import QFont
import sys
from PySide6.QtCore import Qt
from main import MainWindow_login  # Importing the login window from main

class InterfaceSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('Interface Selector')
        self.setStyleSheet("background-color:black;")
        
        # Hide the title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window size
        self.setGeometry(700, 300, 500, 400)

        # Set layout
        layout = QVBoxLayout()

        # Create buttons
        user_button = QPushButton('User Interface', self)
        admin_button = QPushButton('Administrator Interface', self)

        # Style the buttons with different QFont styles
        self.style_button(user_button, QFont('Arial', 14, QFont.Bold))  # Bold
        self.style_button(admin_button, QFont('Times New Roman', 16, QFont.DemiBold))  # DemiBold

        # Connect buttons to functions
        user_button.clicked.connect(self.open_login_window)
        admin_button.clicked.connect(self.open_admin_interface)

        # Add widgets to layout
        layout.addWidget(user_button)
        layout.addWidget(admin_button)

        # Set layout for the main window
        self.setLayout(layout)

    def style_button(self, button, font):
        button.setFont(font)
        button.setFixedSize(500, 70)  # Increase button size
        button.setStyleSheet("""
            QPushButton {
                background-color: #741B97;
                color: white;
                border: none;
                padding: 15px;
                text-align: center;
                text-decoration: none;
                margin: 10px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #CC1EA0;
            }
        """)

    def open_login_window(self):
        print("Login Window button clicked")
        # Open the login window
        login_window = MainWindow_login()
        login_window.setWindowFlag(Qt.FramelessWindowHint)
        login_window.setAttribute(Qt.WA_TranslucentBackground)
        login_window.show()

    def open_admin_interface(self):
        print("Administrator Interface button clicked")
        # Here you can add the code to open the admin interface

    def exit_application(self, event):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    selector = InterfaceSelector()
    selector.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
