import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PySide6.QtCore import Qt
from pythonping import ping

class PingDialog(QDialog):
    def __init__(self, ip):
        super().__init__()
        self.setWindowTitle("Ping IP Address")
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("background-color: black;")

        
        # Layout
        self.layout = QVBoxLayout()

        # IP Label
        self.ip_label = QLabel(f"IP Address: {ip}", self)
        self.ip_label.setStyleSheet("color: grey;")

        self.ip_label.setAlignment(Qt.AlignCenter)
        
        # Ping Button
        self.ping_button = QPushButton("Ping")
        self.ping_button.setStyleSheet("background-color : grey;")
        self.ping_button.clicked.connect(self.ping_ip)

        # Result Label
        self.result_label = QLabel("", self)
        self.result_label.setStyleSheet("color:grey;")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        # Adding widgets to layout
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ping_button)
        self.layout.addWidget(self.result_label)
        
        self.setLayout(self.layout)
        
        # Store the IP address
        self.ip_address = ip

    def ping_ip(self):
        ip_address = self.ip_address
        if not ip_address:
            QMessageBox.warning(self, "Input Error", "Please enter a valid IP address.")
            return
        
        try:
            response_list = ping(ip_address, count=4, timeout=2)
            sent_packets = len(response_list)
            received_packets = len([response for response in response_list if response.success])
            lost_packets = sent_packets - received_packets
            packet_loss_percentage = (lost_packets / sent_packets) * 100

            result_text = (f"--- {ip_address} ping statistics ---\n"
                           f"{sent_packets} packets transmitted, "
                           f"{received_packets} packets received, "
                           f"{packet_loss_percentage:.1f}% packet loss")
            self.result_label.setText(result_text)
        except Exception as e:
            QMessageBox.critical(self, "Ping Error", str(e))

