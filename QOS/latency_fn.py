import socket
import time
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class LatencyDialog(QDialog):
    def __init__(self, address_ip, port, parent=None):
        super(LatencyDialog, self).__init__(parent)
        self.setWindowTitle("Latency Result")
        self.setGeometry(700, 300, 200, 100)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        # Calculate latency
        latency = self.calculate_tcp_latency(address_ip, port)
        if latency is not None:
            self.label = QLabel(f"Latency: {latency:.2f} ms", self)
        else:
            self.label = QLabel("Latency calculation failed.", self)

        layout.addWidget(self.label)
        self.label.setStyleSheet("color: grey;")

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("border: 2px solid rgb(52, 59, 72);\n"
                                     "border-radius: 5px;\n"
                                     "background-color: rgb(52, 59, 72);\n")
        self.ok_button.clicked.connect(self.accept)  # Use accept() to close the dialog
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def calculate_tcp_latency(self, target_ip, target_port):
        try:
            # Create a TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(3)  # Set a timeout for the connection attempt

            start_time = time.time()

            # Connect to the target device
            client_socket.connect((target_ip, target_port))

            # Measure the time taken to establish the connection
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Close the socket
            client_socket.close()

            return latency
        except Exception as e:
            print(f"Error occurred: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            return None
