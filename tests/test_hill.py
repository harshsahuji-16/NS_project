"""Unit tests for Hill Cipher (2x2 Matrix Modulo 26)."""

import pytest
from crypto.hill import (
    validate_hill_matrix,
    invert_matrix_mod26,
    encrypt_hill,
    decrypt_hill,
)


def test_hill_matrix_validation_valid():
    """Verify acceptance of valid coprime matrix."""
    matrix = [[3, 3], [2, 5]]  # det = (15 - 6) = 9; gcd(9, 26) = 1
    is_valid, msg, det = validate_hill_matrix(matrix)
    assert is_valid is True
    assert det == 9
    assert "valid" in msg.lower()


def test_hill_matrix_inversion():
    """Verify calculation of modular inverse matrix modulo 26."""
    matrix = [[3, 3], [2, 5]]
    inv = invert_matrix_mod26(matrix)
    # Expected inverse: [[15, 17], [20, 9]]
    assert inv == [[15, 17], [20, 9]]

    # Matrix product mod 26 must equal identity matrix [[1, 0], [0, 1]]
    a, b = matrix[0]
    c, d = matrix[1]
    ia, ib = inv[0]
    ic, id = inv[1]

    p00 = (a * ia + b * ic) % 26
    p01 = (a * ib + b * id) % 26
    p10 = (c * ia + d * ic) % 26
    p11 = (c * ib + d * id) % 26

    assert [[p00, p01], [p10, p11]] == [[1, 0], [0, 1]]


def test_hill_known_text_encryption():
    """Verify standard textbook example: 'HELP' -> 'HIAT' with key [[3, 3], [2, 5]]."""
    matrix = [[3, 3], [2, 5]]
    plaintext = "HELP"
    ciphertext, meta = encrypt_hill(plaintext, matrix, preserve_formatting=False)
    assert ciphertext == "HIAT"
    assert meta["pad_len"] == 0

    decrypted, dec_meta = decrypt_hill(ciphertext, matrix, pad_len=0, preserve_formatting=False)
    assert decrypted == "HELP"


def test_hill_padding_and_lossless_recovery():
    """Verify odd-length plaintext padding and exact round-trip recovery using pad_len."""
    matrix = [[3, 3], [2, 5]]
    plaintext = "DEF"  # 3 letters -> odd length -> padded to 4
    ciphertext, meta = encrypt_hill(plaintext, matrix, preserve_formatting=True)
    assert meta["pad_len"] == 1

    decrypted, _ = decrypt_hill(ciphertext, matrix, pad_len=meta["pad_len"], preserve_formatting=True)
    assert decrypted == plaintext


def test_hill_case_and_punctuation_preservation():
    """Verify preservation of casing, spaces, and punctuation."""
    matrix = [[3, 3], [2, 5]]
    plaintext = "Network Security, 2026!"
    ciphertext, meta = encrypt_hill(plaintext, matrix, preserve_formatting=True)
    assert ciphertext != plaintext

    decrypted, _ = decrypt_hill(ciphertext, matrix, pad_len=meta["pad_len"], preserve_formatting=True)
    assert decrypted == plaintext


def test_hill_invalid_matrix_singular():
    """Verify rejection of singular matrix (det = 0 mod 26)."""
    singular_matrix = [[2, 4], [1, 2]]  # det = 4 - 4 = 0
    is_valid, msg, det = validate_hill_matrix(singular_matrix)
    assert is_valid is False
    assert "singular" in msg.lower() or "0" in msg


def test_hill_invalid_matrix_even_determinant():
    """Verify rejection of matrix with even determinant (shares factor 2 with 26)."""
    matrix = [[2, 1], [4, 3]]  # det = 6 - 4 = 2 mod 26
    is_valid, msg, det = validate_hill_matrix(matrix)
    assert is_valid is False
    assert "factor 2" in msg.lower() or "even" in msg.lower()


def test_hill_invalid_matrix_factor_13():
    """Verify rejection of matrix with determinant divisible by 13."""
    matrix = [[1, 0], [0, 13]]  # det = 13 mod 26
    is_valid, msg, det = validate_hill_matrix(matrix)
    assert is_valid is False
    assert "13" in msg


def test_hill_invalid_dimensions():
    """Verify rejection of non-2x2 matrices."""
    is_valid, msg, _ = validate_hill_matrix([[1, 2, 3]])  # type: ignore
    assert is_valid is False
