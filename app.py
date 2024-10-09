import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QScreen
from Create import Create

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sign In")
        width, height = self.getWindowSize()
        self.setGeometry(100,100, width, height)

        self.create_page = Create()
        self.setCentralWidget(self.create_page)
        
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