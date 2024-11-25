import bcrypt, re
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
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
from PyQt5.QtCore import Qt, pyqtSignal
from Database import Database
from Tools import Tools
from review import ReviewWindow


class Search(QWidget):
    view_reviews = pyqtSignal(int, str)
    def __init__(
        self,
        city,
        description,
        feature,
        price,
        username,
        main_window,
        added=False,
    ):
        super().__init__()

        self.loadStylesheet("StyleSheet.qss")


        self.main_window = main_window
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

         # Add input fields for feature X and Y
        self.featureLayout = QHBoxLayout()  # Store as an instance variable for visibility toggling
        self.featureXLabel = QLabel("Feature X:")
        self.featureXInput = QLineEdit()
        self.featureLayout.addWidget(self.featureXLabel)
        self.featureLayout.addWidget(self.featureXInput)

        self.featureYLabel = QLabel("Feature Y:")
        self.featureYInput = QLineEdit()
        self.featureLayout.addWidget(self.featureYLabel)
        self.featureLayout.addWidget(self.featureYInput)

        mainLayout.addLayout(self.featureLayout)
        
        # Initially hide the feature inputs
        self.featureXLabel.hide()
        self.featureXInput.hide()
        self.featureYLabel.hide()
        self.featureYInput.hide()
        
        # Add filter menu
        filterMenuLayout = QHBoxLayout()
        # filterLabel = QLabel("Filter: ")
        # filterMenuLayout.addWidget(filterLabel)
        
        self.filterComboBox = QComboBox()
        self.filterComboBox.addItems([
            "Select a filter...",
            "Most Expensive Features",
            "Users with at least 2 units on the same day with Feature X and Y",
            "Units posted by User X with all reviews as Excellent/Good",
            "Users with the most rentals on 10/15/2024",
            "Users with only Poor reviews",
            "Users whose units never received Poor reviews",
        ])
        self.filterComboBox.currentIndexChanged.connect(self.applyFilter)
        filterMenuLayout.addWidget(self.filterComboBox)
        mainLayout.addLayout(filterMenuLayout)

        # Add a button to show after selecting the second filter option
        self.featureButton = QPushButton("Show Data")
        self.featureButton.clicked.connect(self.loadUsersTwoUnits)
        self.featureButton.setFixedSize(100, 50)

        # Initially hide the button
        self.featureButton.hide()
        mainLayout.addWidget(self.featureButton)

        title = QLabel(" Listings: ")
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)

        scroll = QScrollArea()
        self.resultsContainer = QWidget()
        self.resultsLayout = QGridLayout()
        self.resultsContainer.setLayout(self.resultsLayout)
        scroll.setWidget(self.resultsContainer)
        scroll.setWidgetResizable(True)

        mainLayout.addWidget(scroll)
        self.setLayout(mainLayout)

        # Initially load listings without filter
        self.loadListings()
        

    def loadListings(self, listings=None):
        # Clear current listings
        for i in reversed(range(self.resultsLayout.count())):
            self.resultsLayout.itemAt(i).widget().deleteLater()

        if listings is None:
            listings = self.obtain_listings()

        if listings:
            row, column = 0, 0
            for unit_id, unit in listings.items():
                features_str = ", ".join(unit["features"])
                listingWidget = QWidget()
                listingWidget.setObjectName("grid")
                listingLayout = QVBoxLayout()

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
                reviewsButton.clicked.connect(lambda _, id=unit_id: self.onViewReviewsButtonClicked(id))
                reviewsButton.setFixedSize(100, 50)
                buttonLayout.addWidget(reviewsButton)
                buttonLayout.addStretch()

                listingLayout.addLayout(buttonLayout)
                listingWidget.setLayout(listingLayout)
                self.resultsLayout.addWidget(listingWidget, row, column)

                column += 1
                if column == 3:
                    column = 0
                    row += 1
        else:
            self.resultsLayout.addWidget(
                QLabel("No results found for the selected filter.")
            )
    
    

    def applyFilter(self, index):
        # Hide or show feature inputs based on selected filter
        if index == 2:  # Show inputs for "Users with at least 2 units on the same day with Feature X and Y"
            self.featureXLabel.show()
            self.featureXInput.show()
            self.featureYLabel.show()
            self.featureYInput.show()
            self.featureButton.show()  
        else:  # Hide inputs for all other filters
            self.featureXLabel.hide()
            self.featureXInput.hide()
            self.featureYLabel.hide()
            self.featureYInput.hide()
            self.featureButton.hide() 
            
        if index == 0:
            self.current_filter = None
            self.loadListings()
            return

        filter_mapping = {
            1: "most_expensive_features",
            2: "users_two_units_same_day",
            3: "units_reviews_good_or_excellent",
            4: "users_most_units_10152024",
            5: "users_only_poor_reviews",
            6: "users_no_poor_reviews",
        }

        self.current_filter = filter_mapping.get(index)
        self.filterListings()

    def filterListings(self):
        if not self.current_filter:
            return

        # db = Database(
        #     host='localhost',
        #     user='admin_user',
        #     password='CS440Database',
        #     database='CS440_DB_DESIGN',
        # )
        # db.connect()
        ##Martin's connection
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        listings = db.get_filtered_items(self.current_filter, params={
        'feature_x': self.featureXInput.text().strip(),
            'feature_y': self.featureYInput.text().strip()
        })
        db.close()

        if self.current_filter == "users_only_poor_reviews":
            self.loadPoorReviewUsers(listings)
        elif self.current_filter == "users_two_units_same_day":
            self.loadUsersTwoUnits(listings)
        else:
            self.loadListings(listings)

        #function that loads users with two units same day
    def loadUsersTwoUnits(self, listings=None):
        feature_x = self.featureXInput.text().strip()
        feature_y = self.featureYInput.text().strip()
            # Clear current listings
        for i in reversed(range(self.resultsLayout.count())):
            self.resultsLayout.itemAt(i).widget().deleteLater()

            # Get features from input fields
        feature_x = self.featureXInput.text().strip()
        feature_y = self.featureYInput.text().strip()

        if not feature_x or not feature_y:
            self.resultsLayout.addWidget(
                QLabel("Please enter both Feature X and Feature Y.")
            )
            return

            # Connect to the database and query the data
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="COMP440_Fall2024_DB",
        )
        db.connect()
        users = db.get_users_two_units_same_day(feature_x, feature_y)
        db.close()

        if not users:
            self.resultsLayout.addWidget(
                QLabel("No users found with at least two units posted on the same day with the specified features.")
            )
            return

            # Display results
        row, column = 0, 0
        for username in users:
            listingWidget = QWidget()
            listingWidget.setObjectName("grid")
            listingLayout = QVBoxLayout()

            usernameLabel = QLabel("Username: " + str(username))
            usernameLabel.setObjectName("cells")
            listingLayout.addWidget(usernameLabel)

            listingWidget.setLayout(listingLayout)
            self.resultsLayout.addWidget(listingWidget, row, column)

            column += 1
            if column == 3:
                column = 0
                row += 1

        

    def loadPoorReviewUsers(self, users=None):
        # Clear current listings
        for i in reversed(range(self.resultsLayout.count())):
            self.resultsLayout.itemAt(i).widget().deleteLater()

        if not users:  # This will cover both None and empty dictionary
            self.resultsLayout.addWidget(
                QLabel("No users found with poor reviews.")
            )
            return

        row, column = 0, 0
        for username in users:
            listingWidget = QWidget()
            listingWidget.setObjectName("grid")
            listingLayout = QVBoxLayout()

            # Ensure username is treated as a string
            usernameLabel = QLabel("Username: " + str(username))
            usernameLabel.setObjectName("cells")
            listingLayout.addWidget(usernameLabel)

            # Add a placeholder to show that this user gave poor reviews
            poorReviewsLabel = QLabel("This user has given poor reviews.")
            poorReviewsLabel.setObjectName("cells")
            listingLayout.addWidget(poorReviewsLabel)

            listingWidget.setLayout(listingLayout)
            self.resultsLayout.addWidget(listingWidget, row, column)

            column += 1
            if column == 3:
                column = 0
                row += 1



        
    def onViewReviewsButtonClicked(self, unit_id):
        # Create and show the review window directly
        self.review_window = ReviewWindow(self.username, unit_id)
        self.review_window.setGeometry(0, 0, self.width(), self.height())  # Set the geometry
        self.review_window.show()  # Show the window


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