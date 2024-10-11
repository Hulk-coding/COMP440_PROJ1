from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QDesktopWidget,
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from Database import Database


class Create(QWidget):
    def __init__(self):
        super().__init__()

        form_layout = QFormLayout()

        # First name (allow only letters and spaces)
        self.firstname_inp = QLineEdit()
        firstname_regex = QRegExp(r"^[a-zA-Z\s]+$")
        self.firstname_inp.setValidator(QRegExpValidator(firstname_regex))

        # Last name (allow only letters and spaces)
        self.lastname_inp = QLineEdit()
        lastname_regex = QRegExp(r"^[a-zA-Z\s]+$")
        self.lastname_inp.setValidator(QRegExpValidator(lastname_regex))

        # Email (simple email validation)
        self.email_inp = QLineEdit()
        email_regex = QRegExp(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        self.email_inp.setValidator(QRegExpValidator(email_regex))

        # Phone (allow digits, spaces, and some special characters)
        self.phone_inp = QLineEdit()
        phone_regex = QRegExp(r"^[\d\s\+\-\(\)]+$")
        self.phone_inp.setValidator(QRegExpValidator(phone_regex))

        # Username (allow letters, numbers, and underscores)
        self.username_inp = QLineEdit()
        username_regex = QRegExp(r"^[a-zA-Z0-9_]+$")
        self.username_inp.setValidator(QRegExpValidator(username_regex))

        # Password (at least 8 characters, including uppercase, lowercase, and numbers)
        self.password_inp = QLineEdit()
        self.password_inp.setEchoMode(QLineEdit.Password)
        password_regex = QRegExp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        self.password_inp.setValidator(QRegExpValidator(password_regex))

        form_layout.addRow("First name:", self.firstname_inp)
        form_layout.addRow("Last name:", self.lastname_inp)
        form_layout.addRow("Email:", self.email_inp)
        form_layout.addRow("Phone:", self.phone_inp)
        form_layout.addRow("Username:", self.username_inp)
        form_layout.addRow("Password:", self.password_inp)

        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_new_account)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.setAlignment(Qt.AlignCenter)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addLayout(form_layout)
        wrapper_layout.addLayout(button_layout)
        wrapper_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(wrapper_layout)

        self.setWindowTitle("Create New Account")

        self.setWindowFlags(Qt.Window)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_new_account(self):
        firstname = self.firstname_inp.text()
        lastname = self.lastname_inp.text()
        email = self.email_inp.text()
        phone = self.phone_inp.text()
        username = self.username_inp.text()
        password = self.password_inp.text()

        # Validate all fields before proceeding
        if not all([firstname, lastname, email, phone, username, password]):
            print("All fields must be filled")
            return

        # db = Database(
        #     host=,
        #     user=,
        #     password=,
        #     database=,
        # )

        # db.connect()
        # db.insert(firstname, lastname, email, phone, username, password)
        # db.close()

        self.close()
