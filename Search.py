import bcrypt, re
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
<<<<<<< HEAD
    QScrollArea,
    QPushButton,  # Added for the back button
    QHBoxLayout,  # Added for Horizontal layout
=======
    QHBoxLayout,
    QPushButton,
    QScrollArea,
>>>>>>> main
    QMessageBox,
)
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
<<<<<<< HEAD
        new_listing_added=False,
=======
        added=False,
>>>>>>> main
        parent_position=None,
    ):
        super().__init__()

        self.added = added
        self.cityS = city
        self.descriptionS = description
        self.featureS = feature
        self.priceS = price
<<<<<<< HEAD
        self.username = username  # Added this to store the username
        self.new_listing_added = new_listing_added

=======
        self.username = username
>>>>>>> main
        self.showListings()

    def showListings(self):
        self.setWindowTitle(" Results ")

        # Set up layout
        mainLayout = QVBoxLayout()

<<<<<<< HEAD
        # Display message if a new listing was added
        if self.new_listing_added:
=======
        if self.added:
>>>>>>> main
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
<<<<<<< HEAD
                listingLayout = QHBoxLayout()
                listingLabel = QLabel(
                    f"Title: {unit['title']}, Description: {unit['description']}, "
                    f"Features: {features_str}, Price: {unit['price']}"
                )
                resultsLayout.addWidget(listingLabel)
=======

                listingLayout = QHBoxLayout()
                listingLabel = QLabel(f"Title: {unit['title']}")
                listingLabel2 = QLabel(f"Description: {unit['description']}")
                listingLabel3 = QLabel(f"Features: {features_str}")
                listingLabel4 = QLabel(f"Price: {unit['price']}")
                resultsLayout.addWidget(listingLabel)
                resultsLayout.addWidget(listingLabel2)
                resultsLayout.addWidget(listingLabel3)
                resultsLayout.addWidget(listingLabel4)
>>>>>>> main

                # Add 'reviews' button
                reviewsButton = QPushButton("Reviews")
                reviewsButton.clicked.connect(
                    lambda _, id=unit_id: self.open_reviews(id)
                )
<<<<<<< HEAD
=======

                reviewsButton.setFixedSize(100, 50)
>>>>>>> main
                listingLayout.addWidget(reviewsButton)

                listingWidget.setLayout(listingLayout)
                resultsLayout.addWidget(listingWidget)
        else:
            resultsLayout.addWidget(
                QLabel("Sorry! No available units found with the description provided.")
            )

        backButton = QPushButton("Back")
<<<<<<< HEAD
        backButton.clicked.connect(self.returnToRentals)
=======
        # backButton.clicked.connect(self.returnToRentals)
        backButton.setFixedSize(100, 50)
>>>>>>> main
        mainLayout.addWidget(backButton)

        # set mainLayout and add the scroll area
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

        ###Martin's connection
        db = Database(
<<<<<<< HEAD
            host="127.0.0.1",
            user="root",
            password="=lrD(nC2b?87",
=======
            host="localhost",
            user="admin_user",
            password="CS440Database",
>>>>>>> main
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        listings = db.obtain_listings(
            self.cityS, self.descriptionS, self.featureS, self.priceS
        )
        db.close()
        return listings

<<<<<<< HEAD
    # This method handles opening the ReviewWindow.
    def open_reviews(self, unit_id):
        self.review_window = ReviewWindow(self.username, unit_id)
        self.review_window.show()

    def returnToRentals(self):
        from Rentals import Rentals  # Import here to avoid circular import

        self.rentals_window = Rentals(self.username)
        self.rentals_window.show()
        self.close()
=======
    def open_reviews(self, unit_id):
        self.review_window = ReviewWindow(self.username, unit_id, self)
        self.review_window.setGeometry(0, 0, self.width(), self.height())
        self.review_window.show()
>>>>>>> main
