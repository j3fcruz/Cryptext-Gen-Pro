# ui/main_window.py
"""SecurePassPro - Main application window (Unicode-safe, PyInstaller-ready, robust)"""

import os
import sys
import warnings
import cv2
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QLabel,
    QMessageBox, QAction, QShortcut)
from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from app_config.app_config import (
    WORDLIST_PATH, ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    APP_NAME, APP_VERSION, LOGO_PATH
)

from PyQt5.QtGui import QKeySequence

from core.password_generator import PasswordGenerator
from core.passphrase_generator import PassphraseGenerator
from core.wordlist_loader import WordlistLoader
from core.strength_analyzer import StrengthAnalyzer
from core.qr_handler import QRHandler
from utils.clipboard_manager import ClipboardManager
from utils.file_handler import FileHandler
from dialogs.Help_Dialog import HelpDialog
from dialogs.About_Dialog import AboutDialog
from dialogs.Donate_Dialog import DonateDialog
import resources_rc

#Silences Python DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --------------------------
# Logger Setup (Unicode-safe)
# --------------------------
def setup_logger(log_file="CryptextGenPro.log"):
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler with UTF-8 and replacement for invalid chars
    fh = logging.FileHandler(log_file, encoding="utf-8", errors="replace")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# --------------------------
# Safe OpenCV Initialization
# --------------------------
try:
    if hasattr(cv2, "setLogLevel"):
        cv2.setLogLevel(cv2.LOG_LEVEL_SILENT)
except Exception:
    pass
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
logging.getLogger("pyzbar").setLevel(logging.ERROR)


