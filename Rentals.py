
# import bcrypt
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from Database import Database
from Tools import Tools
from Search import Search

class Rentals(QWidget):
    def __init__(self, username, main_window):
        super().__init__()
        self.username = username
        self.added = False
        self.main_window = main_window
       
         # loading stylesheet
        self.loadStylesheet("StyleSheet.qss")

        # labels for input
        self.listingsPage = QLabel("Listings!")
        self.listingsPage.setObjectName("welcomeLabel")

        self.city = QLabel("City:")
        self.description = QLabel("Description")
        self.feature = QLabel("Feature:")
        self.price = QLabel("Price:")
        self.city.setObjectName("labels")
        self.description.setObjectName("labels")
        self.feature.setObjectName("labels")
        self.price.setObjectName("labels")

        self.listingsSign = QLineEdit()
        self.listingsPage.setFixedWidth(200)

        self.cityIn = QLineEdit()
        self.descriptionIn = QLineEdit()
        self.featureIn = QLineEdit()
        self.priceIn = QLineEdit()

        self.city.setFixedWidth(80)
        self.description.setFixedWidth(80)
        self.cityIn.setFixedWidth(200)
        self.cityIn.setObjectName("userNameIn")
        self.descriptionIn.setFixedWidth(200)
        self.descriptionIn.setObjectName("userPasswordIn")
        self.feature.setFixedWidth(80)
        self.price.setFixedWidth(80)
        self.featureIn.setFixedWidth(200)
        self.featureIn.setObjectName("userNameIn")
        self.priceIn.setFixedWidth(200)
        self.priceIn.setObjectName("userPasswordIn")

        # buttons for login page 
        self.createListingButton = QPushButton(" Create ", self)
        self.searchListingButton = QPushButton(" Search ", self)

        # Connect create button to create function
        self.createListingButton.clicked.connect(self.createListing)
        # greg added function
        self.searchListingButton.clicked.connect(self.showSearchWindow)

        # adding style elements
        self.createListingButton.setObjectName("loginButton")
        self.searchListingButton.setObjectName("createAccountButton")
        

        # formatting page, creating layouts for the components
        pageLayout = QFormLayout()

        #layout for welcome sign
        listingLayout = QFormLayout()
        listingLayout.addWidget(self.listingsPage)
        listingLayout.setAlignment(Qt.AlignCenter)

        # layout for city input
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.city)
        inputLayout.addWidget(self.cityIn)
        inputLayout.setSpacing(10)
        inputLayout.setAlignment(Qt.AlignCenter)

        # layout for description input
        inputLayout2 = QHBoxLayout()
        inputLayout2.addWidget(self.description)
        inputLayout2.addWidget(self.descriptionIn)
        inputLayout2.setSpacing(10)
        inputLayout2.setAlignment(Qt.AlignCenter)

         # layout for feature input
        inputLayout3 = QHBoxLayout()
        inputLayout3.addWidget(self.feature)
        inputLayout3.addWidget(self.featureIn)
        inputLayout3.setSpacing(10)
        inputLayout3.setAlignment(Qt.AlignCenter)

        # layout for price input
        inputLayout4 = QHBoxLayout()
        inputLayout4.addWidget(self.price)
        inputLayout4.addWidget(self.priceIn)
        inputLayout4.setSpacing(10)
        inputLayout4.setAlignment(Qt.AlignCenter)


       
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.createListingButton)
        buttonsLayout.addWidget(self.searchListingButton)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(80)
        buttonsLayout.setAlignment(Qt.AlignCenter)

        # Create a QWidget to contain both input layouts
        inputContainer = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addLayout(inputLayout)
        containerLayout.addLayout(inputLayout2)
        containerLayout.addLayout(inputLayout3)
        containerLayout.addLayout(inputLayout4)
        containerLayout.addLayout(buttonsLayout)
        inputContainer.setFixedSize(500,300)
        inputContainer.setLayout(containerLayout)
        inputContainer.setObjectName("inputContainer")
 
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(listingLayout)
        mainLayout.addWidget(inputContainer,  alignment=Qt.AlignCenter)
        #mainLayout.addLayout(pageLayout,  alignment=Qt.AlignCenter)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        self.setWindowFlags(Qt.Window)


    #successfully created lisitng
    def createListing(self):
        city = self.cityIn.text()
        description = self.descriptionIn.text()
        feature = self.featureIn.text()
        price = self.priceIn.text()


        # Here we can store the user information in our database
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="CS440_DB_DESIGN",
        )

        ##Martin's connection
        # db = Database(
        #     host="localhost",
        #     user="admin_user",
        #     password="CS440Database",
        #     database="COMP440_Fall2024_DB",
        # )
        db.connect()
        if not city or not description or not price or not feature:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
        else:
            # If fields are filled, attempt to insert the new unit
            if db.insert_new_unit(city, description, price, self.username, feature):
                QMessageBox.information(self, "SUCCESS", "Listing Created Successfully.")
                self.added = True
            else:
                QMessageBox.information(self, "Failed", "User has reached the maximum of 2 listings for today.")
    
              
        db.close()
        self.clear_all_fields(city, description, feature, price)
             

 

    def showSearchWindow(self):
        city = self.cityIn.text()
        description = self.descriptionIn.text()
        feature = self.featureIn.text()
        price = self.priceIn.text()

        self.main_window.handleRentalsToSearch(city, description, feature, price, self.username)


    def loadStylesheet(self, filename):
        try:
            with open(filename, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def clear_all_fields(self, city, description, feature, price):
    # Clear the form fields after submission
        Tools.clear_form_fields(self.cityIn, self.descriptionIn,  self.featureIn, self.priceIn)