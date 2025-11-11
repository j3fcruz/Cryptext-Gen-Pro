"""
utils/icon_manager.py
---------------
Enterprise-grade icon loader for Enhanced Notepad Pro.
Supports Qt resources and local fallback for PyInstaller.
"""

import os
import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

# -----------------------------------------------------
# Helper: Get Absolute Path
# -----------------------------------------------------
def resource_path(relative_path: str) -> str:
    """Get absolute path to resource (works in dev and PyInstaller)."""
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -----------------------------------------------------
# Load Icon
# -----------------------------------------------------
def load_icon(name: str = "icon.png") -> QIcon:
    """
    Load icon from Qt resource or local folder.
    Fallback: transparent 32x32 QIcon.
    """
    # Try Qt resource
    qrc_path = f":/assets/icons/{name}"
    icon = QIcon(qrc_path)
    if not icon.isNull():
        return icon

    # Try local file
    local_path = resource_path(os.path.join("assets", "icons", name))
    if os.path.exists(local_path):
        icon = QIcon(local_path)
        if not icon.isNull():
            return icon

    # Fallback: transparent placeholder
    placeholder = QPixmap(32, 32)
    placeholder.fill(Qt.transparent)
    return QIcon(placeholder)

# -----------------------------------------------------
# Apply App Icon
# -----------------------------------------------------
def set_app_icon(app, name: str = "icon.png") -> QIcon:
    """Set application-wide icon."""
    icon = load_icon(name)
    app.setWindowIcon(icon)
    return icon
