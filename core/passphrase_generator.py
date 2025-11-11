# core/passphrase_generator.py
"""Passphrase generation from wordlist"""
import secrets
import os
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from app_config.app_config import *

class WordlistManager:
    """Manages wordlist loading from files and Qt resources"""

    @staticmethod
    def load_from_file(path):
        """Load wordlist from file path"""
        if not path or not os.path.exists(path):
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
            return words
        except Exception:
            return []

    @staticmethod
    def load_from_resource(resource_path):
        """Load wordlist from Qt resource (:/path/to/file)"""
        qfile = QFile(resource_path)
        if not qfile.open(QIODevice.ReadOnly | QIODevice.Text):
            return []

        try:
            stream = QTextStream(qfile)
            content = stream.readAll()
            words = [line.strip() for line in content.split('\n') if line.strip()]
            return words
        except Exception:
            return []
        finally:
            qfile.close()

    @staticmethod
    def load(path):
        """Load wordlist from file or Qt resource"""
        # If path starts with :/, it's a Qt resource
        if path and path.startswith(":/"):
            return WordlistManager.load_from_resource(path)

        # Otherwise try regular file path
        words = WordlistManager.load_from_file(path)
        if words:
            return words

        # Fallback: try common local paths
        fallback_paths = [
            "assets/wordlist/eff_file.wordlist",
            "wordlist/eff_file.wordlist",
            "./eff_file.wordlist",
        ]

        for fallback_path in fallback_paths:
            words = WordlistManager.load_from_file(fallback_path)
            if words:
                return words

        return []


class PassphraseGenerator:
    """Generates passphrases from word lists"""

    def __init__(self, wordlist=None):
        """Initialize with wordlist

        Args:
            wordlist: List of words. If None, uses fallback empty list.
        """
        if wordlist is None:
            wordlist = []

        self.wordlist = wordlist if wordlist else []

    def generate(self, num_words, separator="-", word_case="lowercase"):
        """Generate passphrase with specified parameters

        Args:
            num_words: Number of words in passphrase
            separator: String to join words (default: "-")
            word_case: Case transformation ("lowercase", "uppercase", "title case", "random case")

        Returns:
            Generated passphrase string

        Raises:
            ValueError: If wordlist is empty
        """
        if not self.wordlist:
            raise ValueError("Wordlist is empty. Cannot generate passphrase.")

        words = [secrets.choice(self.wordlist) for _ in range(num_words)]
        words = self._apply_case(words, word_case)

        return separator.join(words) if separator else "".join(words)

    def _apply_case(self, words, case_mode):
        """Apply case transformation to words"""
        result = []
        for word in words:
            case_lower = case_mode.lower() if case_mode else "lowercase"

            if case_lower == "uppercase":
                result.append(word.upper())
            elif case_lower == "title case":
                result.append(word.title())
            elif case_lower == "random case":
                result.append("".join(
                    c.upper() if secrets.randbelow(2) else c.lower() for c in word
                ))
            else:  # Lowercase (default)
                result.append(word.lower())

        return result

    def is_ready(self):
        """Check if generator has a valid wordlist"""
        return bool(self.wordlist)