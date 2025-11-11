# utils/file_handler.py
"""File I/O operations"""
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileHandler:
    """Handles file operations"""

    @staticmethod
    def save_file(parent, title, default_name, file_filter):
        """Open save file dialog"""
        filename, _ = QFileDialog.getSaveFileName(
            parent, title, default_name, file_filter
        )
        return filename

    @staticmethod
    def open_file(parent, title, file_filter):
        """Open file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            parent, title, "", file_filter
        )
        return filename

    @staticmethod
    def show_error(parent, title, message):
        """Show error dialog"""
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_warning(parent, title, message):
        """Show warning dialog"""
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_info(parent, title, message):
        """Show info dialog"""
        QMessageBox.information(parent, title, message)