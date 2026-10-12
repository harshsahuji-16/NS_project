"""Validation utilities for Classical Cryptography Toolkit."""

from typing import Any
import string

from crypto.caesar import encrypt_caesar
from crypto.monoalphabetic import validate_monoalphabetic_key
from crypto.playfair import generate_playfair_matrix
from crypto.hill import validate_hill_matrix
from crypto.vigenere import validate_vigenere_key
from crypto.one_time_pad import validate_otp_key
from crypto.rail_fence import validate_rail_fence_key
from crypto.columnar_transposition import validate_columnar_key


def validate_cipher_input(text: str, cipher_name: str, mode: str = "encrypt") -> tuple[bool, str]:
    """Validate plaintext or ciphertext input for a given cipher."""
    if text is None:
        return False, "Input text cannot be None."

    if len(text.strip()) == 0:
        return False, "Input text cannot be empty."

    alpha_count = sum(1 for c in text if c.isalpha())

    if cipher_name in ["Playfair Cipher", "Hill Cipher"]:
        if alpha_count == 0:
            return False, f"{cipher_name} requires at least one alphabetic letter (A-Z) in the input."

    if cipher_name == "Playfair Cipher" and mode == "decrypt":
        if alpha_count % 2 != 0:
            return False, "Playfair ciphertext must contain an even number of letters."

    return True, ""


def validate_key_for_cipher(cipher_name: str, key_val: Any, text: str = "") -> tuple[bool, str, Any]:
    """Validate and parse key based on cipher type.

    Returns:
        (is_valid, error_message, parsed_key)
    """
    if cipher_name == "Caesar Cipher":
        try:
            k = int(key_val)
            return True, "", k
        except (ValueError, TypeError):
            return False, "Caesar key must be an integer (e.g., 3, 5, -2, 29).", None

    elif cipher_name == "Monoalphabetic Substitution Cipher":
        if not isinstance(key_val, str):
            return False, "Key must be a string.", None
        is_val, msg = validate_monoalphabetic_key(key_val)
        if not is_val:
            return False, msg, None
        return True, "", key_val.strip().upper()

    elif cipher_name == "Playfair Cipher":
        if not isinstance(key_val, str):
            return False, "Keyword must be a string.", None
        clean = "".join([c for c in key_val if c.isalpha()])
        if not clean:
            return False, "Playfair keyword must contain at least one alphabetic letter.", None
        return True, "", key_val.strip().upper()

    elif cipher_name == "Hill Cipher":
        # Expecting either 2x2 list of ints or 4 comma-separated numbers "a,b,c,d"
        matrix = None
        if isinstance(key_val, (list, tuple)) and len(key_val) == 2:
            matrix = key_val
        elif isinstance(key_val, str):
            parts = [p.strip() for p in key_val.replace(";", ",").split(",") if p.strip()]
            if len(parts) == 4:
                try:
                    matrix = [
                        [int(parts[0]), int(parts[1])],
                        [int(parts[2]), int(parts[3])],
                    ]
                except ValueError:
                    return False, "Matrix values must be valid integers.", None
            else:
                return False, "Hill key string must provide 4 comma-separated integers (e.g., '3, 3, 2, 5').", None
        else:
            return False, "Invalid Hill key format.", None

        is_val, msg, det = validate_hill_matrix(matrix)
        if not is_val:
            return False, msg, None
        return True, "", matrix

    elif cipher_name == "Vigenère Cipher":
        if not isinstance(key_val, str):
            return False, "Keyword must be a string.", None
        is_val, msg = validate_vigenere_key(key_val)
        if not is_val:
            return False, msg, None
        return True, "", key_val.strip()

    elif cipher_name == "One-Time Pad":
        if not isinstance(key_val, str):
            return False, "OTP key must be a string.", None
        alpha_count = sum(1 for c in text if c.isalpha())
        is_val, msg = validate_otp_key(key_val, alpha_count)
        if not is_val:
            return False, msg, None
        return True, "", key_val.strip()

    elif cipher_name == "Rail Fence Cipher":
        try:
            r = int(key_val)
            is_val, msg = validate_rail_fence_key(r)
            if not is_val:
                return False, msg, None
            return True, "", r
        except (ValueError, TypeError):
            return False, "Rail Fence key must be an integer >= 1.", None

    elif cipher_name == "Columnar Transposition Cipher":
        if not isinstance(key_val, str):
            return False, "Key must be a string.", None
        is_val, msg = validate_columnar_key(key_val)
        if not is_val:
            return False, msg, None
        return True, "", key_val.strip()

    return False, f"Unknown cipher '{cipher_name}'.", None
