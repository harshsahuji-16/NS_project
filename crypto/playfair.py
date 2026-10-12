"""Playfair Cipher implementation.

The Playfair Cipher encrypts digraphs (pairs of letters) using a 5x5 key matrix.
Features:
- Combines 'I' and 'J' into 'I'.
- Resolves repeated letters in pairs using filler 'X' (or 'Q').
- Handles odd-length inputs by appending filler 'X' (or 'Z').
- Standard Row, Column, and Rectangle encryption and decryption rules.
- Documents that Playfair operates on alphabetic letters, and decrypted text
  may retain filler characters ('X').
"""

import string


def generate_playfair_matrix(keyword: str) -> list[list[str]]:
    """Generate a 5x5 Playfair key matrix from a keyword.
    'J' is replaced by 'I'.
    """
    clean_keyword = ""
    seen = set()

    for char in keyword.upper():
        if char.isalpha():
            c = 'I' if char == 'J' else char
            if c not in seen:
                seen.add(c)
                clean_keyword += c

    alphabet = string.ascii_uppercase.replace('J', '')
    for char in alphabet:
        if char not in seen:
            seen.add(char)
            clean_keyword += char

    matrix = []
    for r in range(5):
        matrix.append(list(clean_keyword[r * 5:(r + 1) * 5]))
    return matrix


def prepare_playfair_text(text: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Clean text and split into digraphs with filler characters.

    Returns:
        (digraphs, explanation_log)
    """
    clean_chars = []
    for c in text.upper():
        if c.isalpha():
            clean_chars.append('I' if c == 'J' else c)

    digraphs = []
    log = []
    i = 0
    while i < len(clean_chars):
        c1 = clean_chars[i]
        if i + 1 < len(clean_chars):
            c2 = clean_chars[i + 1]
            if c1 == c2:
                filler = 'Q' if c1 == 'X' else 'X'
                digraphs.append((c1, filler))
                log.append(f"Pair '{c1}{c1}' separated with filler '{filler}' -> '{c1}{filler}'")
                i += 1
            else:
                digraphs.append((c1, c2))
                i += 2
        else:
            filler = 'Z' if c1 == 'X' else 'X'
            digraphs.append((c1, filler))
            log.append(f"Single trailing char '{c1}' padded with filler '{filler}' -> '{c1}{filler}'")
            i += 1

    return digraphs, log


def _get_char_position(matrix: list[list[str]], char: str) -> tuple[int, int]:
    """Find row and column of character in 5x5 matrix."""
    target = 'I' if char == 'J' else char
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == target:
                return r, c
    raise ValueError(f"Character '{char}' not found in Playfair matrix.")


def encrypt_playfair(plaintext: str, keyword: str) -> tuple[str, dict]:
    """Encrypt plaintext using Playfair cipher.

    Returns:
        (ciphertext, details_dict)
    """
    if not any(c.isalpha() for c in keyword):
        raise ValueError("Playfair keyword must contain at least one alphabetic character.")

    matrix = generate_playfair_matrix(keyword)
    digraphs, prep_log = prepare_playfair_text(plaintext)

    ciphertext_pairs = []
    pair_steps = []

    for c1, c2 in digraphs:
        r1, col1 = _get_char_position(matrix, c1)
        r2, col2 = _get_char_position(matrix, c2)

        if r1 == r2:
            # Same row: shift right
            nc1 = matrix[r1][(col1 + 1) % 5]
            nc2 = matrix[r2][(col2 + 1) % 5]
            rule = "Same Row: Shift Right"
        elif col1 == col2:
            # Same column: shift down
            nc1 = matrix[(r1 + 1) % 5][col1]
            nc2 = matrix[(r2 + 1) % 5][col2]
            rule = "Same Column: Shift Down"
        else:
            # Rectangle: swap columns
            nc1 = matrix[r1][col2]
            nc2 = matrix[r2][col1]
            rule = "Rectangle: Swap Columns"

        enc_pair = nc1 + nc2
        ciphertext_pairs.append(enc_pair)
        pair_steps.append({
            "in": f"{c1}{c2}",
            "rule": rule,
            "out": enc_pair,
        })

    ciphertext = "".join(ciphertext_pairs)
    details = {
        "matrix": matrix,
        "digraphs": digraphs,
        "prep_log": prep_log,
        "steps": pair_steps,
        "formatted_ciphertext": " ".join(ciphertext_pairs),
    }
    return ciphertext, details


def decrypt_playfair(ciphertext: str, keyword: str) -> tuple[str, dict]:
    """Decrypt ciphertext using Playfair cipher.

    Returns:
        (decrypted_text, details_dict)
    """
    if not any(c.isalpha() for c in keyword):
        raise ValueError("Playfair keyword must contain at least one alphabetic character.")

    clean_cipher = [c for c in ciphertext.upper() if c.isalpha()]
    if len(clean_cipher) % 2 != 0:
        raise ValueError("Playfair ciphertext length must be even.")

    matrix = generate_playfair_matrix(keyword)
    digraphs = [(clean_cipher[i], clean_cipher[i + 1]) for i in range(0, len(clean_cipher), 2)]

    decrypted_pairs = []
    pair_steps = []

    for c1, c2 in digraphs:
        r1, col1 = _get_char_position(matrix, c1)
        r2, col2 = _get_char_position(matrix, c2)

        if r1 == r2:
            # Same row: shift left
            nc1 = matrix[r1][(col1 - 1) % 5]
            nc2 = matrix[r2][(col2 - 1) % 5]
            rule = "Same Row: Shift Left"
        elif col1 == col2:
            # Same column: shift up
            nc1 = matrix[(r1 - 1) % 5][col1]
            nc2 = matrix[(r2 - 1) % 5][col2]
            rule = "Same Column: Shift Up"
        else:
            # Rectangle: swap columns
            nc1 = matrix[r1][col2]
            nc2 = matrix[r2][col1]
            rule = "Rectangle: Swap Columns"

        dec_pair = nc1 + nc2
        decrypted_pairs.append(dec_pair)
        pair_steps.append({
            "in": f"{c1}{c2}",
            "rule": rule,
            "out": dec_pair,
        })

    decrypted_text = "".join(decrypted_pairs)
    details = {
        "matrix": matrix,
        "digraphs": digraphs,
        "steps": pair_steps,
        "formatted_decrypted": " ".join(decrypted_pairs),
        "note": (
            "Decryption recovers original digraphs. Note that filler letters ('X') "
            "inserted during encryption remain in the decrypted output as classical Playfair "
            "cannot distinguish semantic 'X' from structural filler."
        ),
    }
    return decrypted_text, details
