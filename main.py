import os
import sys

from modules.ui_functions import *
from QOS.speedtest_fn import LoadingWidget
from QOS.latency_fn import LatencyDialog

from modules.ui_main import Ui_MainWindow
from modules.ui_main_admin import Ui_MainWindow_admin
from PySide6.QtWidgets import QMainWindow,QApplication,QDialog,QMessageBox,QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from modules.functions import *
from PySide6.QtCore import QThread, Signal, QObject
from modules.loginUi import Ui_Form
from modules.register import Ui_RegisterForm
from modules.ui_splash import Ui_SplashScreen
from modules.password_mail import *
from modules.password_mail_admin import *
from QOS.loses import PingDialog
from modules.feedback import feedback_msg



os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%


widgets = None
counter = 0

class MainWindow_login_admin(QMainWindow):
    def __init__(self):
        super(MainWindow_login_admin,self).__init__()
        self.ui = Ui_Form()
        self.uii = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton_r.clicked.connect(self.show_register_form)
        self.ui.pushButton_pasw.clicked.connect(self.mail_verif)



    def mail_verif(self):
        mail = EmailVerificationDialog_admin(self)
        mail.show()



    def show_register_form(self):
        # Close the current window
        self.close()
        
        # Open the register window
        self.register_window = RegisterWindow_admin()
        self.register_window.setWindowFlag(Qt.FramelessWindowHint)
        self.register_window.setAttribute(Qt.WA_TranslucentBackground)
        self.register_window.show()
        
    
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
        admin = cursor.fetchone()

        if admin:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def open_main_window(self):
        self.main_window = SplashScreen_admin()
        self.main_window.show()
        self.close()



class RegisterWindow_admin(QMainWindow):
    def __init__(self):
        super(RegisterWindow_admin, self).__init__()
        self.ui = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.register)
        self.ui.pushButton_r.clicked.connect(self.show_login_form)
        self.ui.pushButton_2.clicked.connect(self.close)

    def register(self):
        pseudo = self.ui.lineEdit_pseudo.text()
        email = self.ui.lineEdit_email.text()
        password = self.ui.lineEdit_password.text()

        if not pseudo or not email or not password:
            QMessageBox.warning(None, "Input Error", "All fields are required!")
            return

        # Save to database
        try:
            # Connect to the database (creates the database file if it doesn't exist)
            mydb = create_connection()
            cursor = mydb.cursor()
            
            # Insert the user data
            cursor.execute('''
                INSERT INTO admin (username, email, password)
                VALUES (%s,%s,%s)
            ''', (pseudo, email, password))

            # Commit the transaction and close the connection
            mydb.commit()
            mydb.close()

            QMessageBox.information(None, "Registration Success", "User registered successfully!")

            # Clear the input fields after successful registration
            self.show_login_form()

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

    def show_login_form(self):
        # Close the current window
        self.close()

        # Open the login window
        self.login_window = MainWindow_login_admin()
        self.login_window.setWindowFlag(Qt.FramelessWindowHint)
        self.login_window.setAttribute(Qt.WA_TranslucentBackground)
        self.login_window.show()


class MainWindow_login(QMainWindow):
    def __init__(self):
        super(MainWindow_login,self).__init__()
        self.ui = Ui_Form()
        self.uii = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton_r.clicked.connect(self.show_register_form)
        self.ui.pushButton_pasw.clicked.connect(self.mail_verif)



    def mail_verif(self):
        mail = EmailVerificationDialog(self)
        mail.show()



    def show_register_form(self):
        # Close the current window
        self.close()
        
        # Open the register window
        self.register_window = RegisterWindow()
        self.register_window.setWindowFlag(Qt.FramelessWindowHint)
        self.register_window.setAttribute(Qt.WA_TranslucentBackground)
        self.register_window.show()
        
    
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
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}")
            self.id = int(user[0])
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def open_main_window(self):
        self.main_window = SplashScreen(self.id)
        self.main_window.show()
        self.close()

