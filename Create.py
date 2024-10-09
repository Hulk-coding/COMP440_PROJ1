from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class Create(QWidget):
    def __init__(self):
        super().__init__()
        
        # main_layout = QVBoxLayout()
        
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
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(create_btn)
        button_layout.setAlignment(Qt.AlignCenter)
        form_layout.addRow(button_layout)
       
        self.setStyleSheet("QWidget { border: 2px solid black; padding; 10px;")
       
        form_layout.setAlignment(Qt.AlignCenter)
       
        # main_layout.addLayout(form_layout)
        # main_layout.addLayout(button_layout)
    
        self.setLayout(form_layout)
        
    def create_new_account(self):
        print('connect me')