# --------------------------
# Main Window
# --------------------------
class SecurePassPro(QMainWindow):
    """Professional Password Generator with QR Code Support"""

    def __init__(self):
        super().__init__()

        self.logger = setup_logger()
        self.logger.info(f"Launching {APP_NAME} v{APP_VERSION}")

        try:
            self.DICEWARE_WORDS = self._load_wordlist(r"assets\wordlist\eff_file.wordlist")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load wordlist:\n{e}")
            self.DICEWARE_WORDS = []

        # Initialize core components
        self.password_gen = PasswordGenerator()
        self.strength_analyzer = StrengthAnalyzer()
        self.qr_handler = QRHandler()
        self.file_handler = FileHandler()
        self.clipboard_manager = ClipboardManager()

        self.password_visible = False
        self.current_qr_image = None
        self.logo_path = LOGO_PATH

        # Load wordlist safely
        self.passphrase_gen = PassphraseGenerator(self._load_wordlist())

        # State tracking
        self.current_qr_image = None
        self.visibility_states = {"password": False, "passphrase": False}

        # Initialize UI
        self.init_ui()

        # After menu bar creation
        self.init_shortcuts()

    # --------------------------
    # Wordlist loader with fallback
    # --------------------------
    def _load_wordlist(self, path=r"assets\wordlist\eff_file.wordlist"):
        """Load words from an external Diceware/EFF wordlist file"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Wordlist file not found: {path}")

        words = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # EFF wordlists usually have "12345\tword"
                parts = line.split()
                if len(parts) == 2:
                    words.append(parts[1])
                else:
                    words.append(parts[0])  # fallback if no numbers
        return words

    # --------------------------
    # UI Initialization
    # --------------------------
    def init_ui(self):
        """Initialize UI safely with cross-platform icon handling (PyInstaller-ready)."""
        try:
            from PyQt5.QtGui import QIcon
            from ui.widgets.control_panel import ControlPanel
            from ui.widgets.info_panel import InfoPanel

            self.setWindowTitle(WINDOW_TITLE)
            self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

            # --------------------------
            # Robust Icon Loading (works in PyInstaller, Windows, Linux, macOS)
            # --------------------------
            try:
                if getattr(sys, 'frozen', False):
                    # Running in a PyInstaller bundle
                    base_path = sys._MEIPASS
                else:
                    # Running in normal Python mode
                    base_path = os.path.dirname(os.path.abspath(__file__))

                possible_paths = [
                    ICON_PATH,  # from app_config
                    os.path.join(base_path, "assets", "icons", "icon.ico"),
                    os.path.join(base_path, "assets", "icon.ico"),
                    os.path.join(os.getcwd(), "assets", "icons", "icon.ico"),
                    ":/assets/icons/icon.ico"  # Qt resource path fallback
                ]

                icon_loaded = False
                for path in possible_paths:
                    if path and (path.startswith(":/") or os.path.exists(path)):
                        self.setWindowIcon(QIcon(path))
                        icon_loaded = True
                        self.logger.info(f"✅ App icon loaded successfully from: {path}")
                        break

                if not icon_loaded:
                    self.logger.warning("⚠️ No valid icon found — using default Qt window icon.")
            except Exception as e:
                self.logger.warning(f"⚠️ Icon load error: {e}")

            # --------------------------
            # Layout and Core Panels
            # --------------------------
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            layout = QHBoxLayout(central_widget)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            self.control_panel = ControlPanel(self)
            self.info_panel = InfoPanel(self)

            layout.addWidget(self.control_panel, 2)
            layout.addWidget(self.info_panel, 1)

            # --------------------------
            # Status Bar with Clock
            # --------------------------
            self.statusBar().showMessage("Ready")
            self.clock_label = QLabel()
            self.statusBar().addPermanentWidget(self.clock_label)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_clock)
            self.timer.start(1000)
            self.update_clock()

            # --------------------------
            # Menu Bar
            # --------------------------
            self.create_menu_bar()

        except Exception as e:
            self.logger.error(f"UI initialization failed: {e}")
            QMessageBox.critical(self, "UI Error",
                                 f"Failed to initialize UI:\n{e}")

    def init_shortcuts(self):
        """Define global shortcut keys consistent with HelpDialog"""
        # Password Actions
        QShortcut(QKeySequence("Ctrl+G"), self).activated.connect(
            lambda: self.control_panel.password_tab.generate_btn.click()
        )
        QShortcut(QKeySequence("Ctrl+C"), self).activated.connect(
            lambda: self.control_panel.password_tab.copy_btn.click()
        )
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(
            lambda: self.control_panel.password_tab.save_qr_btn.click()
        )
        # SAFE Ctrl+S
        from PyQt5.QtCore import QTimer
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(
            lambda: QTimer.singleShot(0, self.control_panel.password_tab.save_qr_btn.click)
        )
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(
            lambda: self.control_panel.password_tab.clear_all()
        )
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(
            lambda: QMessageBox.information(
                self,
                "Theme",
                "Single Indigo Dark theme is active.\nTheme customization coming soon!"
            )
        )

        # Help & Documentation
        QShortcut(QKeySequence("F1"), self).activated.connect(self.show_help_dialog)

    # --------------------------
    # Menu Bar
    # --------------------------
    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)

        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help_dialog)

        donate_action = QAction("Donate", self)
        donate_action.triggered.connect(self.show_donate_dialog)

        help_menu.addAction(about_action)
        help_menu.addAction(help_action)
        help_menu.addAction(donate_action)

    # --------------------------
    # Dialogs (Safe)
    # --------------------------
    def show_about_dialog(self): AboutDialog(self).exec_()
    def show_donate_dialog(self): DonateDialog(self).exec_()
    def show_help_dialog(self): HelpDialog(self).exec_()
    def show_terms_conditions_dialog(self): TermsConditionsDialog(self).exec_()
    def show_license_dialog(self): LicenseDialog(self).exec_()

    # --------------------------
    # Clock
    # --------------------------
    def update_clock(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        current_date = QDate.currentDate().toString("yyyy-MM-dd dddd")
        self.clock_label.setText(f"{current_date}   {current_time}")

    # --------------------------
    # Close Event
    # --------------------------
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Do you really want to quit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.logger.info("Application exited by user.")
            event.accept()
        else:
            event.ignore()
