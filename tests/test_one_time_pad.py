"""Unit tests for One-Time Pad."""

import pytest
from crypto.one_time_pad import (
    encrypt_otp,
    decrypt_otp,
    generate_otp_key,
    validate_otp_key,
    OTP_SECURITY_WARNING,
)


def test_otp_key_generation():
    """Verify cryptographically secure random key generation."""
    key = generate_otp_key(10)
    assert len(key) == 10
    assert key.isalpha()
    assert key.isupper()


def test_otp_round_trip():
    """Verify round-trip encryption and decryption with generated key."""
    plaintext = "Network Security Final Year Project 2026!"
    alpha_count = sum(1 for c in plaintext if c.isalpha())
    key = generate_otp_key(alpha_count)

    ciphertext, key_used = encrypt_otp(plaintext, key)
    assert ciphertext != plaintext
    assert key_used == key

    decrypted = decrypt_otp(ciphertext, key)
    assert decrypted == plaintext


def test_otp_insufficient_key_length():
    """Verify error raised when key is shorter than message alphabetic characters."""
    plaintext = "CONFIDENTIAL MESSAGE"
    short_key = "ABC"

    is_val, msg = validate_otp_key(short_key, len(plaintext))
    assert is_val is False
    assert "too short" in msg.lower()

    with pytest.raises(ValueError):
        encrypt_otp(plaintext, short_key)


def test_otp_warning_content():
    """Verify presence of security education warning."""
    assert "NEVER reused" in OTP_SECURITY_WARNING
    assert "information-theoretically secure" in OTP_SECURITY_WARNING
