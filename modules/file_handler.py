"""File encryption and decryption handler for Classical Cryptography Toolkit.

Handles UTF-8 text file encryption, structured metadata packaging,
and lossless round-trip file decryption.
"""

from datetime import datetime, timezone
import json
from typing import Any

from crypto import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_monoalphabetic,
    decrypt_monoalphabetic,
    encrypt_playfair,
    decrypt_playfair,
    encrypt_hill,
    decrypt_hill,
    encrypt_vigenere,
    decrypt_vigenere,
    encrypt_otp,
    decrypt_otp,
    encrypt_rail_fence,
    decrypt_rail_fence,
    encrypt_columnar,
    decrypt_columnar,
)

HEADER_START = "# =============================================================="
HEADER_IDENTIFIER = "# CLASSICAL CRYPTOGRAPHY TOOLKIT - ENCRYPTED FILE FORMAT v1.0"
HEADER_END = "# =============================================================="


def create_encrypted_file_content(
    cipher_name: str,
    ciphertext: str,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Format encrypted text into a structured downloadable text file with metadata.

    Encoding: UTF-8.
    """
    if metadata is None:
        metadata = {}

    meta_json = json.dumps(metadata, ensure_ascii=False)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        HEADER_START,
        HEADER_IDENTIFIER,
        f"# CIPHER: {cipher_name}",
        f"# TIMESTAMP: {timestamp}",
        f"# METADATA: {meta_json}",
        HEADER_END,
        ciphertext,
    ]
    return "\n".join(lines)


def parse_encrypted_file_content(content: str) -> dict[str, Any]:
    """Parse a toolkit-encrypted text file.

    Returns:
        {
            'cipher_name': str,
            'timestamp': str,
            'metadata': dict,
            'ciphertext': str
        }

    Raises:
        ValueError: If file is malformed, corrupted, or unsupported.
    """
    if not content or not content.strip():
        raise ValueError("File is empty.")

    lines = content.splitlines()
    if len(lines) < 6:
        raise ValueError("File does not contain valid toolkit headers (too few lines).")

    if HEADER_IDENTIFIER not in lines[1]:
        raise ValueError(
            "Unsupported file format! The file is missing the Classical Cryptography Toolkit signature."
        )

    cipher_name = None
    timestamp = None
    metadata = {}
    content_start_idx = -1

    for idx, line in enumerate(lines):
        if line.startswith("# CIPHER:"):
            cipher_name = line.replace("# CIPHER:", "").strip()
        elif line.startswith("# TIMESTAMP:"):
            timestamp = line.replace("# TIMESTAMP:", "").strip()
        elif line.startswith("# METADATA:"):
            try:
                metadata = json.loads(line.replace("# METADATA:", "").strip())
            except json.JSONDecodeError:
                raise ValueError("Corrupted metadata header in encrypted file.")
        elif idx >= 5 and line.startswith(HEADER_END):
            content_start_idx = idx + 1
            break

    if not cipher_name or content_start_idx == -1:
        raise ValueError("Malformed file header. Unable to identify cipher or content boundary.")

    ciphertext = "\n".join(lines[content_start_idx:])

    return {
        "cipher_name": cipher_name,
        "timestamp": timestamp,
        "metadata": metadata,
        "ciphertext": ciphertext,
    }


def encrypt_text_file(
    content: str,
    cipher_name: str,
    key: Any,
) -> tuple[str, dict[str, Any]]:
    """Encrypt raw file text content with selected cipher and key.

    Returns:
        (packaged_file_content, meta_info)
    """
    if not content:
        raise ValueError("Cannot encrypt an empty file.")

    metadata = {}
    ciphertext = ""

    if cipher_name == "Caesar Cipher":
        ciphertext = encrypt_caesar(content, int(key))

    elif cipher_name == "Monoalphabetic Substitution Cipher":
        ciphertext = encrypt_monoalphabetic(content, str(key))

    elif cipher_name == "Playfair Cipher":
        ciphertext, playfair_meta = encrypt_playfair(content, str(key))
        metadata["playfair"] = True

    elif cipher_name == "Hill Cipher":
        ciphertext, hill_meta = encrypt_hill(content, key, preserve_formatting=True)
        metadata["pad_len"] = hill_meta.get("pad_len", 0)

    elif cipher_name == "Vigenère Cipher":
        ciphertext = encrypt_vigenere(content, str(key))

    elif cipher_name == "One-Time Pad":
        ciphertext, key_used = encrypt_otp(content, str(key))
        # Do not expose OTP secret key in public file header for security,
        # but record the alphabetic length required
        metadata["otp_key_len"] = len(key_used)

    elif cipher_name == "Rail Fence Cipher":
        ciphertext = encrypt_rail_fence(content, int(key))

    elif cipher_name == "Columnar Transposition Cipher":
        ciphertext, col_meta = encrypt_columnar(content, str(key), pad=False)
        metadata["pad_len"] = col_meta.get("pad_len", 0)

    else:
        raise ValueError(f"Unsupported cipher: {cipher_name}")

    packaged_text = create_encrypted_file_content(cipher_name, ciphertext, metadata)
    return packaged_text, metadata


def decrypt_text_file(
    content: str,
    key: Any,
    expected_cipher: str | None = None,
) -> tuple[str, str]:
    """Parse and decrypt a toolkit-encrypted file.

    Args:
        content: The text content of the encrypted file.
        key: The decryption key.
        expected_cipher: Optional verification against user-selected cipher.

    Returns:
        (decrypted_plaintext, detected_cipher_name)
    """
    parsed = parse_encrypted_file_content(content)
    cipher_name = parsed["cipher_name"]
    ciphertext = parsed["ciphertext"]
    metadata = parsed["metadata"]

    if expected_cipher and expected_cipher != cipher_name:
        raise ValueError(
            f"Cipher mismatch! File was encrypted using '{cipher_name}', "
            f"but current selection is '{expected_cipher}'."
        )

    if cipher_name == "Caesar Cipher":
        plaintext = decrypt_caesar(ciphertext, int(key))

    elif cipher_name == "Monoalphabetic Substitution Cipher":
        plaintext = decrypt_monoalphabetic(ciphertext, str(key))

    elif cipher_name == "Playfair Cipher":
        plaintext, _ = decrypt_playfair(ciphertext, str(key))

    elif cipher_name == "Hill Cipher":
        pad_len = metadata.get("pad_len", 0)
        plaintext, _ = decrypt_hill(ciphertext, key, pad_len=pad_len, preserve_formatting=True)

    elif cipher_name == "Vigenère Cipher":
        plaintext = decrypt_vigenere(ciphertext, str(key))

    elif cipher_name == "One-Time Pad":
        plaintext = decrypt_otp(ciphertext, str(key))

    elif cipher_name == "Rail Fence Cipher":
        plaintext = decrypt_rail_fence(ciphertext, int(key))

    elif cipher_name == "Columnar Transposition Cipher":
        pad_len = metadata.get("pad_len", 0)
        plaintext, _ = decrypt_columnar(ciphertext, str(key), pad_len=pad_len)

    else:
        raise ValueError(f"Unknown cipher specified in file header: {cipher_name}")

    return plaintext, cipher_name