class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.ui = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.register)
        self.ui.pushButton_r.clicked.connect(self.show_login_form)
        self.ui.pushButton_2.clicked.connect(self.close)

    def register(self):
        pseudo = self.ui.lineEdit_pseudo.text()
        email = self.ui.lineEdit_email.text()
        password = self.ui.lineEdit_password.text()

        if not pseudo or not email or not password:
            QMessageBox.warning(None, "Input Error", "All fields are required!")
            return

        # Save to database
        try:
            # Connect to the database (creates the database file if it doesn't exist)
            mydb = create_connection()
            cursor = mydb.cursor()

            cursor.execute("SELECT MAX(Id_user) FROM users")
            self.id = cursor.fetchone()[0]

            if self.id is None:
                self.id = 1
            else:
                self.id = int(self.id) + 1
            
            # Insert the user data
            cursor.execute('''
                INSERT INTO users (Id_user,Username, email, Password)
                VALUES (%s,%s,%s,%s)
            ''', (self.id,pseudo, email, password))

            # Commit the transaction and close the connection
            mydb.commit()
            mydb.close()

            QMessageBox.information(None, "Registration Success", "Admin registered successfully!")

            # Clear the input fields after successful registration
            self.show_login_form()

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

    def show_login_form(self):
        # Close the current window
        self.close()

        # Open the login window
        self.login_window = MainWindow_login()
        self.login_window.setWindowFlag(Qt.FramelessWindowHint)
        self.login_window.setAttribute(Qt.WA_TranslucentBackground)
        self.login_window.show()




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
        exit_button = QPushButton('Exit', self)

        # Style the buttons with different QFont styles
        self.style_button(user_button, QFont('Arial', 14, QFont.Bold))  # Bold
        self.style_button(admin_button, QFont('Times New Roman', 16, QFont.DemiBold))  # DemiBold
        self.style_button(exit_button, QFont('Times New Roman', 16, QFont.DemiBold))  # DemiBold

        # Connect buttons to functions
        user_button.clicked.connect(self.open_login_window)
        admin_button.clicked.connect(self.open_admin_interface)
        exit_button.clicked.connect(self.exit_application)

        # Add widgets to layout
        layout.addWidget(user_button)
        layout.addWidget(admin_button)
        layout.addWidget(exit_button)

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
        # Close the current window
        self.close()

        # Open the login window
        self.login_window = MainWindow_login()
        self.login_window.setWindowFlag(Qt.FramelessWindowHint)
        self.login_window.setAttribute(Qt.WA_TranslucentBackground)
        self.login_window.show()

    def open_admin_interface(self):
        print("Administrator Interface button clicked")
        self.close()

        # Open the login window
        self.login_window = MainWindow_login_admin()
        self.login_window.setWindowFlag(Qt.FramelessWindowHint)
        self.login_window.setAttribute(Qt.WA_TranslucentBackground)
        self.login_window.show()

    def exit_application(self, event):
        QApplication.quit()


class NetworkScanWorker(QObject):
    finished = Signal(str)

    def __init__(self, text,id):
        super().__init__()
        self.text = text
        self.id = id

    def run(self):
        # Perform the network scan
        html_content = scan_press(self.id, self.text)
        # Emit the finished signal with the html_content
        self.finished.emit(html_content)


class NetworkScanWorker_admin(QObject):
    finished = Signal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        # Perform the network scan
        html_content = scan_press_admin(self.text)
        # Emit the finished signal with the html_content
        self.finished.emit(html_content)





class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Loading")
        layout = QVBoxLayout()
        self.loading_label = QLabel("Loading...", self)
        layout.addWidget(self.loading_label)
        self.setLayout(layout)



class NetworkDetailsDialog(QDialog):
    def __init__(self, html_content, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)
        self.webview.setHtml(html_content)
        self.setWindowTitle("Network Details")
        self.resize(400,600)


class NetworkDetailsDialog_admin(QDialog):
    def __init__(self, html_content, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)
        self.webview.setHtml(html_content)
        self.setWindowTitle("Network Details (Administrator)")
        self.resize(400,600)

