# dialog/help_dialog.py
# ---------------------------------------------------------
# 📘 Help & Documentation Dialog - Cryptext Gen Pro
# ---------------------------------------------------------
# Provides in-app documentation, shortcuts,
# encryption overview, QR features, theming, and troubleshooting.
# Fully theme-compatible (Dark/Light).
# ---------------------------------------------------------

import os, sys
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QTabWidget, QWidget, QLabel
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from app_config.app_config import (
    APP_NAME, HELP_ICON_PATH, DARK_THEME_QSS, LIGHT_THEME_QSS
)
import resources_rc


class HelpDialog(QDialog):
    """Comprehensive Help and Documentation dialog for Cryptext Gen Pro."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} - Help & Documentation")
        self.setMinimumSize(780, 540)
        self.setModal(True)

        self.setWindowIcon(QIcon(HELP_ICON_PATH))
        self.dark_mode = True  # ✅ default, can later be auto-detected
        self.setup_ui()
        self.apply_theme()

    # ---------------------------------------------------------
    # 🎨 Apply Theme
    # ---------------------------------------------------------
    def apply_theme(self):
        """Apply the currently selected QSS theme."""
        try:
            qss_path = DARK_THEME_QSS if self.dark_mode else LIGHT_THEME_QSS
            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            print(f"⚠️ Failed to apply theme: {e}")

    # ---------------------------------------------------------
    # 🧱 UI Structure
    # ---------------------------------------------------------
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title
        title_label = QLabel(f"{APP_NAME} - Help & Documentation")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_overview_tab(), "Overview")
        tab_widget.addTab(self.create_shortcuts_tab(), "Keyboard Shortcuts")
        tab_widget.addTab(self.create_encryption_tab(), "Encryption & QR Security")
        tab_widget.addTab(self.create_theming_tab(), "Themes & Interface")
        tab_widget.addTab(self.create_troubleshooting_tab(), "Troubleshooting")
        layout.addWidget(tab_widget)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.setFixedWidth(90)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    # ---------------------------------------------------------
    # 📘 Tabs
    # ---------------------------------------------------------
    def create_overview_tab(self):
        """Overview tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Welcome to {APP_NAME}</h2>
        <p><b>{APP_NAME}</b> is a professional-grade password and QR code generator 
        engineered for cybersecurity professionals, developers, and privacy advocates.</p>

        <h3>Key Features</h3>
        <ul>
            <li>🔑 <b>Secure Password Generation</b> — Cryptographically strong random keys.</li>
            <li>🧩 <b>QR Code Integration</b> — Instantly generate encrypted QR payloads.</li>
            <li>🔐 <b>Integrity Chain</b> — Detects tampering across sessions and builds.</li>
            <li>💾 <b>Persistent Config</b> — Securely stores app state and integrity logs.</li>
            <li>🧠 <b>Professional Interface</b> — Neon dark mode optimized for clarity.</li>
        </ul>

        <h3>Quick Start</h3>
        <ol>
            <li>Launch <b>{APP_NAME}</b>.</li>
            <li>Select your desired password complexity or custom length.</li>
            <li>Click <b>Generate</b> to produce a new secure password.</li>
            <li>Optionally, click <b>Generate QR</b> to export an encrypted QR code.</li>
        </ol>
        """)
        layout.addWidget(text)
        return widget

    def create_shortcuts_tab(self):
        """Keyboard shortcuts tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml("""
        <h2>Keyboard Shortcuts</h2>
        <p>Accelerate your workflow with the following shortcuts:</p>
        <table border="1" cellspacing="0" cellpadding="6" width="100%">
            <tr><th align="left">Action</th><th align="left">Shortcut</th></tr>
            <tr><td>Generate Password</td><td><b>Ctrl + G</b></td></tr>
            <tr><td>Copy Password</td><td><b>Ctrl + C</b></td></tr>
            <tr><td>Generate QR Code</td><td><b>Ctrl + Q</b></td></tr>
            <tr><td>Save Encrypted File</td><td><b>Ctrl + S</b></td></tr>
            <tr><td>Clear Fields</td><td><b>Ctrl + L</b></td></tr>
            <tr><td>Toggle Theme</td><td><b>Ctrl + T</b></td></tr>
            <tr><td>Open Help</td><td><b>F1</b></td></tr>
        </table>
        """)
        layout.addWidget(text)
        return widget

    def create_encryption_tab(self):
        """Encryption & QR security tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Encryption & QR Security</h2>
        <p>{APP_NAME} uses <b>AES-GCM</b> encryption combined with <b>PBKDF2-HMAC</b> key derivation 
        to ensure cryptographic strength and resistance against brute-force attacks.</p>

        <h3>QR Code Protection</h3>
        <ul>
            <li>Each QR code contains <b>encrypted payloads</b> with metadata signatures.</li>
            <li>Nonces and checksums prevent duplication or tampering.</li>
            <li>Integrated checksum chain logs each QR generation event securely.</li>
        </ul>

        <h3>Security Best Practices</h3>
        <ul>
            <li>Use long master keys (≥ 16 chars) for entropy-based generation.</li>
            <li>Never share unencrypted QR codes.</li>
            <li>Regularly rotate your secrets and regenerate hashes.</li>
            <li>Enable “Integrity Watch” for baseline file verification.</li>
        </ul>

        <h3>⚠️ Important</h3>
        <p>All encryption is local — your data never leaves your device.
        Lost encryption keys or corrupted baselines cannot be recovered.</p>
        """)
        layout.addWidget(text)
        return widget

    def create_theming_tab(self):
        """Themes & Interface tab (Single Theme: Indigo Dark)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Themes & Interface</h2>
        <p>{APP_NAME} now uses a <b>Single Indigo Dark Theme</b>, optimized for readability, clarity, and professional use.</p>

        <h3>Mode</h3>
        <ul>
            <li>💠 <b>Indigo Dark:</b> Consistent dark interface with indigo accents, neon highlights, and modern styling.</li>
        </ul>

        <h3>Customization</h3>
        <p>You can adjust minor visual details by editing <code>/assets/themes/indigo_dark.qss</code> if needed.</p>
        """)
        layout.addWidget(text)
        return widget

    def create_troubleshooting_tab(self):
        """Troubleshooting tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(f"""
        <h2>Troubleshooting</h2>

        <h3>Common Issues</h3>

        <h4>1. QR Not Displaying</h4>
        <p><b>Cause:</b> Missing Pillow or qrcode library.<br>
        <b>Fix:</b> Reinstall using <code>pip install pillow qrcode</code>.</p>

        <h4>2. Integrity Check Failed</h4>
        <p><b>Cause:</b> Tampered files or mismatched baseline.<br>
        <b>Fix:</b> Reset baseline via <b>Settings → Security → Rebuild Integrity</b>.</p>

        <h4>3. Theme Not Applying</h4>
        <p><b>Cause:</b> Missing QSS or resource path error.<br>
        <b>Fix:</b> Ensure <code>stylesheet.qss</code> is correctly referenced in assets.</p>

        <h3>Getting Support</h3>
        <ul>
            <li>Visit our GitHub for FAQs and issue tracking.</li>
            <li>View “Help → About” for version and author details.</li>
            <li>Email: <b>security@patronhubdevs.online</b> for verified vulnerability reports.</li>
        </ul>

        <p>Thank you for using <b>{APP_NAME}</b> — 
        your trusted companion for secure password & QR generation.</p>
        """)
        layout.addWidget(text)
        return widget
