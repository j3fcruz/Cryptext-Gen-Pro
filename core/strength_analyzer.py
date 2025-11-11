# core/strength_analyzer.py
"""Password strength analysis and entropy calculation"""
import math
import string


class StrengthAnalyzer:
    """Analyzes password strength and entropy"""

    def analyze(self, password):
        """Analyze password and return strength metrics"""
        if not password:
            return {
                "entropy": 0,
                "strength": "Very Weak",
                "color": "#d32f2f",
                "crack_time": "Instant",
                "progress": 0
            }

        entropy = self._calculate_entropy(password)

        return {
            "entropy": entropy,
            "strength": self._get_strength_text(entropy),
            "color": self._get_strength_color(entropy),
            "crack_time": self._get_crack_time(entropy),
            "progress": min(int((entropy / 128) * 100), 100)
        }

    def _calculate_entropy(self, password):
        """Calculate Shannon entropy in bits"""
        charset_size = 0

        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)

        charset_size = max(charset_size, 1)
        return len(password) * math.log2(charset_size)

    def _get_strength_text(self, entropy):
        """Get strength level text"""
        levels = [
            (40, "Very Weak"),
            (56, "Weak"),
            (64, "Fair"),
            (80, "Good"),
            (96, "Strong"),
            (128, "Very Strong"),
        ]
        for threshold, text in levels:
            if entropy < threshold:
                return text
        return "Excellent"

    def _get_strength_color(self, entropy):
        """Get strength level color (hex)"""
        colors = [
            (40, "#d32f2f"),  # Red
            (56, "#f57c00"),  # Orange
            (64, "#fbc02d"),  # Yellow
            (80, "#689f38"),  # Light Green
            (96, "#388e3c"),  # Green
            (128, "#1976d2"),  # Blue
        ]
        for threshold, color in colors:
            if entropy < threshold:
                return color
        return "#7b1fa2"  # Purple (Excellent)

    def _get_crack_time(self, entropy):
        """Get estimated crack time"""
        times = [
            (40, "Instant"),
            (56, "Seconds"),
            (64, "Minutes"),
            (80, "Hours"),
            (96, "Days"),
            (112, "Months"),
            (128, "Years"),
        ]
        for threshold, time_str in times:
            if entropy < threshold:
                return time_str
        return "Centuries"