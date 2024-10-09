from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class Login(QWidget):
    def __init__(self):
        super().__init__()
        
        #labels for input
        userName = QLabel("Username")
        userPassword = QLabel("Password")

        userNameIn = QLineEdit()
        userPasswordIn = QLineEdit()
        userPasswordIn.setEchoMode(QLineEdit.Password)


        #buttons for login page
        loginButton = QPushButton("Login")
        createAccountButton = QPushButton("Create Account")
        
        #formatting page, creating layouts for the components 
        pageLayout = QFormLayout()
        pageLayout.addRow(userName, userNameIn)
        pageLayout.addRow(userPassword, userPasswordIn)
        
        buttonsLayout = QHBoxLayout()

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(loginButton)
        buttonsLayout.addWidget(createAccountButton)
        buttonsLayout.setAlignment(Qt.AlignCenter)
        pageLayout.addRow(buttonsLayout)
        self.setStyleSheet("QWidget { border: 2px solid black; padding; 10px;")

        pageLayout.setAlignment(Qt.AlignCenter)
       
        self.setLayout(pageLayout)
        self.setWindowTitle("Login")