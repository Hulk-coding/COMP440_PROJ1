import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from Database import Database


class ReviewWindow(QWidget):
    def __init__(self, username, unit_id):
        super().__init__()
        self.username = username
        self.unit_id = unit_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rental Review")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

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
        submit_button.clicked.connect(self.submit_review)
        layout.addWidget(submit_button)

    def submit_review(self):
        rating = int(self.rating_combo.currentText())
        review_text = self.review_text.toPlainText()

        try:
            conn = mysql.connector.connect(
                host="104.172.8.91",
                user="admin_user",
                password="CS440Database",
                database="COMP440_Fall2024_DB",
            )
            cursor = conn.cursor()

            # Call the procedure
            cursor.callproc(
                "AddReview",
                (self.rental_unit_id, self.current_user_id, review_text, rating),
            )

            # Commit the transaction
            conn.commit()

            QMessageBox.information(self, "Success", "Review submitted successfully.")
            self.close()

        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Error", f"Failed to submit review: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
