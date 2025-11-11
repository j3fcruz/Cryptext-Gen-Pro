# utils/encryption.py
"""Encryption utilities for sensitive data"""
from cryptography.fernet import Fernet
from PyQt5.QtCore import QFile, QIODevice


class EncryptionManager:
    """Manages encryption operations"""

    @staticmethod
    def decrypt_resource(resource_path, key):
        """Decrypt encrypted resource file"""
        try:
            file = QFile(resource_path)
            if not file.open(QIODevice.ReadOnly):
                raise FileNotFoundError(f"Failed to open resource: {resource_path}")

            data = bytes(file.readAll())
            file.close()

            fernet = Fernet(key)
            decrypted = fernet.decrypt(data)
            return decrypted.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")