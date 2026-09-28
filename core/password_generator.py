# core/password_generator.py
"""Password generation logic - cryptographically secure"""
import string
import secrets
from app_config.app_config import SYMBOLS, LOGO_PATH


class PasswordGenerator:
    """Generates cryptographically secure passwords"""

    def __init__(self, symbols=None, logo_path=None):
        self.symbols = symbols or SYMBOLS
        self.logo_path = logo_path or LOGO_PATH

    def generate_basic(self, length, use_upper=True, use_lower=True, use_numbers=True, use_symbols=True):
        """Generate password using basic method (fast)

        Args:
            length: Password length
            use_upper: Include uppercase letters
            use_lower: Include lowercase letters
            use_numbers: Include numbers
            use_symbols: Include special symbols

        Returns:
            Generated password string

        Raises:
            ValueError: If no character type selected
        """
        groups = self._build_groups(use_upper, use_lower, use_numbers, use_symbols)
        if not groups:
            raise ValueError("At least one character type must be selected")
        if length < len(groups):
            raise ValueError("Password length is too short for the selected character types")

        # Guarantee at least one character from every selected group, then fill
        # the remaining positions using the combined charset.
        chars = [secrets.choice(group_chars) for _, group_chars in groups]
        charset = "".join(group_chars for _, group_chars in groups)
        chars.extend(secrets.choice(charset) for _ in range(length - len(chars)))
        secrets.SystemRandom().shuffle(chars)
        return "".join(chars)

    def generate_advanced(self, length, use_upper=True, use_lower=True, use_numbers=True, use_symbols=True):
        """Generate password with no consecutive types and no repetitions

        Args:
            length: Password length
            use_upper: Include uppercase letters
            use_lower: Include lowercase letters
            use_numbers: Include numbers
            use_symbols: Include special symbols

        Returns:
            Generated password string with mixed character types

        Raises:
            ValueError: If no character type selected or length too long
        """
        groups = self._build_groups(use_upper, use_lower, use_numbers, use_symbols)
        if not groups:
            raise ValueError("At least one character type must be selected")

        if length > self._count_unique_chars(groups):
            raise ValueError("Password length too long to ensure unique characters")

        password_chars = []
        used_chars = set()
        last_group = None

        # Ensure at least one char from each group
        for name, chars in groups:
            ch = self._pick_char(chars, used_chars)
            if ch:
                password_chars.append((name, ch))
                used_chars.add(ch)
                last_group = name

        # Fill remaining positions
        while len(password_chars) < length:
            candidates = [g for g in groups if g[0] != last_group] or groups
            name, chars = secrets.choice(candidates)
            ch = self._pick_char(chars, used_chars)
            if not ch:
                break  # fallback if no unique chars left
            password_chars.append((name, ch))
            used_chars.add(ch)
            last_group = name

        return "".join(ch for _, ch in password_chars)

    def _build_charset(self, use_upper, use_lower, use_numbers, use_symbols):
        """Build character set from options"""
        charset = ""
        if use_lower:
            charset += string.ascii_lowercase
        if use_upper:
            charset += string.ascii_uppercase
        if use_numbers:
            charset += string.digits
        if use_symbols:
            charset += self.symbols
        return charset

    def _build_groups(self, use_upper, use_lower, use_numbers, use_symbols):
        """Build character groups"""
        groups = []
        if use_lower:
            groups.append(('lowercase', string.ascii_lowercase))
        if use_upper:
            groups.append(('uppercase', string.ascii_uppercase))
        if use_numbers:
            groups.append(('digit', string.digits))
        if use_symbols:
            groups.append(('symbol', self.symbols))
        return groups

    def _pick_char(self, chars, used_chars):
        """Pick unused character from set"""
        available = [c for c in chars if c not in used_chars]
        return secrets.choice(available) if available else None

    def _count_unique_chars(self, groups):
        """Count unique characters across all groups"""
        return len(set(c for _, chars in groups for c in chars))

    def get_logo_path(self):
        """Get the logo path for QR code embedding"""
        return self.logo_path

    def set_logo_path(self, path):
        """Set the logo path for QR code embedding"""
        self.logo_path = path
