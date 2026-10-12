"""Unit tests for Monoalphabetic Substitution Cipher."""

import pytest
import string
from crypto.monoalphabetic import (
    encrypt_monoalphabetic,
    decrypt_monoalphabetic,
    generate_monoalphabetic_key,
    validate_monoalphabetic_key,
)


def test_monoalphabetic_key_generation():
    """Verify generated key is valid, contains 26 unique uppercase letters."""
    key = generate_monoalphabetic_key()
    is_valid, msg = validate_monoalphabetic_key(key)
    assert is_valid is True
    assert msg == ""
    assert len(key) == 26
    assert set(key) == set(string.ascii_uppercase)


def test_monoalphabetic_round_trip():
    """Verify lossless encryption and decryption."""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    plaintext = "Network Security Mini Project 2026!"
    ciphertext = encrypt_monoalphabetic(plaintext, key)
    assert ciphertext != plaintext

    decrypted = decrypt_monoalphabetic(ciphertext, key)
    assert decrypted == plaintext


def test_monoalphabetic_case_preservation():
    """Verify casing and punctuation are preserved."""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    plaintext = "AbC, xYz!"
    # 'A' maps to 'Q', 'b' maps to 'w', 'C' maps to 'E'
    # 'x' maps to 'b', 'Y' maps to 'N', 'z' maps to 'm'
    ciphertext = encrypt_monoalphabetic(plaintext, key)
    assert ciphertext == "QwE, bNm!"
    assert decrypt_monoalphabetic(ciphertext, key) == plaintext


def test_monoalphabetic_invalid_keys():
    """Verify rejection of short, long, non-alphabetic, or duplicate keys."""
    # Too short
    valid, msg = validate_monoalphabetic_key("ABC")
    assert valid is False
    assert "26 letters" in msg

    # Duplicate letters
    dup_key = "A" * 26
    valid, msg = validate_monoalphabetic_key(dup_key)
    assert valid is False
    assert "UNIQUE" in msg

    # Contains numbers
    bad_chars = "QWERTYUIOPASDFGHJKLZXCVBN1"
    valid, msg = validate_monoalphabetic_key(bad_chars)
    assert valid is False

    with pytest.raises(ValueError):
        encrypt_monoalphabetic("Hello", "INVALID_KEY")


def test_monoalphabetic_empty_text():
    """Verify empty text handling."""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert encrypt_monoalphabetic("", key) == ""
    assert decrypt_monoalphabetic("", key) == ""
