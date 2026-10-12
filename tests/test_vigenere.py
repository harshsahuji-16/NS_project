"""Unit tests for Vigenère Cipher."""

import pytest
from crypto.vigenere import (
    encrypt_vigenere,
    decrypt_vigenere,
    validate_vigenere_key,
    get_vigenere_steps,
)


def test_vigenere_known_text_reference():
    """Verify standard classical cryptography reference: 'ATTACKATDAWN' with key 'LEMON' -> 'LXFOPVEFRNHR'."""
    plaintext = "ATTACKATDAWN"
    keyword = "LEMON"
    expected_ciphertext = "LXFOPVEFRNHR"

    ciphertext = encrypt_vigenere(plaintext, keyword)
    assert ciphertext == expected_ciphertext

    decrypted = decrypt_vigenere(ciphertext, keyword)
    assert decrypted == plaintext


def test_vigenere_case_and_punctuation_preservation():
    """Verify spaces and punctuation do not advance key index, and casing is preserved."""
    plaintext = "Attack at Dawn, 0600!"
    keyword = "LEMON"
    ciphertext = encrypt_vigenere(plaintext, keyword)
    assert ciphertext == "Lxfopv ef Rnhr, 0600!"

    decrypted = decrypt_vigenere(ciphertext, keyword)
    assert decrypted == plaintext


def test_vigenere_key_validation():
    """Verify validation of keywords."""
    valid, msg = validate_vigenere_key("SECRET")
    assert valid is True

    valid, msg = validate_vigenere_key("12345")
    assert valid is False
    assert "at least one" in msg.lower()

    with pytest.raises(ValueError):
        encrypt_vigenere("Hello", "")


def test_vigenere_steps_generation():
    """Verify educational steps helper."""
    steps = get_vigenere_steps("ATTACK", "LEMON")
    assert len(steps) == 6
    assert steps[0]["char"] == "A"
    assert steps[0]["key_char"] == "L"
    assert steps[0]["result"] == "L"
