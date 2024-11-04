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
from Database import Database
from Tools import Tools
from Rentals import Rentals


class Login(QWidget):
    def __init__(self):
        super().__init__()

        # loading stylesheet
        # self.loadStylesheet("StyleSheet.qss")

        # labels for input
        userName = QLabel("Username")
        userPassword = QLabel("Password")

        # labels for input
        self.welcomePage = QLabel("Welcome!")
        self.welcomePage.setObjectName("welcomeLabel")

        self.userName = QLabel("Username:")
        self.userPassword = QLabel("Password:")
        self.userName.setObjectName("labels")
        self.userPassword.setObjectName("labels")

        self.welcomeSign = QLineEdit()
        self.welcomePage.setFixedWidth(200)

        self.userNameIn = QLineEdit()
        self.userPasswordIn = QLineEdit()
        self.userPasswordIn.setEchoMode(QLineEdit.Password)

        self.userName.setFixedWidth(80)
        self.userPassword.setFixedWidth(80)
        self.userNameIn.setFixedWidth(200)
        self.userNameIn.setObjectName("userNameIn")
        self.userPasswordIn.setFixedWidth(200)
        self.userPasswordIn.setObjectName("userPasswordIn")

        # buttons for login page - greg edited
        self.loginButton = QPushButton(" Login ", self)
        self.createAccountButton = QPushButton(" Create Account ", self)

        # test button
        # self.testButton = QPushButton(" test ", self)

        # Connect login button to login function
        self.loginButton.clicked.connect(self.login)
        # greg added function
        self.createAccountButton.clicked.connect(self.open_create_window)

        # self.testButton.clicked.connect(self.showRentalsWindow)

        # adding style elements
        self.loginButton.setObjectName("loginButton")
        self.createAccountButton.setObjectName("createAccountButton")

        # formatting page, creating layouts for the components
        pageLayout = QFormLayout()

        # layout for welcome sign
        welcomeLayout = QFormLayout()
        welcomeLayout.addWidget(self.welcomePage)
        welcomeLayout.setAlignment(Qt.AlignCenter)

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

        # Apply border to the inputContainer widget (can be styled in QSS)
        # inputContainer.setStyleSheet("QWidget { border: 2px solid black; padding: 10px; }")

        # Apply border to the inputContainer widget (can be styled in QSS)
        # inputContainer.setStyleSheet("QWidget { border: 2px solid black; padding: 10px; }")

        # greg edit - add self
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.loginButton)
        buttonsLayout.addWidget(self.createAccountButton)
        # buttonsLayout.addWidget(self.testButton)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(80)
        buttonsLayout.setAlignment(Qt.AlignCenter)

        # Create a QWidget to contain both input layouts
        inputContainer = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addLayout(inputLayout)
        containerLayout.addLayout(inputLayout2)
        containerLayout.addLayout(buttonsLayout)
        inputContainer.setFixedSize(500, 300)
        inputContainer.setLayout(containerLayout)
        inputContainer.setObjectName("inputContainer")

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(welcomeLayout)
        mainLayout.addWidget(inputContainer, alignment=Qt.AlignCenter)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        self.setWindowFlags(Qt.Window)

    # greg added create function
    def open_create_window(self):
        self.create_window = Create(self.frameGeometry().center())
        self.create_window.setFixedSize(400, 300)

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
        hash_pass = self.hash_password(password)

        if self.get_password(username, password):
            QMessageBox.information(
                self, "Login Successful", "You have successfully logged in!"
            )
            self.clear_all_fields(username, password)
            self.showRentalsWindow(username)

        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password.")

    # function created to show the rentals window
    def showRentalsWindow(self, username):
        self.rentalsWindow = Rentals(username)
        self.rentalsWindow.showMaximized()
        self.close()

    def get_password(self, username, password):
        db = Database(
            host="127.0.0.1",
            user="root",
            password="=lrD(nC2b?87",
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        is_password = db.check_password(username, password)
        db.close()
        return is_password

    def get_password(self, username, password):
        db = Database(
            host="127.0.0.1",
            user="root",
            password="=lrD(nC2b?87",
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        is_password = db.check_password(username, password)
        db.close()
        return is_password

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def clear_all_fields(self, username, password):
        # Clear the form fields after submission
        Tools.clear_form_fields(self.userNameIn, self.userPasswordIn)
