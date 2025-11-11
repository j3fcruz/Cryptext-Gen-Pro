# ui/widgets/control_panel.py
"""Left control panel with mode selection and password/passphrase tabs"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtGui import QFont

from app_config.app_config import APP_NAME, ABOUT_APP, LOGO_PATH
from ui.widgets.password_tab import PasswordTab
from ui.widgets.passphrase_tab import PassphraseTab


class ControlPanel(QWidget):
    """Left control panel with mode selection and tabs"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        """Initialize control panel UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Header
        title = QLabel(APP_NAME)
        title.setObjectName("title")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title)

        subtitle = QLabel(ABOUT_APP)
        subtitle.setObjectName("subtitle")
        subtitle.setFont(QFont("Arial", 11))
        layout.addWidget(subtitle)

        # --- Mode Selection ---
        mode_group = QGroupBox("Mode")
        mode_layout = QHBoxLayout()

        self.password_radio = QRadioButton("🔑 Password")
        self.passphrase_radio = QRadioButton("📝 Passphrase")
        self.password_radio.setChecked(True)
        self.password_radio.toggled.connect(self.on_mode_changed)

        self.mode_buttons = QButtonGroup()
        self.mode_buttons.addButton(self.password_radio, 0)
        self.mode_buttons.addButton(self.passphrase_radio, 1)

        mode_layout.addWidget(self.password_radio)
        mode_layout.addWidget(self.passphrase_radio)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # --- Create Password and Passphrase Tabs ---
        self.password_tab = PasswordTab()
        self.passphrase_tab = PassphraseTab()

        layout.addWidget(self.password_tab)
        layout.addWidget(self.passphrase_tab)

        # Initially hide passphrase tab
        self.passphrase_tab.hide()

        # Connect signals from tabs to main window
        self._connect_signals()

        layout.addStretch()
        self.setLayout(layout)

    def on_mode_changed(self):
        """Handle mode change between password and passphrase"""
        if self.password_radio.isChecked():
            self.password_tab.show()
            self.passphrase_tab.hide()
        else:
            # Check if wordlist is available before switching to passphrase mode
            if not self.main_window.passphrase_gen.is_ready():
                QMessageBox.warning(
                    self,
                    "Wordlist Missing",
                    "Passphrase generator requires a wordlist.\n\n"
                    "Please ensure the wordlist file is in:\n"
                    "• assets/wordlist/eff_file.wordlist\n"
                    "• wordlist/eff_file.wordlist\n\n"
                    "Switching back to Password mode."
                )
                self.password_radio.setChecked(True)
                return

            self.password_tab.hide()
            self.passphrase_tab.show()

    def _connect_signals(self):
        """Connect tab signals to main window handlers"""
        # Password Tab Signals
        self.password_tab.generate_btn.clicked.connect(self.on_generate_password)
        self.password_tab.copy_btn.clicked.connect(self.on_copy_password)
        self.password_tab.visibility_btn.clicked.connect(self.on_toggle_password_visibility)
        self.password_tab.upload_qr_btn.clicked.connect(self.on_upload_qr)
        self.password_tab.save_qr_btn.clicked.connect(self.on_save_qr)
        self.password_tab.scan_qr_btn.clicked.connect(self.on_scan_qr)
        self.password_tab.clear_btn.clicked.connect(self.on_clear_password)
        self.password_tab.password_edit.textChanged.connect(self.on_password_changed)

        # Passphrase Tab Signals
        self.passphrase_tab.generate_btn.clicked.connect(self.on_generate_passphrase)
        self.passphrase_tab.copy_btn.clicked.connect(self.on_copy_passphrase)
        self.passphrase_tab.visibility_btn.clicked.connect(self.on_toggle_passphrase_visibility)
        self.passphrase_tab.save_qr_btn.clicked.connect(self.on_save_qr)
        self.passphrase_tab.clear_btn.clicked.connect(self.on_clear_passphrase)
        self.passphrase_tab.passphrase_edit.textChanged.connect(self.on_passphrase_changed)

    def on_generate_password(self):
        """Generate password"""
        try:
            settings = self.password_tab.get_settings()
            length = settings["length"]

            if length > 40:
                password = self.main_window.password_gen.generate_basic(
                    length,
                    settings["uppercase"],
                    settings["lowercase"],
                    settings["numbers"],
                    settings["symbols"]
                )
            else:
                password = self.main_window.password_gen.generate_advanced(
                    length,
                    settings["uppercase"],
                    settings["lowercase"],
                    settings["numbers"],
                    settings["symbols"]
                )

            self.password_tab.set_password(password)
            self.main_window.statusBar().showMessage("New password generated successfully!")

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            self.main_window.statusBar().showMessage("Failed to generate password")

    def on_generate_passphrase(self):
        """Generate passphrase"""
        try:
            if not self.main_window.passphrase_gen.is_ready():
                QMessageBox.warning(
                    self,
                    "Wordlist Missing",
                    "Passphrase generator requires a wordlist.\n\n"
                    "Please ensure the wordlist file is in:\n"
                    "• assets/wordlist/eff_file.wordlist\n"
                    "• wordlist/eff_file.wordlist"
                )
                return

            settings = self.passphrase_tab.get_settings()
            passphrase = self.main_window.passphrase_gen.generate(
                num_words=settings["num_words"],
                separator=settings["separator"],
                word_case=settings["word_case"]
            )

            self.passphrase_tab.set_passphrase(passphrase)
            self.passphrase_tab.update_char_count(len(passphrase))
            self.main_window.statusBar().showMessage("New passphrase generated successfully!")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate passphrase: {e}")
            self.main_window.statusBar().showMessage("Failed to generate passphrase")

    def on_password_changed(self):
        """Handle password text changes"""
        password = self.password_tab.get_password()
        if password:
            metrics = self.main_window.strength_analyzer.analyze(password)
            self.password_tab.update_strength(metrics)

            qr_image = self.main_window.qr_handler.generate(password, LOGO_PATH)
            self.main_window.current_qr_image = qr_image
            pixmap = self.main_window.qr_handler.to_pixmap(qr_image, 220)
            if pixmap:
                self.main_window.info_panel.set_qr_pixmap(pixmap)
        else:
            self.password_tab.update_strength(self.main_window.strength_analyzer.analyze(""))
            self.main_window.info_panel.clear_qr()

    def on_passphrase_changed(self):
        """Handle passphrase text changes"""
        passphrase = self.passphrase_tab.get_passphrase()
        if passphrase:
            metrics = self.main_window.strength_analyzer.analyze(passphrase)
            self.passphrase_tab.update_strength(metrics)

            qr_image = self.main_window.qr_handler.generate(passphrase, LOGO_PATH)
            self.main_window.current_qr_image = qr_image
            pixmap = self.main_window.qr_handler.to_pixmap(qr_image, 220)
            if pixmap:
                self.main_window.info_panel.set_qr_pixmap(pixmap)
        else:
            self.passphrase_tab.update_strength(self.main_window.strength_analyzer.analyze(""))
            self.main_window.info_panel.clear_qr()

    def on_copy_password(self):
        """Copy password to clipboard"""
        password = self.password_tab.get_password()
        if not password:
            QMessageBox.warning(self, "Warning", "No password to copy.")
            return

        if self.main_window.clipboard_manager.copy(password):
            QMessageBox.information(self, "Success", "Password copied to clipboard!")
            self.main_window.statusBar().showMessage("Password copied to clipboard!")

    def on_copy_passphrase(self):
        """Copy passphrase to clipboard"""
        passphrase = self.passphrase_tab.get_passphrase()
        if not passphrase:
            QMessageBox.warning(self, "Warning", "No passphrase to copy.")
            return

        if self.main_window.clipboard_manager.copy(passphrase):
            QMessageBox.information(self, "Success", "Passphrase copied to clipboard!")
            self.main_window.statusBar().showMessage("Passphrase copied to clipboard!")

    def on_toggle_password_visibility(self):
        """Toggle password visibility"""
        self.password_tab.toggle_visibility()

    def on_toggle_passphrase_visibility(self):
        """Toggle passphrase visibility"""
        self.passphrase_tab.toggle_visibility()

    def on_upload_qr(self):
        """Upload QR code image"""
        from utils.file_handler import FileHandler
        filename = FileHandler.open_file(
            self,
            "Select QR Code Image",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if not filename:
            return

        try:
            data = self.main_window.qr_handler.scan_from_file(filename)

            if not data:
                QMessageBox.warning(self, "Error", "No QR code found or unreadable QR code.")
                return

            self.password_tab.set_password(data)
            QMessageBox.information(self, "Success", "Password imported from QR code!")
            self.main_window.statusBar().showMessage("Password imported from QR code!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read QR code: {str(e)}")
            self.main_window.statusBar().showMessage("Failed to read QR code")

    def on_save_qr(self):
        """Save QR code to file"""
        from utils.file_handler import FileHandler

        if not self.main_window.current_qr_image:
            QMessageBox.warning(self, "Warning", "No QR code to save.")
            self.main_window.statusBar().showMessage("No QR code to save.")
            return

        filename = FileHandler.save_file(
            self,
            "Save QR Code",
            "password_qr.png",
            "PNG Files (*.png)"
        )

        if filename:
            self.main_window.current_qr_image.save(filename)
            QMessageBox.information(self, "Success", "QR code saved successfully!")
            self.main_window.statusBar().showMessage("QR code saved successfully!")

    def on_scan_qr(self):
        """Scan QR code from camera"""
        try:
            decoded_text = self.main_window.qr_handler.scan_from_camera()

            if decoded_text:
                self.password_tab.set_password(decoded_text)
                QMessageBox.information(self, "Success", "Password extracted from QR code!")
                self.main_window.statusBar().showMessage("Password extracted from QR code!")
            else:
                QMessageBox.warning(self, "Result", "No QR code was detected.")
                self.main_window.statusBar().showMessage("No QR code was detected.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to scan QR code: {e}")
            self.main_window.statusBar().showMessage("Failed to scan QR code")

    def on_clear_password(self):
        """Clear password field"""
        if not self.password_tab.get_password():
            QMessageBox.information(self, "Info", "Nothing to clear.")
            self.main_window.statusBar().showMessage("Nothing to clear.")
            return

        self.password_tab.clear_all()
        self.main_window.info_panel.clear_qr()
        QMessageBox.information(self, "Success", "All fields reset to default state.")
        self.main_window.statusBar().showMessage("All fields reset to default state.")

    def on_clear_passphrase(self):
        """Clear passphrase field"""
        if not self.passphrase_tab.get_passphrase():
            QMessageBox.information(self, "Info", "Nothing to clear.")
            self.main_window.statusBar().showMessage("Nothing to clear.")
            return

        self.passphrase_tab.clear_all()
        self.main_window.info_panel.clear_qr()
        QMessageBox.information(self, "Success", "All fields reset to default state.")
        self.main_window.statusBar().showMessage("All fields reset to default state.")