from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from Database import Database

class Create(QWidget):
    def __init__(self):
        super().__init__()
        
        form_layout = QFormLayout()
        
        firstname_lbl = QLabel('first name:')
        firstname_inp = QLineEdit()
        
        lastname_lbl = QLabel('last name:')
        lastname_inp = QLineEdit()
        
        email_lbl = QLabel('email:')
        email_inp = QLineEdit()
        
        phone_lbl = QLabel('phone:')
        phone_inp = QLineEdit()
        
        username_lbl = QLabel('Username:')
        username_inp = QLineEdit()
        
        password_lbl = QLabel('Password')
        password_inp = QLineEdit()
        password_inp.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow(firstname_lbl, firstname_inp)
        form_layout.addRow(lastname_lbl, lastname_inp)
        form_layout.addRow(email_lbl, email_inp)
        form_layout.addRow(phone_lbl, phone_inp)
        form_layout.addRow(username_lbl, username_inp)
        form_layout.addRow(password_lbl, password_inp)
        
        create_btn = QPushButton('Create')
        create_btn.clicked.connect(self.create_new_account)
        
        cancel_btn = QPushButton('Cancel')
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
        
        self.setWindowTitle('Create New Account')
        
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
        
        # db = Database(
        #     host=,
        #     user=,
        #     password=,
        #     database=,
        # )
        
        db.connect()
        db.insert(firstname, lastname, email, phone, username, password)
        db.close()
        
        self.close()