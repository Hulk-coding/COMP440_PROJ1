import sys


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget,QPushButton
from PyQt5.QtGui import QScreen
from Create import Create

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sign In")
        width, height = self.getWindowSize()
        self.setGeometry(100,100, width, height)

        self.create_btn = QPushButton("Create Account", self)
        self.create_btn.clicked.connect(self.open_create_window)
        self.setCentralWidget(self.create_btn)
        
    def open_create_window(self):
        self.create_window = Create()
        self.create_window.show()
        
    # find user screen size
    def getWindowSize(self):
        screen = app.primaryScreen()
        size = screen.size()
        return size.width(), size.height()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())