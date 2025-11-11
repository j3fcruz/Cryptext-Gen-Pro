"""Application entry point (Unicode-safe, PyInstaller-ready, with app icon)"""
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import SecurePassPro
from ui.styles import StyleManager
from app_config.app_config import APP_NAME, APP_VERSION, ICON_PATH


def get_app_icon():
    """Resolve app icon path robustly for all platforms and PyInstaller builds."""
    try:
        if getattr(sys, 'frozen', False):
            # Running inside PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Normal script run
            base_path = os.path.dirname(os.path.abspath(__file__))

        possible_paths = [
            ICON_PATH,  # defined in app_config
            os.path.join(base_path, "assets", "icons", "app_icon.png"),
            os.path.join(base_path, "assets", "app_icon.png"),
            os.path.join(os.getcwd(), "assets", "icons", "app_icon.png"),
            ":/assets/icons/app_icon.png",  # Qt resource fallback
        ]

        for path in possible_paths:
            if path and (path.startswith(":/") or os.path.exists(path)):
                return QIcon(path)
    except Exception as e:
        print(f"⚠️ Icon resolution error: {e}")

    print("⚠️ No valid icon found — using default Qt icon.")
    return QIcon()  # fallback (Qt default)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_NAME)
    app.setStyle("Fusion")

    # Apply global app icon (affects window, taskbar, and Dock on macOS)
    icon = get_app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)

        # macOS Dock icon support (optional)
        if sys.platform == "darwin":
            try:
                import ctypes
                from AppKit import NSApplication, NSImage
                ns_app = NSApplication.sharedApplication()
                ns_icon = NSImage.alloc().initByReferencingFile_(icon.name())
                if ns_icon:
                    ns_app.setApplicationIconImage_(ns_icon)
            except Exception:
                pass

    # Apply theme safely
    if not StyleManager.load_stylesheet(app):
        StyleManager.apply_fallback_theme(app, dark_mode=True)

    # Launch main window
    window = SecurePassPro()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
