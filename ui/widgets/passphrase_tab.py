# ui/widgets/passphrase_tab.py
"""Passphrase generation tab widget"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel,
    QSpinBox, QCheckBox, QLineEdit, QPushButton, QHBoxLayout,
    QProgressBar, QFrame, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from app_config.app_config import MIN_WORDS, MAX_WORDS, DEFAULT_WORDS, DEFAULT_SEPARATOR


class PassphraseTab(QWidget):
    """Passphrase generator tab"""

    def __init__(self):
        super().__init__()
        self.init_ui()

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

    def _create_settings_group(self):
        """Create settings group box"""
        group = QGroupBox("Passphrase Settings")
        layout = QGridLayout()

        # Number of Words
        words_label = QLabel(f"Number of Words [{MIN_WORDS}–{MAX_WORDS}]:")
        self.words_spinbox = QSpinBox()
        self.words_spinbox.setRange(MIN_WORDS, MAX_WORDS)
        self.words_spinbox.setValue(DEFAULT_WORDS)
        self.words_spinbox.setMinimumHeight(35)
        self.words_spinbox.setMinimumWidth(200)

        layout.addWidget(words_label, 0, 0)
        layout.addWidget(self.words_spinbox, 0, 1)

        # Editable Separator
        separator_label = QLabel("Separator (leave empty for none):")
        self.separator_edit = QLineEdit(DEFAULT_SEPARATOR)
        self.separator_edit.setMaximumWidth(100)

        separator_row = QHBoxLayout()
        separator_row.addWidget(separator_label)
        separator_row.addWidget(self.separator_edit)
        separator_row.addStretch()
        layout.addLayout(separator_row, 1, 0, 1, 2)

        # Word Case
        wordcase_label = QLabel("Word Case:")
        self.wordcase_cb = QComboBox()
        self.wordcase_cb.addItems(["Lowercase", "Uppercase", "Title Case", "Random Case"])

        layout.addWidget(wordcase_label, 2, 0)
        layout.addWidget(self.wordcase_cb, 2, 1)

        # Character Count Display
        charcount_label = QLabel("Character Count:")
        self.charcount_display = QLabel("0")

        layout.addWidget(charcount_label, 3, 0)
        layout.addWidget(self.charcount_display, 3, 1)

        group.setLayout(layout)
        return group

    def _create_output_group(self):
        """Create output group box"""
        group = QGroupBox("Generated Passphrase")
        layout = QVBoxLayout()

        # Passphrase field
        passphrase_row = QHBoxLayout()
        self.passphrase_edit = QLineEdit()
        self.passphrase_edit.setFont(QFont("Courier", 12))
        self.passphrase_edit.setPlaceholderText("Generated passphrase will appear here...")
        self.passphrase_edit.setEchoMode(QLineEdit.Normal)
        self.passphrase_edit.setMinimumHeight(36)

        self.visibility_btn = QPushButton("👁")
        self.visibility_btn.setFixedSize(35, 35)

        passphrase_row.addWidget(self.passphrase_edit)
        passphrase_row.addWidget(self.visibility_btn)
        layout.addLayout(passphrase_row)

        # Strength indicators
        strength_frame = self._create_strength_frame()
        layout.addWidget(strength_frame)

        group.setLayout(layout)
        return group

    def _create_strength_frame(self):
        """Create strength indicator frame"""
        frame = QFrame()
        layout = QVBoxLayout()

        self.strength_label = QLabel("Passphrase Strength")
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

    def _create_actions_group(self):
        """Create actions group box - ALL BUTTONS INCLUDED"""
        group = QGroupBox("Actions")
        layout = QGridLayout()

        # Generate Passphrase Button
        self.generate_btn = QPushButton("🔄 Generate Passphrase")
        self.generate_btn.setMinimumHeight(40)

        # Copy to Clipboard Button
        self.copy_btn = QPushButton("📋 Copy to Clipboard")
        self.copy_btn.setMinimumHeight(35)

        # Save QR Code Button
        self.save_qr_btn = QPushButton("💾 Save QR Code")
        self.save_qr_btn.setMinimumHeight(35)

        # Clear All Button
        self.clear_btn = QPushButton("🗑 Clear All")
        self.clear_btn.setMinimumHeight(35)

        # Layout all buttons in grid
        layout.addWidget(self.generate_btn, 0, 0, 1, 2)      # Row 0: Full width
        layout.addWidget(self.copy_btn, 1, 0)                # Row 1: Left
        layout.addWidget(self.save_qr_btn, 1, 1)             # Row 1: Right
        layout.addWidget(self.clear_btn, 2, 0, 1, 2)         # Row 2: Full width

        group.setLayout(layout)
        return group

    def get_settings(self):
        """Get current passphrase settings"""
        return {
            "num_words": self.words_spinbox.value(),
            "separator": self.separator_edit.text(),
            "word_case": self.wordcase_cb.currentText(),
        }

    def get_passphrase(self):
        """Get current passphrase"""
        return self.passphrase_edit.text()

    def set_passphrase(self, passphrase):
        """Set passphrase text"""
        self.passphrase_edit.setText(passphrase)

    def update_char_count(self, count):
        """Update character count display"""
        self.charcount_display.setText(str(count))

    def toggle_visibility(self):
        """Toggle passphrase visibility"""
        if self.passphrase_edit.echoMode() == QLineEdit.Normal:
            self.passphrase_edit.setEchoMode(QLineEdit.Password)
            self.visibility_btn.setText("👁")
        else:
            self.passphrase_edit.setEchoMode(QLineEdit.Normal)
            self.visibility_btn.setText("🙈")

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

    def clear_all(self):
        """Clear all fields"""
        self.passphrase_edit.clear()
        self.passphrase_edit.setPlaceholderText("Generated passphrase will appear here...")
        self.passphrase_edit.setEchoMode(QLineEdit.Normal)
        self.visibility_btn.setText("👁")

        # Reset settings to defaults
        self.words_spinbox.setValue(DEFAULT_WORDS)
        self.separator_edit.setText(DEFAULT_SEPARATOR)
        self.wordcase_cb.setCurrentIndex(0)

        # Reset strength UI
        self.update_strength({
            "entropy": 0,
            "strength": "Very Weak",
            "color": "#d32f2f",
            "crack_time": "Instant",
            "progress": 0
        })

        # Reset character count
        self.charcount_display.setText("0")