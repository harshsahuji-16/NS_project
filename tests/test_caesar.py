"""Unit tests for Caesar Cipher."""

import pytest
from crypto.caesar import encrypt_caesar, decrypt_caesar, get_caesar_steps


def test_caesar_reference_test_case():
    """Verify exact reference test case specified in project prompt."""
    plaintext = "NETWORK SECURITY"
    key = 5
    expected_ciphertext = "SJYBTWP XJHZWNYD"

    ciphertext = encrypt_caesar(plaintext, key)
    assert ciphertext == expected_ciphertext

    decrypted = decrypt_caesar(ciphertext, key)
    assert decrypted == plaintext


def test_caesar_case_and_punctuation_preservation():
    """Verify that lowercase, uppercase, spaces, and punctuation are preserved."""
    plaintext = "Hello, World! 123"
    key = 3
    ciphertext = encrypt_caesar(plaintext, key)
    assert ciphertext == "Khoor, Zruog! 123"

    decrypted = decrypt_caesar(ciphertext, key)
    assert decrypted == plaintext


def test_caesar_negative_and_oversized_keys():
    """Verify modulo 26 arithmetic handles negative and oversized keys."""
    plaintext = "Cryptography"
    key_normal = 3
    key_oversized = 29  # 29 % 26 == 3
    key_negative = -23  # -23 % 26 == 3

    c1 = encrypt_caesar(plaintext, key_normal)
    c2 = encrypt_caesar(plaintext, key_oversized)
    c3 = encrypt_caesar(plaintext, key_negative)

    assert c1 == c2 == c3
    assert decrypt_caesar(c1, key_oversized) == plaintext
    assert decrypt_caesar(c1, key_negative) == plaintext


def test_caesar_empty_string():
    """Verify behavior on empty string."""
    assert encrypt_caesar("", 7) == ""
    assert decrypt_caesar("", 7) == ""


def test_caesar_zero_key():
    """Verify shift of 0 leaves text unchanged."""
    text = "Secret Message"
    assert encrypt_caesar(text, 0) == text
    assert decrypt_caesar(text, 0) == text


def test_caesar_invalid_key_type():
    """Verify that non-integer keys raise TypeError."""
    with pytest.raises(TypeError):
        encrypt_caesar("Test", "invalid_key")  # type: ignore

    with pytest.raises(TypeError):
        decrypt_caesar("Test", 3.14)  # type: ignore


def test_caesar_steps_generation():
    """Verify educational transformation step generator."""
    steps = get_caesar_steps("ABC", 3, mode="encrypt")
    assert len(steps) == 3
    assert steps[0]["char"] == "A"
    assert steps[0]["result"] == "D"
