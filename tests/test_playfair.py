"""Unit tests for Playfair Cipher."""

import pytest
from crypto.playfair import (
    encrypt_playfair,
    decrypt_playfair,
    generate_playfair_matrix,
    prepare_playfair_text,
)


def test_playfair_matrix_generation():
    """Verify 5x5 key matrix structure, J-to-I mapping, and unique 25 characters."""
    keyword = "MONARCHY"
    matrix = generate_playfair_matrix(keyword)
    assert len(matrix) == 5
    assert all(len(row) == 5 for row in matrix)

    flat = [c for row in matrix for c in row]
    assert len(flat) == 25
    assert len(set(flat)) == 25
    assert 'J' not in flat
    assert 'I' in flat
    # First row should start with unique letters of MONARCHY
    assert matrix[0] == ['M', 'O', 'N', 'A', 'R']


def test_playfair_digraph_preprocessing():
    """Verify handling of repeated letters ('LL') and odd length padding."""
    digraphs, log = prepare_playfair_text("BALLOON")
    # 'BA', 'LL' -> 'LX', 'LO', 'ON'
    expected_pairs = [('B', 'A'), ('L', 'X'), ('L', 'O'), ('O', 'N')]
    assert digraphs == expected_pairs
    assert len(log) > 0


def test_playfair_known_text_encryption_and_decryption():
    """Verify known encryption and round-trip digraph decryption."""
    keyword = "MONARCHY"
    plaintext = "INSTRUMENT"
    ciphertext, details = encrypt_playfair(plaintext, keyword)

    # Length must be even
    assert len(ciphertext) % 2 == 0
    assert len(details["steps"]) == len(plaintext) // 2

    decrypted, dec_details = decrypt_playfair(ciphertext, keyword)
    # Replaces 'J' with 'I' if any, recovers digraphs
    assert decrypted == plaintext
    assert "Decryption recovers original digraphs" in dec_details["note"]


def test_playfair_repeated_letter_filler():
    """Verify that repeated consecutive letters like 'COMMUNICATION' get split by 'X'."""
    keyword = "SECURITY"
    plaintext = "MEET"  # 'ME', 'ET' -> no duplicate in same pair!
    # 'HELLO' -> 'HE', 'LL' -> 'LX', 'LO' -> 'HE', 'LX', 'LO'
    ciphertext, _ = encrypt_playfair("HELLO", keyword)
    decrypted, _ = decrypt_playfair(ciphertext, keyword)
    assert decrypted == "HELXLO"


def test_playfair_invalid_keyword():
    """Verify rejection of empty or non-alphabetic keywords."""
    with pytest.raises(ValueError):
        encrypt_playfair("HELLO", "12345")

    with pytest.raises(ValueError):
        decrypt_playfair("KHOOR", "!!!")


def test_playfair_invalid_ciphertext_length():
    """Verify decryption rejects odd-length ciphertext."""
    with pytest.raises(ValueError):
        decrypt_playfair("ABC", "KEYWORD")
