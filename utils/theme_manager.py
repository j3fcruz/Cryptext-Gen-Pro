"""
theme_manager.py
----------------
Centralized theme management for Enhanced Notepad Pro.
Handles system dark/light mode detection, auto-reload, and safe fallback QSS.
"""

import os
import sys
import time
from threading import Thread
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from config.app_config import DEFAULT_THEME_QSS, DARK_THEME_QSS, LIGHT_THEME_QSS

# -----------------------------------------------------
# Helper: Get Absolute Resource Path
# -----------------------------------------------------
def resource_path(relative_path: str) -> str:
    """Return absolute path to resource, works in dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -----------------------------------------------------
# System Theme Detection
# -----------------------------------------------------
def is_dark_mode_enabled() -> bool:
    """Detect Windows system dark mode. Default to dark if unknown."""
    try:
        if sys.platform == "win32":
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0  # 0 = dark, 1 = light
    except Exception:
        pass
    return True  # default to dark

# -----------------------------------------------------
# Built-in QSS Fallbacks
# -----------------------------------------------------
def get_dark_theme(font_size=14):
    return f"""
    QMainWindow {{ background-color: #242424; }}
    QPlainTextEdit {{
        background-color: #1e1e1e;
        color: #dcdcdc;
        font-size: {font_size}px;
        font-family: Consolas, monospace;
        selection-background-color: #004b90;
    }}
    QMenuBar, QMenu, QStatusBar {{ background-color: #333; color: #dcdcdc; }}
    QPushButton {{
        background-color: #3a3a3a;
        color: #ffffff;
        border-radius: 6px;
        padding: 4px 10px;
    }}
    QPushButton:hover {{ background-color: #505050; }}
    """

def get_light_theme(font_size=14):
    return f"""
    QMainWindow {{ background-color: #fafafa; }}
    QPlainTextEdit {{
        background-color: #ffffff;
        color: #222222;
        font-size: {font_size}px;
        font-family: Consolas, monospace;
        selection-background-color: #3399ff;
    }}
    QMenuBar, QMenu, QStatusBar {{ background-color: #eaeaea; color: #111; }}
    QPushButton {{
        background-color: #f0f0f0;
        color: #111;
        border-radius: 6px;
        padding: 4px 10px;
    }}
    QPushButton:hover {{ background-color: #dcdcdc; }}
    """

# -----------------------------------------------------
# Load Theme (Default Mode Only)
# -----------------------------------------------------
def load_theme(app: QApplication, base_path="assets/themes/") -> bool:
    """Always load default theme safely with resource fallback."""
    theme_file = "dark_theme.qss"
    qrc_path = f":/assets/themes/{theme_file}"
    local_path = resource_path(os.path.join(base_path, theme_file))

    # Try embedded resource
    file = QFile(qrc_path)
    if file.exists() and file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
        file.close()
        print(f"[Theme] ✅ Loaded default theme from resource → {qrc_path}")
        return True

    # Try local file
    if os.path.exists(local_path):
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
            print(f"[Theme] ✅ Loaded default theme from local folder → {local_path}")
            return True
        except Exception as e:
            print(f"[Theme] ⚠️ Failed to load local default theme: {e}")

    # Fallback built-in
    print(f"[Theme] ⚠️ No theme found. Applying built-in default theme.")
    app.setStyleSheet(get_dark_theme())
    return False


# -----------------------------------------------------
# Apply theme to any child/dialog
# -----------------------------------------------------
def apply_global_theme(widget):
    """Apply current global QSS to a widget."""
    app = QApplication.instance()
    if app:
        widget.setStyleSheet(app.styleSheet())

# -----------------------------------------------------
# Optional: Live Theme Watcher (Windows Only) - optional
# -----------------------------------------------------
def watch_theme(app: QApplication, interval=3):
    """Continuously watch system theme changes."""
    if sys.platform != "win32":
        return
    def _watch():
        last_state = is_dark_mode_enabled()
        while True:
            time.sleep(interval)
            current_state = is_dark_mode_enabled()
            if current_state != last_state:
                print(f"[Theme] 🔄 System theme changed → {'Dark' if current_state else 'Light'}")
                load_theme(app)
                last_state = current_state
    Thread(target=_watch, daemon=True).start()
