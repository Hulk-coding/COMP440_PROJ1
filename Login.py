import bcrypt
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QDesktopWidget,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from Create import Create


class Login(QWidget):
    def __init__(self):
        super().__init__()

        # labels for input
        userName = QLabel("Username")
        userPassword = QLabel("Password")

        # loading stylesheet
        self.loadStylesheet("StyleSheet.qss")

        # labels for input
        self.userName = QLabel("Username:")
        self.userPassword = QLabel("Password:")

        self.userNameIn = QLineEdit()
        self.userPasswordIn = QLineEdit()
        self.userPasswordIn.setEchoMode(QLineEdit.Password)

        self.userName.setFixedWidth(80)
        self.userPassword.setFixedWidth(80)
        self.userNameIn.setFixedWidth(200)
        self.userNameIn.setObjectName("QLineEdit")
        self.userPasswordIn.setFixedWidth(200)
        self.userPasswordIn.setObjectName("QLineEdit")

        # buttons for login page - greg edited
        self.loginButton = QPushButton(" Login ", self)
        self.createAccountButton = QPushButton(" Create Account ", self)

        # Connect login button to login function
        self.loginButton.clicked.connect(self.login)
        # greg added function
        self.createAccountButton.clicked.connect(self.open_create_window)

        # adding style elements
        self.loginButton.setObjectName("QButton")
        self.createAccountButton.setObjectName("QButton")

        # formatting page, creating layouts for the components
        pageLayout = QFormLayout()

        # layout for username input
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.userName)
        inputLayout.addWidget(self.userNameIn)
        inputLayout.setSpacing(10)
        inputLayout.setAlignment(Qt.AlignCenter)

        # layout for password input
        inputLayout2 = QHBoxLayout()
        inputLayout2.addWidget(self.userPassword)
        inputLayout2.addWidget(self.userPasswordIn)
        inputLayout2.setSpacing(10)
        inputLayout2.setAlignment(Qt.AlignCenter)

        # greg edit - add self
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.loginButton)
        buttonsLayout.addWidget(self.createAccountButton)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(80)
        buttonsLayout.setAlignment(Qt.AlignCenter)

        pageLayout.addRow(inputLayout)
        pageLayout.addRow(inputLayout2)
        pageLayout.addRow(buttonsLayout)
        pageLayout.setVerticalSpacing(50)

        # self.setStyleSheet("QWidget { border: 2px solid black; padding; 10px;") # this is not doing anything visible

        # pageLayout.setAlignment(Qt.AlignCenter)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(pageLayout)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        # self.setWindowTitle("Login")
        self.setWindowFlags(Qt.Window)

        # self.center()

    # greg added create function
    def open_create_window(self):
        self.create_window = Create()
        self.create_window.show()

    def loadStylesheet(self, filename):
        try:
            with open(filename, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def login(self):
        username = self.userNameIn.text()
        password = self.userPasswordIn.text()

        # Here we would typically fetch the stored hashed password from database
        # Here I have put a dummy hashed password
        # It should be replaced with a database query
        stored_hashed_password = (
            b"$2b$12$9vXLlX6X6X6X6X6X6X6X6uX6X6X6X6X6X6X6X6X6X6X6X6X6X6X6X6"
        )

        if self.check_password(password, stored_hashed_password):
            QMessageBox.information(
                self, "Login Successful", "You have successfully logged in!"
            )
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
