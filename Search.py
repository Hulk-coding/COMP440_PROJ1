import bcrypt, re
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QMessageBox,
    QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Database import Database
from Tools import Tools
from review import ReviewWindow


class Search(QWidget):
    def __init__(
        self,
        city,
        description,
        feature,
        price,
        username,
        added=False,
        parent_position=None,
    ):
        super().__init__()

        self.loadStylesheet("StyleSheet.qss")

        self.added = added
        self.cityS = city
        self.descriptionS = description
        self.featureS = feature
        self.priceS = price
        self.username = username
        self.showListings()


    def showListings(self):
        self.setWindowTitle(" Results ")

        mainLayout = QVBoxLayout()
        title = QLabel(" Listings: ")
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)

    
        scroll = QScrollArea()
        resultsContainer = QWidget()
        resultsLayout = QGridLayout() 
        resultsContainer.setLayout(resultsLayout)
        scroll.setWidget(resultsContainer)
        scroll.setWidgetResizable(True)

        # Obtain listings' data from DB
        listings = self.obtain_listings()
        if listings:
            row, column = 0, 0
            for unit_id, unit in listings.items():
                features_str = ", ".join(unit["features"])
                listingWidget = QWidget()
                listingWidget.setObjectName("grid")
                listingLayout = QVBoxLayout() 
                

                # Formatting listing in a box
                titleLabel = QLabel("Title: " + unit['title'])
                titleLabel.setObjectName("cells")
                listingLayout.addWidget(titleLabel)

                descriptionLabel = QLabel("Description: " + unit['description'])
                descriptionLabel.setObjectName("cells")
                listingLayout.addWidget(descriptionLabel)

                featuresLabel = QLabel("Features: " + features_str)
                featuresLabel.setObjectName("cells")
                listingLayout.addWidget(featuresLabel)

                priceLabel = QLabel("Price: $" + str(unit['price']))
                priceLabel.setObjectName("cells")
                listingLayout.addWidget(priceLabel)

                buttonLayout = QHBoxLayout()
                buttonLayout.addStretch() 
                reviewsButton = QPushButton("Reviews")
                reviewsButton.clicked.connect(
                    lambda _, id=unit_id: self.open_reviews(id)
                )
                reviewsButton.setFixedSize(100, 50)
                buttonLayout.addWidget(reviewsButton)
                buttonLayout.addStretch()  

                listingLayout.addLayout(buttonLayout)
                
                listingWidget.setLayout(listingLayout)
                resultsLayout.addWidget(listingWidget, row, column)

                #Grid Layout accomodation of listings 2 per row
                #we can change the number of columns to make the listings smaller
                #more columns = more listings in the row
                column += 1
                if column == 3:  
                    column = 0
                    row += 1
        else:
            resultsLayout.addWidget(
                QLabel("Sorry! No available units found with the description provided.")
            )

        # backButton = QPushButton("Back")
        # backButton.clicked.connect(self.returnToRentals)
        # backButton.setFixedSize(100, 50)
        # mainLayout.addWidget(backButton)

        # adding layouts to main layout and the scroll feature
        mainLayout.addWidget(scroll)
        self.setLayout(mainLayout)

    def obtain_listings(self):
        # Connect to the database and retrieve listings based on criteria
        # db = Database(
        #     host='localhost',
        #     user='admin_user',
        #     password='CS440Database',
        #     database='CS440_DB_DESIGN',
        # )

        ##Martin's connection
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        listings = db.obtain_listings(
            self.cityS, self.descriptionS, self.featureS, self.priceS
        )
        db.close()
        return listings

    def open_reviews(self, unit_id):
        self.review_window = ReviewWindow(self.username, unit_id, self)
        self.review_window.setGeometry(0, 0, self.width(), self.height())
        self.review_window.show()

    def returnToRentals(self):
        from Rentals import Rentals
        self.rentalsWindow = Rentals(self.username)  
        self.rentalsWindow.showMaximized()
        self.close()
        
    def loadStylesheet(self, filename):
        try:
            with open(filename, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")