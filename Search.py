import bcrypt, re
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QScrollArea
)
from PyQt5.QtCore import Qt
from Database import Database
from Tools import Tools
from review import ReviewWindow

class Search(QWidget):
    def __init__(self,city,description,feature,price, username, added=False,parent_position=None):
        super().__init__()

        self.username = username
        self.added = added
        self.cityS = city
        self.descriptionS = description
        self.featureS = feature
        self.priceS = price

        self.showListings()

    def showListings(self):
        self.setWindowTitle(" Results ")

        # Set up layout
        mainLayout = QVBoxLayout()
        
        if self.added:
            QMessageBox.information(
                self, "New Listing", "A new listing has been added successfully!"
            )


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
        listings = self.obtain_listings()
        # if listings:
        #     for unit_id, unit in listings.items(): 
        #         features_str = ', '.join(unit['features'])  
        #         listingLabel = QLabel(f"Title: {unit['title']}, Description: {unit['description']}, "
        #                             f"Features: {features_str}, Price: {unit['price']}")
        #         resultsLayout.addWidget(listingLabel)
        # else:
        #     resultsLayout.addWidget(QLabel("Sorry! No available units found with the description provided."))
        
        
        if listings:
            for unit_id, unit in listings.items():
                features_str = ", ".join(unit["features"])
                listingWidget = QWidget()
                listingLayout = QHBoxLayout()
                listingLabel = QLabel(
                    f"Title: {unit['title']}, Description: {unit['description']}, "
                    f"Features: {features_str}, Price: {unit['price']}"
                )
                resultsLayout.addWidget(listingLabel)

                # Add 'reviews' button
                reviewsButton = QPushButton("Reviews")
                reviewsButton.clicked.connect(
                    lambda _, id=unit_id: self.open_reviews(id)
                )
                listingLayout.addWidget(reviewsButton)

                listingWidget.setLayout(listingLayout)
                resultsLayout.addWidget(listingWidget)
        else:
            resultsLayout.addWidget(
                QLabel("Sorry! No available units found with the description provided.")
            )

        backButton = QPushButton("Back")
        # backButton.clicked.connect(self.returnToRentals)
        mainLayout.addWidget(backButton)



        #set mainLayout and add the scroll area
        mainLayout.addWidget(scroll)
        self.setLayout(mainLayout)

    def obtain_listings(self):
        # Connect to the database and retrieve listings based on criteria
        db = Database(
            host='localhost',
            user='admin_user',
            password='CS440Database',
            database='CS440_DB_DESIGN',
        )
        db.connect()
        listings = db.obtain_listings(self.cityS, self.descriptionS, self.featureS, self.priceS)
        db.close()
        return listings
    
    
    def open_reviews(self, unit_id):
        self.review_window = ReviewWindow(self.username, unit_id)
        self.review_window.show()
