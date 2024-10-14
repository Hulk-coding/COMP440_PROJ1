from PyQt5.QtWidgets import QLineEdit, QTextEdit


class Tools:
    @staticmethod
    def clear_form_fields(*widgets):
        # Clears the text from the given widgets.
        # Accepts any numbers of widgets as arguments.
        for widget in widgets:
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
