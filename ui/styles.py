"""
ui/styles.py
=============
UI styling and theming manager for Cryptext Gen Pro.

This module handles dynamic theme loading, fallback to default themes,
and error logging for reliable UI consistency.
"""

import os
import datetime
from PyQt5.QtCore import QFile, QTextStream
from app_config.app_config import DARK_THEME_QSS, LIGHT_THEME_QSS, APPLY_THEME
import resources_rc

class StyleManager:
    """Manages application styling and theme switching."""

    @staticmethod
    def load_stylesheet(app, path=APPLY_THEME):
        """
        Load a QSS stylesheet and apply it to the application.

        Args:
            app: QApplication instance
            path (str): Path to QSS file (can be resource or file path)
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        if not app:
            print("[⚠️] No QApplication instance provided for stylesheet loading.")
            return False

        file = QFile(path)
        if not file.exists():
            print(f"[❌] QSS file not found: {path}")
            return False

        if not file.open(QFile.ReadOnly | QFile.Text):
            print(f"[❌] Failed to open QSS file: {path}")
            return False

        try:
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            app.setStyleSheet(stylesheet)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[✅] Theme applied successfully from: {path} at {timestamp}")
            return True
        except Exception as e:
            print(f"[❌] Exception applying theme: {e}")
            return False
        finally:
            file.close()

    @staticmethod
    def apply_fallback_theme(app, dark_mode=True):
        """
        Apply fallback theme (dark or light) if main theme fails.
        """
        fallback_path = DARK_THEME_QSS if dark_mode else LIGHT_THEME_QSS
        print(f"[ℹ️] Applying fallback theme: {fallback_path}")
        return StyleManager.load_stylesheet(app, fallback_path)

    @staticmethod
    def switch_theme(app, dark_mode=True):
        """
        Switch between dark and light theme dynamically.
        """
        target = DARK_THEME_QSS if dark_mode else LIGHT_THEME_QSS
        if not StyleManager.load_stylesheet(app, target):
            StyleManager.apply_fallback_theme(app, dark_mode)
