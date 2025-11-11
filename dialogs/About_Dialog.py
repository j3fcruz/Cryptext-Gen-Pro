"""
about_dialog.py
================
About Dialog for Cryptext Gen Pro v2.0.0

Displays version, author info, website, license, and support links.

Author      : Marco Polo (PatronHub)
Website     : https://patronhubdevs.online
GitHub      : https://github.com/j3fcruz
Ko-fi       : https://ko-fi.com/marcopolo55681
Created     : 2025-11-11
License     : MIT License
"""

import os, sys
import webbrowser
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from app_config.app_config import (
    APP_NAME, APP_VERSION, APP_DEVELOPER, AUTHOR,
    ABOUT_ICON_PATH, DARK_THEME_QSS, LIGHT_THEME_QSS
)
from utils.icon_manager import load_icon
import resources_rc


class AboutDialog(QDialog):
    """About dialog showing Cryptext Gen Pro application information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(520, 420)
        self.setModal(True)
        self.setWindowIcon(QIcon(ABOUT_ICON_PATH))

        # Default dark theme (auto-detect optional)
        self.dark_mode = True

        self.setup_ui()
        self.apply_theme()

    def apply_theme(self):
        """Apply selected QSS theme."""
        try:
            qss_path = DARK_THEME_QSS if self.dark_mode else LIGHT_THEME_QSS
            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding="utf-8") as file:
                    self.setStyleSheet(file.read())
        except Exception as e:
            print(f"⚠️ Failed to apply theme: {e}")

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # --- Header section ---
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # App icon
        icon_label = QLabel()
        icon_label.setFixedSize(72, 72)
        app_icon = load_icon("cryptext_icon.png")

        if app_icon and not app_icon.isNull():
            icon_label.setPixmap(app_icon.pixmap(64, 64))
        else:
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #39ff14;
                    border-radius: 36px;
                    color: black;
                    font-size: 22px;
                    font-weight: bold;
                    border: 2px solid #00ff88;
                }
            """)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setText("CG")

        header_layout.addWidget(icon_label)

        # App title + version
        title_layout = QVBoxLayout()
        title_label = QLabel(APP_NAME)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_layout.addWidget(title_label)

        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        title_layout.addWidget(version_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        layout.addWidget(header_frame)

        # --- Separator ---
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # --- Description section ---
        description = QTextEdit()
        description.setReadOnly(True)
        description.setMaximumHeight(200)
        description.setHtml("""
        <h3>Cryptext Gen Pro</h3>
        <p><b>Cryptext Gen Pro</b> is a professional-grade password and QR code generator
        designed for security-focused developers and enterprises.</p>
        <ul>
            <li><b>Secure Key Generation</b> — AES-GCM and PBKDF2-HMAC based entropy.</li>
            <li><b>QR Integration</b> — Instantly create encrypted QR payloads.</li>
            <li><b>Integrity Chain</b> — Built-in tamper detection and verification.</li>
            <li><b>Dark Neon UI</b> — Modern hacker-style neon interface for professionals.</li>
        </ul>
        <p>Cryptext Gen Pro empowers cybersecurity-minded users to generate, verify,
        and store credentials securely with elegant simplicity.</p>
        """)
        layout.addWidget(description)

        # --- Footer / Credits ---
        credits_label = QLabel()
        credits_label.setWordWrap(True)
        credits_label.setText(
            f"Developed by {AUTHOR} – {APP_DEVELOPER}\n\n"
            f"© 2025 {APP_NAME}. All rights reserved.\n"
            "Powered by PyQt5, Python 3, and modern encryption technologies."
        )
        credits_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        layout.addWidget(credits_label)

        # --- Support Buttons Section ---
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        website_btn = QPushButton("🌐 PatronHubDevs")
        website_btn.clicked.connect(lambda: webbrowser.open("https://patronhubdevs.online"))
        buttons_layout.addWidget(website_btn)

        github_btn = QPushButton("💻 GitHub")
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/j3fcruz"))
        buttons_layout.addWidget(github_btn)

        kofi_btn = QPushButton("☕ Ko-fi")
        kofi_btn.clicked.connect(lambda: webbrowser.open("https://ko-fi.com/marcopolo55681"))
        buttons_layout.addWidget(kofi_btn)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(80)
        ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_btn)

        layout.addLayout(buttons_layout)