class SplashScreen_admin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")
        QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.main = MainWindow_admin()
            self.main.show()
            self.close()
        counter += 1


class SplashScreen(QMainWindow):
    def __init__(self, id):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")
        QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        self.id = id
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.main = MainWindow(self.id)
            self.main.show()
            self.close()
        counter += 1

class MainWindow_admin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        self.ui = Ui_MainWindow_admin()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        title = "NETMOON"
        # APPLY TEXTS
        self.setWindowTitle(title)

        # TOGGLE MENU
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)
        self.slider = self.ui.slider
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        
        # BUTTONS CLICK
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_scan.clicked.connect(self.buttonClick)
        widgets.btn_baudrate.clicked.connect(self.buttonClick)
        widgets.btn_latency.clicked.connect(self.buttonClick)
        widgets.btn_more.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)
        widgets.btn_more.clicked.connect(self.buttonClick)
        widgets.btn_message.clicked.connect(self.buttonClick)
        widgets.btn_logout.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        self.show()

        # SET CUSTOM THEME
        
        self.themeFile = "themes\Light_Monitoring_style.qss"
        UIFunctions.theme(self, self.themeFile, True)
        AppFunctions.setThemeHack(self)
        self.ui.btn_style.clicked.connect(self.themechanger)




        # SET HOME PAGE AND SELECT MENU
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        self.ui.list_users.cellClicked.connect(self.populate_second_table)

        


    def themechanger(self):
        if self.themeFile == "themes\Dark_Monitoring_style.qss" :
            UIFunctions.theme(self, "themes\Light_Monitoring_style.qss", True)
            AppFunctions.setThemeHack(self)
        else :
            UIFunctions.theme(self, "themes\Dark_Monitoring_style.qss", True)
            AppFunctions.setThemeHack(self)



    # BUTTONS CLICK
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            table_feedback = self.ui.list_feedback
            populate_table_feedback(table_feedback)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            self.ui.scan_button.clicked.connect(self.start)
            
        if btnName == "btn_scan":
            widgets.stackedWidget.setCurrentWidget(widgets.scan_page)
            table = self.ui.list_admins
            table_users = self.ui.list_users
            populate_table_users(table_users)
            populate_table_admin(table)
            UIFunctions.resetStyle(self, btnName)
            self.ui.schema_button.clicked.connect(self.popup_network)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_baudrate":
            row = self.ui.list_devices.currentRow()
            try :
                device_ip = self.ui.list_devices.item(row,1).text()
                self.loading_widget = LoadingWidget(device_ip , self)
                self.loading_widget.show()
            except :
                QMessageBox.warning(None, "Error !", "Select a device ip adress")

        if btnName == "btn_latency":
            row = self.ui.list_devices.currentRow()
            if row == -1:
                QMessageBox.warning(self, "Warning", "No device selected!")
                return

            try:
                device_ip_item = self.ui.list_devices.item(row, 1)
                device_services_item = self.ui.list_devices.item(row, 3)

                if not device_ip_item or not device_services_item:
                    QMessageBox.warning(self, "Warning", "Selected row does not contain valid data!")
                    return

                device_ip = device_ip_item.text()
                device_services = device_services_item.text()

                try:
                    # Try to convert the string to a dictionary using json.loads for safety
                    import json
                    device_services_dict = json.loads(device_services)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to eval but print a warning
                    print("Warning: Falling back to eval. Ensure the string is safe to evaluate.")
                    device_services_dict = eval(device_services)

                if 'tcp' not in device_services_dict:
                    QMessageBox.warning(self, "Warning", "Device services do not contain 'tcp' key!")
                    return

                device_ports = list(device_services_dict['tcp'].keys())
                if not device_ports:
                    QMessageBox.warning(self, "Warning", "No TCP ports found in device services!")
                    return

                device_port = int(device_ports[0])

                self.latency_widget = LatencyDialog(device_ip, device_port)
                self.latency_widget.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")


        if btnName == "btn_more":
            row = self.ui.list_devices.currentRow()
            if row == -1:
                QMessageBox.warning(self, "Warning", "No device selected!")
                return

            try:
                device_ip_item = self.ui.list_devices.item(row, 1)

                if not device_ip_item:
                    QMessageBox.warning(self, "Warning", "Selected row does not contain valid data!")
                    return

                device_ip = device_ip_item.text()
                self.ping_widget = PingDialog(device_ip)
                self.ping_widget.show()
            except Exception as e:
                QMessageBox.warning(self, "Error!", f"Failed to create PingDialog: {e}")



            
        if btnName =="btn_exit":
            QApplication.quit()


        if btnName == "btn_message":
            self.reclamation = feedback_msg(1)
            self.reclamation.show()

        if btnName == "btn_logout":
            self.close()
            self.login_window = MainWindow_login()
            self.login_window.setWindowFlag(Qt.FramelessWindowHint)
            self.login_window.setAttribute(Qt.WA_TranslucentBackground)
            self.login_window.show()

    def start(self):
            self.slider_start()
            self.start_network_scan()


    def slider_start(self):
            # Set up timer to update the slider progress
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateSliderProgress)
            self.slider.setValue(0)
            self.timer.start(100)


    def updateSliderProgress(self):
            # Increment the slider value
            current_value = self.slider.value()
            max_value = self.slider.maximum()
            if current_value < max_value:
                self.slider.setValue(current_value + 1)
            else:
                self.slider.setValue(0)


    def start_network_scan(self):
                self.text = self.ui.input_field.text()
                self.thread = QThread()
                self.worker = NetworkScanWorker_admin(self.text)
                self.worker.moveToThread(self.thread)

                # Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.show_network_scan_results)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                # Start the thread
                self.thread.start()

    def show_network_scan_results(self, html_content):
            self.timer.stop()
            self.slider.setValue(0)

            dialog = NetworkDetailsDialog(html_content, self)
            dialog.show()




    def merged_list(self):
            selected_rows = self.ui.list_widget.selectedItems()
            area_ids = [int(item.text()) for item in selected_rows if item.column() == 1]

            if len(area_ids) < 2 :
                QMessageBox.warning(None, "ERROR !", "Your need to select atleast two area ID's", QMessageBox.Cancel)
            else:
                populate_fourth_table(area_ids,self.ui.list_merged)



    def populate_second_table(self):
            row = self.ui.list_users.currentRow()
            username = self.ui.list_users.item(row, 0).text()
            populate_second_table_admin(username,self.ui.list_scans)
            widgets.delete_button.clicked.connect(self.delete_user)


    def delete_user(self):
        # Get the selected row
        selected_row = self.ui.list_users.currentRow()
        if selected_row < 0:
            return  QMessageBox.warning(self, "Error!", f"Select a User to Delete")


        # Get the username from the selected row
        username = self.ui.list_users.item(selected_row, 0).text()

        # Delete the user from the database
        mydb = self.create_connection()
        if not mydb:
            return

        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        mydb.commit()
        mydb.close()

        # Remove the row from the table
        self.ui.list_users.removeRow(selected_row)

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

    def populate_third_table(self):
            row = self.ui.list_scans.currentRow()
            scan_id = self.ui.list_scans.item(row,0).text()
            populate_third_table(scan_id,self.ui.list_devices)
            self.ui.list_devices.resizeColumnsToContents()

    def getting_device_ip(self):
            row = self.ui.list_devices.currentRow()
            device_ip = self.ui.list_devices.item(row,0).text()
            

    def popup_network(self):
            selected_rows = self.ui.list_scans.selectedItems()
            scan_ids = [int(item.text()) for item in selected_rows if item.column() == 0]

            if len(scan_ids) == 1:
                merged_network = getting_network_one_id(scan_ids[0])
            else:
                merged_network = getting_network_multiple(scan_ids)

            dialog = NetworkDetailsDialog_admin(merged_network, self)
            dialog.exec()


    def popup_area(self):
            selected_rows = self.ui.list_widget.selectedItems()
            area_ids = [int(item.text()) for item in selected_rows if item.column() == 1]

            if len(area_ids) == 1:
                merged_network = getting_network_one_id_area(area_ids[0])
            else:
                merged_network = getting_network_multiple_area(area_ids)

            dialog = NetworkDetailsDialog(merged_network, self)
            dialog.exec()

            


