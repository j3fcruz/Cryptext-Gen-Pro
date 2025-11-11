# ui/widgets/info_panel.py
"""Right info panel with QR code, about, and donation sections"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QScrollArea, QFrame, QPushButton, QMessageBox, QDialog
)
from PyQt5.QtGui import QFont, QPixmap, QDesktopServices, QImage
from PyQt5.QtCore import Qt, QUrl, QIODevice, QBuffer, QByteArray

from io import BytesIO
import qrcode

from app_config.app_config import APP_NAME, APP_VERSION, LOGO_PATH, MAYA_QR_KEY, MAYA_QR_PATH
from utils.encryption import EncryptionManager
from utils.file_handler import FileHandler
from PIL import Image
import resources_rc

class InfoPanel(QWidget):
    """Right info panel with QR, About, and Donations"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        """Initialize info panel UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # --- QR Code Group ---
        qr_group = self._create_qr_group()
        layout.addWidget(qr_group)

        # --- About / Info Group ---
        info_group = self._create_about_group()
        layout.addWidget(info_group)

        # --- Support & Donations Group ---
        donate_group = self._create_donate_group()
        layout.addWidget(donate_group)

        layout.addStretch()
        self.setLayout(layout)

    def _create_qr_group(self):
        """Create QR code group box"""
        group = QGroupBox("QR Code")
        layout = QVBoxLayout()

        self.qr_label = QLabel("QR Code will\nappear here")
        self.qr_label.setFixedSize(220, 220)
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setTextFormat(Qt.RichText)
        self.qr_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #fff;
                color: #888;
                font-size: 11pt;
            }
        """)

        layout.addWidget(self.qr_label)
        group.setLayout(layout)
        return group

    def _create_about_group(self):
        """Create about information group box"""
        group = QGroupBox("About")
        layout = QVBoxLayout()

        info_label = QLabel()
        info_label.setTextFormat(Qt.RichText)
        info_label.setAlignment(Qt.AlignTop)
        info_label.setWordWrap(True)
        info_label.setFont(QFont("Arial", 9))
        info_label.setText(f"""
            <b>🔐 {APP_NAME} {APP_VERSION}</b><br><br>
            {APP_NAME} is a professional offline password generator designed for privacy-conscious users.<br><br>
            <b>Key Features:</b>
            <ul style="margin-left: -20px;">
                <li>Cryptographically secure password generation</li>
                <li>Customizable character sets</li>
                <li>Real-time strength and entropy analysis</li>
                <li>QR code generation and scanning</li>
                <li>Fully offline and privacy-respecting</li>
                <li>Modern, intuitive interface</li>
            </ul>
        """)

        info_scroll = QScrollArea()
        info_scroll.setWidgetResizable(True)
        info_scroll.setFrameShape(QFrame.NoFrame)
        info_scroll.setFixedHeight(180)

        info_container = QWidget()
        info_container_layout = QVBoxLayout(info_container)
        info_container_layout.setContentsMargins(0, 0, 0, 0)
        info_container_layout.addWidget(info_label)

        info_scroll.setWidget(info_container)
        layout.addWidget(info_scroll)
        group.setLayout(layout)
        return group

    def _create_donate_group(self):
        """Create donation support group box"""
        group = QGroupBox("Support & Donations")
        layout = QVBoxLayout()

        donate_text = QLabel(f"""
            Thank you for supporting the development of <b>{APP_NAME}</b>!<br><br>
            Your contribution helps keep the app free and continually improving.<br><br>

            <b>Ways to Donate:</b><br>
            • <a href="ko-fi" style="color: orange;">Ko-fi</a><br>
            • <a href="paypal" style="color: orange;">PayPal</a><br>
            • <a href="bitcoin" style="color: orange;">Bitcoin (BTC)</a><br>
            • <a href="ethereum" style="color: orange;">Ethereum (ETH)</a><br>
            • <a href="maya" style="color: orange;">Maya</a>
        """)
        donate_text.setFont(QFont("Arial", 9))
        donate_text.setWordWrap(True)
        donate_text.setTextFormat(Qt.RichText)
        donate_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        donate_text.setOpenExternalLinks(False)
        donate_text.linkActivated.connect(self.on_donation_link)

        donate_scroll = QScrollArea()
        donate_scroll.setWidgetResizable(True)
        donate_scroll.setFrameShape(QFrame.NoFrame)
        donate_scroll.setFixedHeight(130)

        donate_container = QWidget()
        donate_layout_inner = QVBoxLayout(donate_container)
        donate_layout_inner.setContentsMargins(0, 0, 0, 0)
        donate_layout_inner.addWidget(donate_text)

        donate_scroll.setWidget(donate_container)
        layout.addWidget(donate_scroll)
        group.setLayout(layout)
        return group

    def on_donation_link(self, link):
        """Handle donation link clicks"""
        if link == "ko-fi":
            QDesktopServices.openUrl(QUrl("https://ko-fi.com/marcopolo55681"))
        elif link == "paypal":
            QDesktopServices.openUrl(QUrl("https://paypal.me/jofreydelacruz13"))
        elif link == "bitcoin":
            QMessageBox.information(self, "Bitcoin (BTC) Address", "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk")
        elif link == "ethereum":
            QMessageBox.information(self, "Ethereum (ETH) Address", "0xcd5eef32ff4854e4cefa13cb308b727433505bf4")
        elif link == "maya":
            self.show_maya_qr()

    def show_maya_qr(self):
        """Show Maya QR code dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Donate via Maya")
        dialog.setFixedSize(300, 400)
        layout = QVBoxLayout(dialog)

        try:
            link = EncryptionManager.decrypt_resource(MAYA_QR_PATH, MAYA_QR_KEY)
        except Exception as e:
            error = QLabel(f"Failed to load QR code: {e}")
            error.setAlignment(Qt.AlignCenter)
            layout.addWidget(error)
            dialog.exec_()
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(image)

        label = QLabel()
        label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        message = QLabel(
            "Support the development of Cryptext Gen Pro by scanning the QR code with your preferred e-Wallet application.\nWe sincerely appreciate your contribution."
        )
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        btns = QHBoxLayout()
        btns.addStretch()
        close = QPushButton("Close")
        close.clicked.connect(dialog.accept)
        btns.addWidget(close)
        btns.addStretch()
        layout.addLayout(btns)

        dialog.exec_()

    def set_qr_pixmap(self, pixmap):
        """Set QR code pixmap display"""
        if pixmap:
            self.qr_label.setPixmap(pixmap)
        else:
            self.clear_qr()

    def clear_qr(self):
        """Clear QR code display"""
        self.qr_label.clear()
        self.qr_label.setText("QR Code will\nappear here")