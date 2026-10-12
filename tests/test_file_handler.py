"""Unit tests for File Encryption and Decryption Handlers."""

import pytest
from modules.file_handler import (
    create_encrypted_file_content,
    parse_encrypted_file_content,
    encrypt_text_file,
    decrypt_text_file,
)


def test_file_packaging_and_parsing():
    """Verify structured file envelope format serialization and parsing."""
    cipher = "Caesar Cipher"
    raw_ciphertext = "KHOOR ZRUOG"
    metadata = {"pad_len": 0}

    packaged = create_encrypted_file_content(cipher, raw_ciphertext, metadata)
    parsed = parse_encrypted_file_content(packaged)

    assert parsed["cipher_name"] == cipher
    assert parsed["ciphertext"] == raw_ciphertext
    assert parsed["metadata"]["pad_len"] == 0
    assert "TIMESTAMP" in packaged


def test_file_encryption_decryption_caesar():
    """Verify text file encryption/decryption round trip for Caesar cipher."""
    original_text = "This is a secret document.\nLine 2 with numbers 12345.\nLine 3 with punctuation!"
    packaged_encrypted, _ = encrypt_text_file(original_text, "Caesar Cipher", 7)

    decrypted, cipher = decrypt_text_file(packaged_encrypted, 7, expected_cipher="Caesar Cipher")
    assert cipher == "Caesar Cipher"
    assert decrypted == original_text


def test_file_encryption_decryption_hill_with_padding():
    """Verify text file encryption/decryption for Hill cipher preserves padding metadata."""
    original_text = "Secret Data"  # 10 letters -> even; let's do 11 letters: "Secret Data!" -> 10 letters; "Sec" -> 3 letters
    odd_text = "Odd length string abc"
    matrix = [[3, 3], [2, 5]]

    packaged, meta = encrypt_text_file(odd_text, "Hill Cipher", matrix)
    assert "pad_len" in meta

    decrypted, cipher = decrypt_text_file(packaged, matrix, expected_cipher="Hill Cipher")
    assert cipher == "Hill Cipher"
    assert decrypted == odd_text


def test_file_handler_empty_content_rejection():
    """Verify rejection of empty text files."""
    with pytest.raises(ValueError):
        encrypt_text_file("", "Caesar Cipher", 3)

    with pytest.raises(ValueError):
        parse_encrypted_file_content("")


def test_file_handler_corrupted_file_rejection():
    """Verify rejection of malformed or invalid files."""
    invalid_content = "This is just an ordinary text file without any toolkit header."
    with pytest.raises(ValueError) as exc:
        parse_encrypted_file_content(invalid_content)
    assert "signature" in str(exc.value).lower() or "header" in str(exc.value).lower()


def test_file_handler_cipher_mismatch():
    """Verify detection when user attempts to decrypt with wrong cipher type."""
    packaged, _ = encrypt_text_file("Secret", "Caesar Cipher", 3)
    with pytest.raises(ValueError) as exc:
        decrypt_text_file(packaged, "KEYWORD", expected_cipher="Vigenère Cipher")
    assert "mismatch" in str(exc.value).lower()
