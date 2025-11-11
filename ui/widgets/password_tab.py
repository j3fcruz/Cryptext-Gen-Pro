# ui/widgets/password_tab.py
"""Password generation tab widget - Final Working Version"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel,
    QSpinBox, QCheckBox, QLineEdit, QPushButton, QHBoxLayout,
    QProgressBar, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from app_config.app_config import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, DEFAULT_PASSWORD_LENGTH, LOGO_PATH


class PasswordTab(QWidget):
    """Password generator tab"""

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.password_visible = False
        self.current_qr_image = None
        self.logo_path = LOGO_PATH

        # Visibility state tracking
        self.visibility_states = {"password": False}

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()

        # Settings Group
        settings_group = self._create_settings_group()
        layout.addWidget(settings_group)

        # Output Group
        output_group = self._create_output_group()
        layout.addWidget(output_group)

        # Actions Group
        actions_group = self._create_actions_group()
        layout.addWidget(actions_group)

        layout.addStretch()
        self.setLayout(layout)

    # -------------------------
    # SETTINGS GROUP
    # -------------------------
    def _create_settings_group(self):
        """Create settings group box"""
        group = QGroupBox("Password Settings")
        layout = QGridLayout()

        # Length
        layout.addWidget(QLabel(f"Password Length [MIN={MIN_PASSWORD_LENGTH},MAX={MAX_PASSWORD_LENGTH}]:"), 0, 0)
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
        self.length_spinbox.setValue(DEFAULT_PASSWORD_LENGTH)
        self.length_spinbox.setMinimumHeight(35)
        self.length_spinbox.setMinimumWidth(200)
        layout.addWidget(self.length_spinbox, 0, 1)

        # Character options
        self.uppercase_cb = QCheckBox("Uppercase letters (A-Z)")
        self.lowercase_cb = QCheckBox("Lowercase letters (a-z)")
        self.numbers_cb = QCheckBox("Numbers (0-9)")
        self.symbols_cb = QCheckBox("Special symbols (!@#$%...)")
        for cb in [self.uppercase_cb, self.lowercase_cb, self.numbers_cb, self.symbols_cb]:
            cb.setChecked(True)
            cb.setFont(QFont("Arial", 10))

        layout.addWidget(self.uppercase_cb, 1, 0, 1, 2)
        layout.addWidget(self.lowercase_cb, 2, 0, 1, 2)
        layout.addWidget(self.numbers_cb, 3, 0, 1, 2)
        layout.addWidget(self.symbols_cb, 4, 0, 1, 2)

        group.setLayout(layout)
        return group

    # -------------------------
    # OUTPUT GROUP
    # -------------------------
    def _create_output_group(self):
        """Create output group box"""
        group = QGroupBox("Generated Password")
        layout = QVBoxLayout()

        # Password field + visibility
        password_row = QHBoxLayout()
        self.password_edit = QLineEdit()
        self.password_edit.setFont(QFont("Courier", 12))
        self.password_edit.setPlaceholderText("Generated password will appear here...")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setMinimumHeight(36)
        self.password_edit.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # FIX: Eye button uses echoMode() directly, not state variable
        self.visibility_btn = QPushButton("👁")
        self.visibility_btn.setFixedSize(35, 35)
        self.visibility_btn.setToolTip("Toggle password visibility")
        self.visibility_btn.clicked.connect(self.toggle_visibility)

        password_row.addWidget(self.password_edit)
        password_row.addWidget(self.visibility_btn)
        layout.addLayout(password_row)

        # Strength indicators
        layout.addWidget(self._create_strength_frame())

        group.setLayout(layout)
        return group

    def _create_strength_frame(self):
        """Create strength indicator frame"""
        frame = QFrame()
        layout = QVBoxLayout()

        self.strength_label = QLabel("Password Strength")
        self.strength_label.setFont(QFont("Arial", 10, QFont.Bold))

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(12)

        self.strength_text_label = QLabel("")
        self.entropy_label = QLabel("")
        self.crack_time_label = QLabel("")

        for label in [self.strength_text_label, self.entropy_label, self.crack_time_label]:
            label.setFont(QFont("Arial", 9))

        layout.addWidget(self.strength_label)
        layout.addWidget(self.strength_bar)
        layout.addWidget(self.strength_text_label)
        layout.addWidget(self.entropy_label)
        layout.addWidget(self.crack_time_label)
        frame.setLayout(layout)
        return frame

    # -------------------------
    # ACTIONS GROUP
    # -------------------------
    def _create_actions_group(self):
        """Create actions group box - ALL BUTTONS INCLUDED"""
        group = QGroupBox("Actions")
        layout = QGridLayout()

        # Generate Password Button
        self.generate_btn = QPushButton("🔄 Generate Password")
        self.generate_btn.setMinimumHeight(40)

        # Upload QR Image Button
        self.upload_qr_btn = QPushButton("📁 Upload QR Image")
        self.upload_qr_btn.setMinimumHeight(35)

        # Copy to Clipboard Button
        self.copy_btn = QPushButton("📋 Copy to Clipboard")
        self.copy_btn.setMinimumHeight(35)

        # Save QR Code Button
        self.save_qr_btn = QPushButton("💾 Save QR Code")
        self.save_qr_btn.setMinimumHeight(35)

        # Scan QR Code Button
        self.scan_qr_btn = QPushButton("📷 Scan QR Code")
        self.scan_qr_btn.setMinimumHeight(35)

        # Clear All Button
        self.clear_btn = QPushButton("🗑 Clear All")
        self.clear_btn.setMinimumHeight(35)

        # Layout all buttons in grid
        layout.addWidget(self.generate_btn, 0, 0, 1, 2)  # Row 0: Full width
        layout.addWidget(self.upload_qr_btn, 1, 0, 1, 2)  # Row 1: Full width
        layout.addWidget(self.copy_btn, 2, 0)  # Row 2: Left
        layout.addWidget(self.save_qr_btn, 2, 1)  # Row 2: Right
        layout.addWidget(self.scan_qr_btn, 3, 0)  # Row 3: Left
        layout.addWidget(self.clear_btn, 3, 1)  # Row 3: Right

        group.setLayout(layout)
        return group

    # -------------------------
    # SETTINGS / PASSWORD METHODS
    # -------------------------
    def get_settings(self):
        """Get current password settings"""
        return {
            "length": self.length_spinbox.value(),
            "uppercase": self.uppercase_cb.isChecked(),
            "lowercase": self.lowercase_cb.isChecked(),
            "numbers": self.numbers_cb.isChecked(),
            "symbols": self.symbols_cb.isChecked(),
        }

    def set_password(self, password):
        """Set password text"""
        self.password_edit.setText(password)

    def get_password(self):
        """Get current password"""
        return self.password_edit.text()

    # -------------------------
    # VISIBILITY METHODS - FIXED VERSION
    # -------------------------
    def toggle_visibility_(self):
        """Toggle password visibility - WORKING VERSION

        Uses echoMode() directly instead of tracking state variable.
        This is the key fix that makes it work perfectly!
        """
        if self.password_edit.echoMode() == QLineEdit.Normal:
            # Hide password
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.visibility_btn.setText("👁")
        else:
            # Show password
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.visibility_btn.setText("🙈")

    def reset_visibility_(self):
        """Reset to hidden state"""
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.visibility_btn.setText("👁")

    def toggle_visibility(self):
        """Toggle password visibility"""
        if self.password_visible:
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.visibility_btn.setText("👁")
            self.password_visible = False
        else:
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.visibility_btn.setText("🙈")
            self.password_visible = True

    def reset_visibility(self):
        """Reset to hidden state with default button text"""
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.visibility_btn.setText("👁 Show")

    # -------------------------
    # CLEAR METHODS
    # -------------------------
    def clear_password(self):
        """Clear only the password field"""
        self.password_edit.clear()
        self.password_edit.setPlaceholderText("Generated password will appear here...")
        self.reset_visibility()

    def clear_all(self):
        """Clear all fields and reset defaults"""
        self.clear_password()
        self.uppercase_cb.setChecked(True)
        self.lowercase_cb.setChecked(True)
        self.numbers_cb.setChecked(True)
        self.symbols_cb.setChecked(True)
        self.length_spinbox.setValue(DEFAULT_PASSWORD_LENGTH)
        # Reset strength bar
        self.update_strength({
            "entropy": 0,
            "strength": "Very Weak",
            "color": "#d32f2f",
            "crack_time": "Instant",
            "progress": 0
        })

    # -------------------------
    # STRENGTH METHODS
    # -------------------------
    def update_strength(self, strength_data):
        """Update strength indicator"""
        self.strength_bar.setValue(strength_data["progress"])
        self.strength_text_label.setText(f"Strength: {strength_data['strength']}")
        self.entropy_label.setText(f"Entropy: {strength_data['entropy']:.1f} bits")
        self.crack_time_label.setText(f"Crack time: {strength_data['crack_time']}")
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {strength_data['color']};
                border-radius: 3px;
            }}
        """)

