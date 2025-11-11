# utils/clipboard_manager.py
"""Clipboard operations"""
from PyQt5.QtWidgets import QApplication, QMessageBox


class ClipboardManager:
    """Manages clipboard operations"""

    @staticmethod
    def copy(text):
        """Copy text to clipboard"""
        if not text:
            return False

        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        return True

    @staticmethod
    def show_copied_message(parent, text):
        """Show confirmation message"""
        QMessageBox.information(parent, "Success", f"{text} copied to clipboard!")