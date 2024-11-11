import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QScreen
from Create import Create
from Login import Login
from Rentals import Rentals
from Search import Search


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RESERVATIONS 4 US")
        width, height = self.getWindowSize()
        self.setGeometry(100, 100, width, height)

        self.login_form = Login()
        self.rentals_form = None
        self.search_form = None

        self.setCentralWidget(self.login_form)
        self.createNav()

        self.login_form.login_success.connect(self.handleLogin)

    def createNav(self):
        toolbar = self.addToolBar("Navigation")

        # self.login_btn = QPushButton("Login")
        # self.login_btn.clicked.connect(lambda: self.switchView(self.login_form))
        # toolbar.addWidget(self.login_btn)

        self.rentals_btn = QPushButton("Search")
        self.rentals_btn.setEnabled(False)
        self.rentals_btn.clicked.connect(self.handleLogin)
        toolbar.addWidget(self.rentals_btn)

        # self.search_btn = QPushButton("Listings")
        # self.search_btn.clicked.connect(lambda: self.switchView(self.search_form))
        # toolbar.addWidget(self.search_btn)

    def switchView(self, new_widget):
        if new_widget:
            self.setCentralWidget(new_widget)

    def handleLogin(self, username):
        self.rentals_form = Rentals(username, self) 
        self.switchView(self.rentals_form)
        self.rentals_btn.setEnabled(True)


    def handleRentalsToSearch(self, city, description, feature, price, username):
        self.search_form = Search(city, description, feature, price, username)
        self.switchView(self.search_form)

    # Find user screen size
    def getWindowSize(self):
        screen = app.primaryScreen()
        size = screen.size()
        return size.width(), size.height()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
