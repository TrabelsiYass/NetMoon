import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication, QMessageBox
from main import MainWindow_login, RegisterWindow

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    main_window = MainWindow_login()
    qtbot.addWidget(main_window)
    return main_window

def test_login_success(app, qtbot):
    with patch('main.mysql.connector.connect') as mock_connect:
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1, 'test_user', 'test_password']

        app.ui.lineEdit.setText('test_user')
        app.ui.lineEdit_2.setText('test_password')

        with qtbot.waitSignal(QMessageBox.information, timeout=1000) as blocker:
            app.login()
        assert "Login Successful" in blocker.args[0].text()

def test_login_failure(app, qtbot):
    with patch('main.mysql.connector.connect') as mock_connect:
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        app.ui.lineEdit.setText('wrong_user')
        app.ui.lineEdit_2.setText('wrong_password')

        with qtbot.waitSignal(QMessageBox.warning, timeout=1000) as blocker:
            app.login()
        assert "Login Failed" in blocker.args[0].text()

def test_register_success(qtbot):
    app = RegisterWindow()
    qtbot.addWidget(app)

    with patch('main.create_connection') as mock_create_connection:
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [(None,), (1,)]

        app.ui.lineEdit_pseudo.setText('new_user')
        app.ui.lineEdit_email.setText('new_user@example.com')
        app.ui.lineEdit_password.setText('new_password')

        with qtbot.waitSignal(QMessageBox.information, timeout=1000) as blocker:
            app.register()
        assert "Registration Success" in blocker.args[0].text()

def test_register_failure(qtbot):
    app = RegisterWindow()
    qtbot.addWidget(app)

    with patch('main.create_connection') as mock_create_connection:
        mock_create_connection.side_effect = Exception('Database error')

        app.ui.lineEdit_pseudo.setText('new_user')
        app.ui.lineEdit_email.setText('new_user@example.com')
        app.ui.lineEdit_password.setText('new_password')

        with qtbot.waitSignal(QMessageBox.critical, timeout=1000) as blocker:
            app.register()
        assert "Database Error" in blocker.args[0].text()
