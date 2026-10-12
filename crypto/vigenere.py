"""Vigenère Cipher implementation.

The Vigenère Cipher is a method of encrypting alphabetic text using a series of
interwoven Caesar ciphers, based on the letters of a keyword.
Features:
- Preserves letter casing.
- Preserves spaces, punctuation, and digits.
- Non-alphabetic characters do NOT advance the keyword stream.
- Validates the keyword.
- Generates step-by-step trace for educational demonstration.
"""


def validate_vigenere_key(key: str) -> tuple[bool, str]:
    """Validate a Vigenère keyword.

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(key, str):
        return False, "Keyword must be a string."

    clean_key = [c for c in key if c.isalpha()]
    if not clean_key:
        return False, "Keyword must contain at least one alphabetic character (A-Z)."

    return True, ""


def encrypt_vigenere(plaintext: str, key: str) -> str:
    """Encrypt plaintext using Vigenère cipher.

    Preserves case and non-alphabetic characters.
    Non-alphabetic characters do not advance the key index.
    """
    is_valid, err_msg = validate_vigenere_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Vigenère key: {err_msg}")

    clean_key = [c.upper() for c in key if c.isalpha()]
    key_len = len(clean_key)
    key_idx = 0

    result = []
    for char in plaintext:
        if char.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            enc_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(enc_char)
            key_idx += 1
        else:
            result.append(char)

    return "".join(result)


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using Vigenère cipher.

    Preserves case and non-alphabetic characters.
    Non-alphabetic characters do not advance the key index.
    """
    is_valid, err_msg = validate_vigenere_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Vigenère key: {err_msg}")

    clean_key = [c.upper() for c in key if c.isalpha()]
    key_len = len(clean_key)
    key_idx = 0

    result = []
    for char in ciphertext:
        if char.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            dec_char = chr((ord(char) - base - shift + 26) % 26 + base)
            result.append(dec_char)
            key_idx += 1
        else:
            result.append(char)

    return "".join(result)


def get_vigenere_steps(text: str, key: str, mode: str = "encrypt") -> list[dict]:
    """Generate educational steps showing character mapping against repeating keyword."""
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        return []

    key_len = len(clean_key)
    key_idx = 0
    steps = []

    for char in text:
        if char.isalpha():
            k_char = clean_key[key_idx % key_len]
            shift = ord(k_char) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            orig_val = ord(char) - base
            if mode == "encrypt":
                res_val = (orig_val + shift) % 26
                formula = f"({orig_val} + {shift}) mod 26 = {res_val}"
            else:
                res_val = (orig_val - shift + 26) % 26
                formula = f"({orig_val} - {shift} + 26) mod 26 = {res_val}"
            res_char = chr(res_val + base)

            steps.append({
                "char": char,
                "key_char": k_char,
                "shift": shift,
                "formula": formula,
                "result": res_char,
            })
            key_idx += 1
            if len(steps) >= 12:
                break
    return steps
