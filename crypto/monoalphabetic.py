"""Monoalphabetic Substitution Cipher implementation.

In a Monoalphabetic Substitution Cipher, each letter of the standard alphabet
is replaced by a unique letter from a 26-letter substitution alphabet key.
Preserves spaces, punctuation, digits, and original letter casing.
"""

import random
import string


def validate_monoalphabetic_key(key: str) -> tuple[bool, str]:
    """Validate a 26-letter substitution alphabet key.

    Returns:
        (True, "") if valid, or (False, error_message) if invalid.
    """
    if not isinstance(key, str):
        return False, "Key must be a string."

    clean_key = key.strip().upper()
    if len(clean_key) != 26:
        return False, f"Key must contain exactly 26 letters (current length: {len(clean_key)})."

    if not clean_key.isalpha():
        return False, "Key must only contain alphabetic characters (A-Z)."

    unique_chars = set(clean_key)
    if len(unique_chars) != 26:
        duplicates = [c for c in string.ascii_uppercase if clean_key.count(c) > 1]
        missing = [c for c in string.ascii_uppercase if c not in unique_chars]
        return False, f"Key must contain 26 UNIQUE letters. Duplicates: {','.join(duplicates)}. Missing: {','.join(missing)}."

    return True, ""


def generate_monoalphabetic_key() -> str:
    """Generate a random valid 26-letter substitution key."""
    letters = list(string.ascii_uppercase)
    random.shuffle(letters)
    return "".join(letters)


def encrypt_monoalphabetic(plaintext: str, key: str) -> str:
    """Encrypt plaintext using a 26-letter substitution key.

    Preserves case and non-alphabetic characters.
    """
    is_valid, err_msg = validate_monoalphabetic_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Monoalphabetic key: {err_msg}")

    key_upper = key.strip().upper()
    enc_map_upper = {string.ascii_uppercase[i]: key_upper[i] for i in range(26)}
    enc_map_lower = {string.ascii_lowercase[i]: key_upper[i].lower() for i in range(26)}

    result = []
    for char in plaintext:
        if char in enc_map_upper:
            result.append(enc_map_upper[char])
        elif char in enc_map_lower:
            result.append(enc_map_lower[char])
        else:
            result.append(char)
    return "".join(result)


def decrypt_monoalphabetic(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using a 26-letter substitution key.

    Preserves case and non-alphabetic characters.
    """
    is_valid, err_msg = validate_monoalphabetic_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Monoalphabetic key: {err_msg}")

    key_upper = key.strip().upper()
    dec_map_upper = {key_upper[i]: string.ascii_uppercase[i] for i in range(26)}
    dec_map_lower = {key_upper[i].lower(): string.ascii_lowercase[i] for i in range(26)}

    result = []
    for char in ciphertext:
        if char in dec_map_upper:
            result.append(dec_map_upper[char])
        elif char in dec_map_lower:
            result.append(dec_map_lower[char])
        else:
            result.append(char)
    return "".join(result)


def get_monoalphabetic_mapping(key: str) -> dict[str, str]:
    """Return dictionary mapping A-Z to substitution letters."""
    key_upper = key.strip().upper()
    return {string.ascii_uppercase[i]: key_upper[i] for i in range(26)}
