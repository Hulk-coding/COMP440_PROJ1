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

class Search(QWidget):
    def __init__(self,city,description,feature,price, parent_position=None):
        super().__init__()

        self.cityS = city
        self.descriptionS = description
        self.featureS = feature
        self.priceS = price

        self.showListings()

    def showListings(self):
        self.setWindowTitle(" Results ")

        # Set up layout
        mainLayout = QVBoxLayout()

        # Title label
        title = QLabel(" Listings: ")
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)

        # Scroll screen feature to see listings
        scroll = QScrollArea()
        resultsContainer = QWidget()
        resultsLayout = QVBoxLayout()
        resultsContainer.setLayout(resultsLayout)
        scroll.setWidget(resultsContainer)
        scroll.setWidgetResizable(True)

        # Obtain listings' data from DB
        listings = self.obtainListings()
        if listings:
            for listing in listings:
                listingLabel = QLabel(f"City: {listing['city']}, Description: {listing['description']}, "
                                       f"Feature: {listing['feature']}, Price: {listing['price']}")
                resultsLayout.addWidget(listingLabel)
        else:
            resultsLayout.addWidget(QLabel("Sorry!, No available units found with the description provided! "))

        #set mainLayout and add the scroll area
        mainLayout.addWidget(scroll)
        self.setLayout(mainLayout)

    def obtainListings(self):
        # Connect to the database and retrieve listings based on criteria
        db = Database(
            host='localhost',
            user='admin_user',
            password='CS440Database',
            database='CS440_DB_DESIGN',
        )
        db.connect()
        listings = db.obtainListings(self.city, self.description, self.feature, self.price)
        db.close()
        return listings