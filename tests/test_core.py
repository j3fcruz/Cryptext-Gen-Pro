import string

import pytest

from core.password_generator import PasswordGenerator
from core.strength_analyzer import StrengthAnalyzer


def test_basic_generation_has_requested_length_and_all_selected_groups():
    gen = PasswordGenerator()
    password = gen.generate_basic(64, True, True, True, True)
    assert len(password) == 64
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in gen.symbols for c in password)


def test_basic_generation_rejects_empty_charset():
    gen = PasswordGenerator()
    with pytest.raises(ValueError):
        gen.generate_basic(16, False, False, False, False)


def test_advanced_generation_is_unique_and_no_adjacent_type_repeats():
    gen = PasswordGenerator()
    password = gen.generate_advanced(32, True, True, True, True)
    assert len(password) == 32
    assert len(set(password)) == len(password)

    def kind(ch):
        if ch in string.ascii_lowercase:
            return "lower"
        if ch in string.ascii_uppercase:
            return "upper"
        if ch in string.digits:
            return "digit"
        return "symbol"

    assert all(kind(a) != kind(b) for a, b in zip(password, password[1:]))


def test_strength_analyzer_empty_input():
    result = StrengthAnalyzer().analyze("")
    assert result["entropy"] == 0
    assert result["progress"] == 0
    assert result["strength"] == "Very Weak"
