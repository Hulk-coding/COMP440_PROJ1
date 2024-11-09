import sys

# import mysql.connector
from PyQt5.QtWidgets import (
    # QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    # QHBoxLayout,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    # QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import Qt, pyqtSignal
from Database import Database


class ReviewWindow(QWidget):
    reviewCompleted = (
        pyqtSignal()
    )  # Signal to indicate review completion or window closure

    def __init__(self, username, unit_id, parent=None):
        super().__init__(parent)
        self.username = username
        self.unit_id = unit_id
        self.initUI()

        # Load existing reviews after initializing UI
        self.load_existing_reviews()

    def initUI(self):
        self.setWindowTitle("Rental Review")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Section for displaying existing reviews
        self.existing_reviews = QTextEdit()
        self.existing_reviews.setReadOnly(True)
        layout.addWidget(QLabel("Existing Reviews:"))
        layout.addWidget(self.existing_reviews)

        # Dropdown for rating
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["Excellent", "Good", "Fair", "Poor"])
        layout.addWidget(QLabel("Rating:"))
        layout.addWidget(self.rating_combo)

        # Text area for review description
        self.review_text = QTextEdit()
        self.review_text.setPlaceholderText("This is a cool place to rent.")
        layout.addWidget(QLabel("Review:"))
        layout.addWidget(self.review_text)

        # Submit button
        submit_button = QPushButton("Submit Review")
        submit_button.clicked.connect(self.capture_and_submit_review)
        submit_button.clicked.connect(self.closeReview)  # Close after submission

    def capture_and_submit_review(self):
        # Capture the input values from the UI
        rating_mapping = {"Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4}
        review_text = self.review_text.toPlainText()
        rating = self.rating_combo.currentText()

        rating_text = self.rating_combo.currentText()
        rating = rating_mapping.get(rating_text)

        # db = Database(
        #             host="localhost",
        #             user="admin_user",
        #             password="CS440Database",
        #             database="CS440_DB_DESIGN",
        #         )
        # db.connect()

        ###Martin's connection
        db = Database(
            host="127.0.0.1",
            user="root",
            password="=lrD(nC2b?87",
            database="COMP440_Fall2024_DB",
        )
        #     host="localhost",
        #     user="admin_user",
        #     password="CS440Database",
        #     database="COMP440_Fall2024_DB",
        # )
        db.connect()
        # Call the method to submit the review
        db.submit_review(self.unit_id, self.username, review_text, rating)
        db.close()

        self.reviewCompleted.emit()
        self.close()

    def closeReview(self):
        self.reviewCompleted.emit()  # Emit signal if needed
        self.hide()  # Hide instead of closing a new window

    def closeEvent(self, event):
        self.reviewCompleted.emit()  # Emit signal on close
        super().closeEvent(event)  # Call parent class's closeEvent method

    def load_existing_reviews(self):
        db = Database(
            host="localhost",
            user="admin_user",
            password="CS440Database",
            database="COMP440_Fall2024_DB",
        )

        db.connect()

        # Database class to fetch reviews by unit_id
        reviews = db.get_reviews_by_unit_id(self.unit_id)

        db.close()

        # Display reviews in the text edit widget
        all_reviews = "\n\n".join(
            [
                f"User: {review['username']}\nRating: {review['rating']}\n{review['text']}"
                for review in reviews
            ]
        )

        self.existing_reviews.setText(all_reviews)