class MainWindow(QMainWindow):
    def __init__(self,id):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.id = id

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        title = "NETMOON"
        # APPLY TEXTS
        self.setWindowTitle(title)

        # TOGGLE MENU
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)
        self.slider = self.ui.slider
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        
        # BUTTONS CLICK
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_scan.clicked.connect(self.buttonClick)
        widgets.btn_baudrate.clicked.connect(self.buttonClick)
        widgets.btn_latency.clicked.connect(self.buttonClick)
        widgets.btn_more.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)
        widgets.btn_more.clicked.connect(self.buttonClick)
        widgets.btn_message.clicked.connect(self.buttonClick)
        widgets.btn_logout.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        self.ui.button4.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        self.show()

        # SET CUSTOM THEME
        
        self.themeFile = "themes\Light_Monitoring_style.qss"
        UIFunctions.theme(self, self.themeFile, True)
        AppFunctions.setThemeHack(self)
        self.ui.btn_style.clicked.connect(self.themechanger)




        # SET HOME PAGE AND SELECT MENU
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        
        self.ui.list_widget.cellClicked.connect(self.populate_second_table)
        self.ui.list_scans.cellClicked.connect(self.populate_third_table)
        self.ui.button3.clicked.connect(self.merged_list)
        self.ui.button2.clicked.connect(self.popup_network)
        self.ui.button1.clicked.connect(self.popup_area)


    def themechanger(self):
        if self.themeFile == "themes\Dark_Monitoring_style.qss" :
            UIFunctions.theme(self, "themes\Light_Monitoring_style.qss", True)
            AppFunctions.setThemeHack(self)
        else :
            UIFunctions.theme(self, "themes\Dark_Monitoring_style.qss", True)
            AppFunctions.setThemeHack(self)



    # BUTTONS CLICK
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            self.ui.scan_button.clicked.connect(self.start)
            
        if btnName == "btn_scan":
            widgets.stackedWidget.setCurrentWidget(widgets.scan_page)
            table = self.ui.list_widget
            table = populate_table(1,table)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_baudrate":
            row = self.ui.list_devices.currentRow()
            try :
                device_ip = self.ui.list_devices.item(row,1).text()
                self.loading_widget = LoadingWidget(device_ip , self)
                self.loading_widget.show()
            except :
                QMessageBox.warning(None, "Error !", "Select a device ip adress")

        if btnName == "btn_latency":
            row = self.ui.list_devices.currentRow()
            if row == -1:
                QMessageBox.warning(self, "Warning", "No device selected!")
                return

            try:
                device_ip_item = self.ui.list_devices.item(row, 1)
                device_services_item = self.ui.list_devices.item(row, 3)

                if not device_ip_item or not device_services_item:
                    QMessageBox.warning(self, "Warning", "Selected row does not contain valid data!")
                    return

                device_ip = device_ip_item.text()
                device_services = device_services_item.text()

                try:
                    # Try to convert the string to a dictionary using json.loads for safety
                    import json
                    device_services_dict = json.loads(device_services)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to eval but print a warning
                    print("Warning: Falling back to eval. Ensure the string is safe to evaluate.")
                    device_services_dict = eval(device_services)

                if 'tcp' not in device_services_dict:
                    QMessageBox.warning(self, "Warning", "Device services do not contain 'tcp' key!")
                    return

                device_ports = list(device_services_dict['tcp'].keys())
                if not device_ports:
                    QMessageBox.warning(self, "Warning", "No TCP ports found in device services!")
                    return

                device_port = int(device_ports[0])

                self.latency_widget = LatencyDialog(device_ip, device_port)
                self.latency_widget.show()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        if btnName == "btn_more":
            row = self.ui.list_devices.currentRow()
            if row == -1:
                QMessageBox.warning(self, "Warning", "No device selected!")
                return

            try:
                device_ip_item = self.ui.list_devices.item(row, 1)

                if not device_ip_item:
                    QMessageBox.warning(self, "Warning", "Selected row does not contain valid data!")
                    return

                device_ip = device_ip_item.text()
                self.ping_widget = PingDialog(device_ip)
                self.ping_widget.show()
            except Exception as e:
                QMessageBox.warning(self, "Error!", f"Failed to create PingDialog: {e}")



            
        if btnName =="btn_exit":
            QApplication.quit()


        if btnName == "btn_message":
            self.reclamation = feedback_msg(self.id)
            self.reclamation.show()

        if btnName == "btn_logout":
            self.close()
            self.login_window = MainWindow_login()
            self.login_window.setWindowFlag(Qt.FramelessWindowHint)
            self.login_window.setAttribute(Qt.WA_TranslucentBackground)
            self.login_window.show()
            

            

            
        

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def start(self):
            self.slider_start()
            self.start_network_scan()



    def slider_start(self):
            # Set up timer to update the slider progress
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateSliderProgress)
            self.slider.setValue(0)
            self.timer.start(100)


    def updateSliderProgress(self):
            # Increment the slider value
            current_value = self.slider.value()
            max_value = self.slider.maximum()
            if current_value < max_value:
                self.slider.setValue(current_value + 1)
            else:
                self.slider.setValue(0)


    def start_network_scan(self):
                self.text = self.ui.input_field.text()
                self.thread = QThread()
                self.worker = NetworkScanWorker(self.text,self.id)
                self.worker.moveToThread(self.thread)

                # Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.show_network_scan_results)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                # Start the thread
                self.thread.start()

    def show_network_scan_results(self, html_content):
            self.timer.stop()
            self.slider.setValue(0)

            dialog = NetworkDetailsDialog(html_content, self)
            dialog.show()




    def merged_list(self):
            selected_rows = self.ui.list_widget.selectedItems()
            area_ids = [int(item.text()) for item in selected_rows if item.column() == 1]

            if len(area_ids) < 2 :
                QMessageBox.warning(None, "ERROR !", "Your need to select atleast two area ID's", QMessageBox.Cancel)
            else:
                populate_fourth_table(area_ids,self.ui.list_merged)



    def populate_second_table(self):
            row = self.ui.list_widget.currentRow()
            scan_id = self.ui.list_widget.item(row, 1).text()
            populate_second_table(scan_id,self.ui.list_scans)


    def populate_third_table(self):
            row = self.ui.list_scans.currentRow()
            scan_id = self.ui.list_scans.item(row,0).text()
            populate_third_table(scan_id,self.ui.list_devices)
            self.ui.list_devices.resizeColumnsToContents()

    def getting_device_ip(self):
            row = self.ui.list_devices.currentRow()
            device_ip = self.ui.list_devices.item(row,0).text()
            

    def popup_network(self):
            selected_rows = self.ui.list_scans.selectedItems()
            scan_ids = [int(item.text()) for item in selected_rows if item.column() == 0]

            if len(scan_ids) == 1:
                merged_network = getting_network_one_id(scan_ids[0])
            else:
                merged_network = getting_network_multiple(scan_ids)

            dialog = NetworkDetailsDialog(merged_network, self)
            dialog.exec()


    def popup_area(self):
            selected_rows = self.ui.list_widget.selectedItems()
            area_ids = [int(item.text()) for item in selected_rows if item.column() == 1]

            if len(area_ids) == 1:
                merged_network = getting_network_one_id_area(area_ids[0])
            else:
                merged_network = getting_network_multiple_area(area_ids)

            dialog = NetworkDetailsDialog(merged_network, self)
            dialog.exec()




def main():
    app = QApplication(sys.argv)
    selector = InterfaceSelector()
    selector.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
