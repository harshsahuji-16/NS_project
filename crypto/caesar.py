"""Caesar Cipher implementation.

The Caesar Cipher is one of the earliest and simplest substitution ciphers.
Each letter in the plaintext is shifted by a fixed number of positions (the key)
down the alphabet.
Preserves case, spaces, and punctuation.
Handles negative and oversized integer keys via modulo 26.
"""


def encrypt_caesar(plaintext: str, key: int) -> str:
    """Encrypt plaintext using Caesar Cipher with integer key.

    Formula: C = (P + k) mod 26
    Preserves case and non-alphabetic characters.
    """
    if not isinstance(key, int):
        raise TypeError("Caesar cipher key must be an integer.")

    shift = key % 26
    result = []
    for char in plaintext:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return "".join(result)


def decrypt_caesar(ciphertext: str, key: int) -> str:
    """Decrypt ciphertext using Caesar Cipher with integer key.

    Formula: P = (C - k) mod 26
    Preserves case and non-alphabetic characters.
    """
    if not isinstance(key, int):
        raise TypeError("Caesar cipher key must be an integer.")

    return encrypt_caesar(ciphertext, -key)


def get_caesar_steps(text: str, key: int, mode: str = "encrypt") -> list[dict]:
    """Generate educational transformation steps for display in UI.
    Shows the character, original position, shift, and resulting character.
    Limits to first 12 alphabetic characters for clean presentation.
    """
    shift = (key if mode == "encrypt" else -key) % 26
    steps = []
    count = 0
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            orig_pos = ord(char) - base
            new_pos = (orig_pos + shift) % 26
            new_char = chr(new_pos + base)
            steps.append({
                "char": char,
                "orig_pos": orig_pos,
                "shift": shift,
                "formula": f"({orig_pos} {'+' if mode == 'encrypt' else '-'} {abs(key)} mod 26) = {new_pos}",
                "result": new_char,
            })
            count += 1
            if count >= 12:
                break
    return steps
