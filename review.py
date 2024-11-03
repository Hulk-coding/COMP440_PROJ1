from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QLabel,
)
from PyQt5.QtCore import Qt
from Database import Database


class ReviewPage(QMainWindow):
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
        db = Database(
            host="104.172.8.91",
            user="admin_user",
            password="CS440Database",
            database="COMP440_Fall2024_DB",
        )
        db.connect()

        try:
            if not db.can_submit_review(self.username):
                QMessageBox.warning(
                    self,
                    "Review Limit Reached",
                    "You can only submit 3 reviews per day.",
                )
                return

            if db.is_self_review(self.username, self.unit_id):
                QMessageBox.warning(
                    self, "Self Review", "You cannot review your own rental unit."
                )
                return

            if db.has_reviewed_unit(self.username, self.unit_id):
                QMessageBox.warning(
                    self,
                    "Duplicate Review",
                    "You have already reviewed this rental unit.",
                )
                return

            rating = int(
                self.rating_combo.currentText()[0]
            )  # Extract the number from the rating text
            review = self.review_text.toPlainText()

            db.save_review(self.username, self.unit_id, review, rating)

            QMessageBox.information(
                self, "Review Submitted", "Your review has been submitted successfully."
            )
            self.clear_form()

        finally:
            db.close()

    def clear_form(self):
        self.rating_combo.setCurrentIndex(0)
        self.review_text.clear()
