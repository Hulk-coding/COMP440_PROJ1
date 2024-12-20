import bcrypt, re
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QDesktopWidget,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QColor
from Database import Database
from Tools import Tools


class Create(QWidget):
    def __init__(self, parent_position=None):
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
        # password_regex = QRegExp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        # self.password_inp.setValidator(QRegExpValidator(password_regex))
        self.password_inp.textChanged.connect(self.check_password_strength)

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


        self.tools = Tools()  # Create an instance of Tools

    def center(self, parent_position = None):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        cp = parent_position
        qr.moveCenter(cp)
        self.move(qr.topLeft())
       

    def check_password_strength(self):
        password = self.password_inp.text()
        strength = 0
        suggestions = []

        if len(password) >= 8:
            strength += 1
        else:
            suggestions.append("Use at least 8 characters")
        if re.search(r"[A-Z]", password):
            strength += 1
        else:
            suggestions.append("Include at least one uppercase letter")

        if re.search(r"[a-z]", password):
            strength += 1
        else:
            suggestions.append("Include at least one lowercase letter")

        if re.search(r"\d", password):
            strength += 1
        else:
            suggestions.append("Include at least one number")

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1
        else:
            suggestions.append("Include at least one special character")

        # Set color based on password strength
        if strength < 2:
            color = QColor(255, 0, 0)  # Red
        elif strength < 4:
            color = QColor(255, 165, 0)  # Orange
        else:
            color = QColor(0, 255, 0)  # Green

        self.password_inp.setStyleSheet(
            f"QLineEdit {{ background-color: {color.name()}; }}"
        )

        if suggestions:
            tooltip = "Password should:\n" + "\n".join(suggestions)
            self.password_inp.setToolTip(tooltip)
        else:
            self.password_inp.setToolTip("Strong password")

    def create_new_account(self):
        firstname = self.firstname_inp.text()
        lastname = self.lastname_inp.text()
        email = self.email_inp.text()
        phone = self.phone_inp.text()
        username = self.username_inp.text()
        password = self.password_inp.text()

        # Check password strength before proceeding
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ):
            QMessageBox.warning(
                self,
                "Weak Password",
                "Please choose a stronger password. It should be at least 8 characters long and include uppercase, lowercase, numbers, and special characters.",
            )
            return

        # Validate all fields before proceeding
        if not all([firstname, lastname, email, phone, username, password]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Here we can store the user information in our database
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="CS440_DB_DESIGN",
        )
        # db.connect()

         ###Martin's connection
        # db = Database(
        #     host="localhost",
        #     user="admin_user",
        #     password="CS440Database",
        #     database="COMP440_Fall2024_DB",
        # )
        db.connect()
        if db.insert_new_user(firstname, lastname, email, phone, username, hashed_password):
            QMessageBox.information(self, "SUCCESS", "Account Created Successfully.")
        db.close()
     
        self.clear_all_fields()
        # Close the window after the account creation
        self.close()

    def clear_all_fields(self):
        # Clear the form fields after submission
        self.tools.clear_form_fields(
            self.firstname_inp,
            self.lastname_inp,
            self.email_inp,
            self.phone_inp,
            self.username_inp,
            self.password_inp,
        )

    def closeEvent(self, event):
        # When the widget is about to be closed, clear the form fields before closing
        self.clear_all_fields()
        event.accept()
