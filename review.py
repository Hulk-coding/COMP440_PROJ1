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
from PyQt5.QtCore import Qt, pyqtSignal
from Database import Database


class ReviewWindow(QWidget):
    reviewCompleted = (
        pyqtSignal()
    )  # Signal to indicate review completion or window closure

    def __init__(self, username, unit_id):
        super().__init__()
        self.username = username
        self.unit_id = unit_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rental Review")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

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

        self.setLayout(layout)

    def submit_review(self):
        rating_text = self.rating_combo.currentText()
        rating_map = {"Excellent": 3, "Good": 2, "Fair": 1, "Poor": 1}
        rating = rating_map[rating_text]
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
                (self.unit_id, self.username, review_text, rating),
            )

            # Commit the transaction
            conn.commit()

            QMessageBox.information(self, "Success", "Review submitted successfully.")
            self.reviewCompleted.emit()  # Emit the signal
            self.close()

        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Error", f"Failed to submit review: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def closeEvent(self, event):
        self.reviewCompleted.emit()  # Emit the signal when window is closed
        super().closeEvent(event)
