"""Unit tests for Columnar Transposition Cipher."""

import pytest
from crypto.columnar_transposition import (
    encrypt_columnar,
    decrypt_columnar,
    validate_columnar_key,
    get_column_order,
)


def test_columnar_key_order_and_duplicate_handling():
    """Verify consistent tie-breaking for duplicate characters using stable sort."""
    # BALLOON -> B(1), A(0), L(2), L(3), O(4), O(5), N(6)
    # Characters: A (pos 1), B (pos 0), L (pos 2), L (pos 3), N (pos 6), O (pos 4), O (pos 5)
    order = get_column_order("BALLOON")
    assert order == [1, 0, 2, 3, 6, 4, 5]


def test_columnar_irregular_transposition_round_trip():
    """Verify lossless round trip for irregular (unpadded) columnar transposition."""
    key = "GERMAN"
    plaintext = "DEFEND THE EAST WALL AT DAWN!"
    ciphertext, meta = encrypt_columnar(plaintext, key, pad=False)
    assert ciphertext != plaintext
    assert meta["pad_len"] == 0

    decrypted, _ = decrypt_columnar(ciphertext, key, pad_len=0)
    assert decrypted == plaintext


def test_columnar_padded_transposition_round_trip():
    """Verify padded columnar transposition and metadata recovery."""
    key = "CIPHER"
    plaintext = "Network Security Mini Project"
    ciphertext, meta = encrypt_columnar(plaintext, key, pad=True, pad_char="X")
    assert meta["pad_len"] > 0

    decrypted, _ = decrypt_columnar(ciphertext, key, pad_len=meta["pad_len"])
    assert decrypted == plaintext


def test_columnar_empty_text():
    """Verify behavior on empty text."""
    ciphertext, _ = encrypt_columnar("", "KEYWORD")
    assert ciphertext == ""
    decrypted, _ = decrypt_columnar("", "KEYWORD")
    assert decrypted == ""


def test_columnar_invalid_keys():
    """Verify rejection of keys that are too short or invalid."""
    valid, msg = validate_columnar_key("A")
    assert valid is False
    assert "at least 2" in msg

    with pytest.raises(ValueError):
        encrypt_columnar("Hello", "A")
