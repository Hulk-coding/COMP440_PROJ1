from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from Create import Create

class Login(QWidget):
    def __init__(self):
        super().__init__()
        
        #labels for input
        userName = QLabel("Username")
        userPassword = QLabel("Password")

        userNameIn = QLineEdit()
        userPasswordIn = QLineEdit()
        userPasswordIn.setEchoMode(QLineEdit.Password)


        #buttons for login page - greg edited
        self.loginButton = QPushButton("Login", self)
        self.createAccountButton = QPushButton("Create Account", self)
        
        # greg added function
        self.createAccountButton.clicked.connect(self.open_create_window)
        
        #formatting page, creating layouts for the components 
        pageLayout = QFormLayout()
        pageLayout.addRow(userName, userNameIn)
        pageLayout.addRow(userPassword, userPasswordIn)
        
        buttonsLayout = QHBoxLayout()

        # greg edit - add self
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.loginButton)
        buttonsLayout.addWidget(self.createAccountButton)
        buttonsLayout.setAlignment(Qt.AlignCenter)
        pageLayout.addRow(buttonsLayout)
        # self.setStyleSheet("QWidget { border: 2px solid black; padding; 10px;") # this is not doing anything visible

        pageLayout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(pageLayout)
        # self.setWindowTitle("Login")
        
    # greg added create function
    def open_create_window(self):
        self.create_window = Create()
        self.create_window.show()
    
        
       
        