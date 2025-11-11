# ---------------------------------------------------------
# 🔐 Cryptext Gen Pro - Config (Environment-based)
# ---------------------------------------------------------

import os
import sys
from dotenv import load_dotenv

# ---------------------------------------------------------
# 📦 Safe Logging
# ---------------------------------------------------------
def safe_log(msg: str):
    """Safe logging (avoids IDE or PyInstaller crashes)."""
    try:
        print(msg)
    except Exception:
        pass


safe_log("🔹 Initializing Cryptext Gen Pro config...")

# ---------------------------------------------------------
# 🌍 Load .env File (Development Mode)
# ---------------------------------------------------------
ENV_FILE = ".env"
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    safe_log(f"⚠️ Warning: {ENV_FILE} not found. Using default values.")

# ---------------------------------------------------------
# 📦 Resource Path (Supports PyInstaller)
# ---------------------------------------------------------
def resource_path(relative_path: str) -> str:
    """Resolve absolute path to a resource."""
    if relative_path.startswith(":/"):
        relative_path = relative_path[2:]  # remove leading :/
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        path = os.path.join(base_path, relative_path)
        if os.path.exists(path):
            return path

        # Fallbacks
        alt_path = os.path.join(os.getcwd(), relative_path)
        if os.path.exists(alt_path):
            return alt_path

        assets_path = os.path.join(os.getcwd(), "assets", os.path.basename(relative_path))
        if os.path.exists(assets_path):
            return assets_path

        safe_log(f"❌ Resource not found: {relative_path}")
        return relative_path
    except Exception as e:
        safe_log(f"⚠️ Resource path error for {relative_path}: {e}")
        return relative_path



# ---------------------------------------------------------
# 🧱 Application Metadata
# ---------------------------------------------------------
APP_NAME = os.getenv("APP_NAME", "Cryptext Gen Pro")
HASH_NAME = os.getenv("HASH_NAME", "cryptextgenpro")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
AUTHOR = os.getenv("AUTHOR", "Marco Polo")
APP_DEVELOPER = os.getenv("APP_DEVELOPER", "PatronHubDevs")
COPYRIGHT_YEAR = os.getenv("COPYRIGHT_YEAR", "2025")
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
COPYRIGHT = f"© {COPYRIGHT_YEAR} {APP_NAME}. All rights reserved."

ABOUT_APP = os.getenv(
    "ABOUT_APP",
    "Next-Gen Password Generation – Secured by Design."
)

DESCRIPTION = os.getenv(
    "DESCRIPTION",
    f"""{APP_NAME} by {AUTHOR} is a professional-grade password generator 
and secure note manager. Cryptext Gen Pro combines advanced encryption, 
QR code support, and a sleek, modern interface to help you safely generate, 
store, and manage passwords and sensitive information."""
)

# ---------------------------------------------------------
# 🖼️ Resource & Asset Paths
# ---------------------------------------------------------
ICON_PATH = resource_path(os.getenv("ICON_PATH", ":/assets/icons/icon.ico"))
LOGO_PATH = resource_path(os.getenv("LOGO_PATH", ":/assets/logo/logo.ico"))
ABOUT_ICON_PATH = resource_path(":/assets/icons/about_icon.png")
DONATE_ICON_PATH = resource_path(":/assets/icons/donate_icon.png")
HELP_ICON_PATH = resource_path(":/assets/icons/help_icon.png")
LICENSE_ICON_PATH = resource_path(":/assets/icons/license_icon.png")
SAVE_ICON_PATH = resource_path(":/assets/icons/save_icon.ico")
TERMS_ICON_PATH = resource_path(":/assets/icons/terms_icon.png")

# Wordlist
#_default_wordlist = os.path.join("assets", "wordlist", "eff_file.wordlist")
WORDLIST_PATH = resource_path(os.getenv("WORDLIST_PATH", ":/assets/wordlist/eff_file.wordlist"))

if not os.path.exists(WORDLIST_PATH):
    safe_log(f"❌ Wordlist file not found: {WORDLIST_PATH}")
    WORDLIST_PATH = None
else:
    safe_log(f"✅ Wordlist loaded successfully: {WORDLIST_PATH}")

MAYA_QR_PATH = resource_path(os.getenv("MAYA_QR_PATH", ":/assets/resources/maya_qr.bin"))
MAYA_QR_KEY = os.getenv("MAYA_QR_KEY", "").encode()

# ---------------------------------------------------------
# 🧩 UI & Generation Settings
# ---------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 850
QR_SIZE = 220

DEFAULT_PASSWORD_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 94

# Passphrase
MIN_WORDS = 3
MAX_WORDS = 12
DEFAULT_WORDS = 4
DEFAULT_SEPARATOR = "-"

# QR Code
QR_VERSION = 1
QR_ERROR_CORRECTION = "H"
QR_BOX_SIZE = 10
QR_BORDER = 4
QR_LOGO_RATIO = 0.25

# Password Generation
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
MAX_GENERATION_ATTEMPTS = 100000

# Camera Settings
MAX_CAMERA_ATTEMPTS = 5
CAMERA_BACKEND = "DSHOW"  # Windows specific; use "" for cross-platform

# ---------------------------------------------------------
# 🌐 External Links
# ---------------------------------------------------------
GITHUB_ID = os.getenv("GITHUB_ID", "https://github.com/j3fcruz/Cryptext-Gen-Pro")
KOFI_ID = os.getenv("KOFI_ID", "https://ko-fi.com/marcopolo55681")
PAYPAL_ID = os.getenv("PAYPAL_ID", "https://paypal.me/jofreydelacruz13")

BTC_NAME = os.getenv("BTC_NAME", "Bitcoin (BTC) Address")
BTC_ID = os.getenv("BTC_ID", "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk")

ETH_NAME = os.getenv("ETH_NAME", "Ethereum (ETH) Address")
ETH_ID = os.getenv("ETH_ID", "0xcd5eef32ff4854e4cefa13cb308b727433505bf4")

# ---------------------------------------------------------
# ⚙️ Environment & Themes
# ---------------------------------------------------------
APP_ENV = os.getenv("APP_ENV", "production").lower()
IS_PRODUCTION = APP_ENV == "production"
IS_DEVELOPMENT = APP_ENV == "development"

APPLY_THEME = resource_path(os.getenv("APP_THEME", ":/assets/themes/default_theme.qss"))
DARK_THEME_QSS = resource_path(os.getenv("DARK_THEME", ":/assets/themes/dark_theme.qss"))
LIGHT_THEME_QSS = resource_path(os.getenv("LIGHT_THEME", ":/assets/themes/light_theme.qss"))


safe_log(f"✅ Cryptext Gen Pro config loaded successfully ({APP_ENV.upper()} MODE)")








