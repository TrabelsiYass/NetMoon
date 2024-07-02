from PySide6.QtCore import Qt, QTimer, QThread, Signal, Slot
from PySide6.QtWidgets import QToolButton, QLabel, QDialog, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen
import speedtest

class SpeedTestThread(QThread):
    result_ready = Signal(str)

    def __init__(self, device_ip, parent=None):
        super().__init__(parent)
        self.device_ip_1 = device_ip
        self.result = ""

    def run(self):
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000     # Convert to Mbps
        ping_latency = st.results.ping

        self.result = (
            f"Speed test results for {self.device_ip_1}:\n"
            f"Download speed: {download_speed:.2f} Mbps\n"
            f"Upload speed: {upload_speed:.2f} Mbps\n"
            f"Ping latency: {ping_latency} ms"
        )
        self.result_ready.emit(self.result)

class ResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.results = results
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Speed Test Results")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()

        result_label = QLabel(self.results, self)
        result_label.setStyleSheet("color: white; font-size: 14px;")
        result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(result_label)

        self.setLayout(layout)

    def closeEvent(self, event):
        if self.parent():
            self.parent().reset_loading()
        super().closeEvent(event)


class LoadingWidget(QDialog):
    def __init__(self,device_ip,parent=None):
        super().__init__(parent)
        self.init_ui()
        self.loading_progress = 0
        self.device_ip = device_ip
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.loading_speed = 50
        self.ring_count = 0
        self.ring_sizes = [280, 240, 200, 160, 120, 80, 40]
    
    def init_ui(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle("Loading Widget")
        self.setStyleSheet("background-color: black;")

        self.button = QToolButton(self)
        self.button.setText("Start")
        self.button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 18px;
            }
            QToolButton:hover {
                background-color: #555555;
            }
            QToolButton:pressed {
                background-color: #111111;
            }
        """)
        self.button.clicked.connect(self.start_loading)
        self.button.setGeometry(100, 100, 100, 40)

        self.loading_text = QLabel("Loading ...", self)
        self.loading_text.setStyleSheet("color: grey; font-size: 10px;")
        self.loading_text.setGeometry(100, 150, 100, 20)
        self.loading_text.hide()  # Initially hidden

    def start_loading(self):
        self.loading_progress = 0
        self.ring_count = 0
        self.loading_text.show()  # Show the loading text
        self.timer.start(self.loading_speed)
        self.update()

        self.speed_test_thread = SpeedTestThread(self.device_ip)
        self.speed_test_thread.result_ready.connect(self.handle_speed_test_result)
        self.speed_test_thread.start()

    @Slot(str)
    def handle_speed_test_result(self, result):
        self.speed_test_result = result
        self.timer.stop()
        self.loading_text.hide()  # Optionally hide the loading text when done
        self.show_speed_test_results()

    def update_progress(self):
        self.loading_progress += 1
        if self.loading_progress > 100:
            self.loading_progress = 0
            self.ring_count += 1
            if self.ring_count >= len(self.ring_sizes):
                self.ring_count = 0
        self.update()

    def show_speed_test_results(self):
        result_dialog = ResultDialog(self.speed_test_result, self)
        result_dialog.exec()

    def reset_loading(self):
        self.ring_count = 0
        self.loading_progress = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for i in range(self.ring_count + 1):
            pen = QPen(QColor(128, 128, 128))
            pen.setWidth(10)  # Set pen width for the arc
            painter.setPen(pen)
            size = self.ring_sizes[i % len(self.ring_sizes)]
            offset = (300 - size) // 2
            painter.drawArc(offset, offset, size, size, 90 * 16, int(3.6 * self.loading_progress) * 16)