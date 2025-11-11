# core/wordlist_loader.py
"""Wordlist loading and management"""
import os
from PyQt5.QtCore import QFile, QIODevice, QTextStream


class WordlistLoader:
    """Loads wordlists from files and Qt resources"""

    @staticmethod
    def load(path):
        """Load wordlist from file or Qt resource

        Args:
            path: File path or Qt resource path (:/path/to/file)

        Returns:
            List of words, or empty list if loading fails
        """
        if not path:
            return []

        # Try Qt resource path first (:/path/to/file)
        if isinstance(path, str) and path.startswith(":/"):
            words = WordlistLoader._load_from_resource(path)
            if words:
                return words

        # Try regular file path
        words = WordlistLoader._load_from_file(path)
        if words:
            return words

        # Try fallback paths
        fallback_paths = [
            "assets/wordlist/eff_file.wordlist",
            "wordlist/eff_file.wordlist",
            "./eff_file.wordlist",
            "../assets/wordlist/eff_file.wordlist",
        ]

        for fallback_path in fallback_paths:
            words = WordlistLoader._load_from_file(fallback_path)
            if words:
                return words

        return []

    @staticmethod
    def _load_from_file(file_path):
        """Load wordlist from regular file path

        Args:
            file_path: Path to wordlist file

        Returns:
            List of words, or empty list if file not found
        """
        try:
            if not os.path.exists(file_path):
                return []

            with open(file_path, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]

            return words
        except Exception:
            return []

    @staticmethod
    def _load_from_resource(resource_path):
        """Load wordlist from Qt resource

        Args:
            resource_path: Qt resource path (:/path/to/file)

        Returns:
            List of words, or empty list if resource not found
        """
        try:
            qfile = QFile(resource_path)
            if not qfile.open(QIODevice.ReadOnly | QIODevice.Text):
                return []

            stream = QTextStream(qfile)
            content = stream.readAll()
            qfile.close()

            words = [line.strip() for line in content.split('\n') if line.strip()]
            return words
        except Exception:
            return []

    @staticmethod
    def is_valid(wordlist):
        """Check if wordlist is valid

        Args:
            wordlist: List of words

        Returns:
            True if wordlist has words, False otherwise
        """
        return bool(wordlist and len(wordlist) > 0)