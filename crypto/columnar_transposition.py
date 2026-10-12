"""Columnar Transposition Cipher implementation.

The Columnar Transposition Cipher writes plaintext in rows of a fixed width
determined by the key length, then reads off the columns in alphabetical order
of the key characters.
Features:
- Accepts alphabetic keywords.
- Consistent tie-breaking for duplicate letters via stable left-to-right sorting.
- Implements both:
  1. Irregular Columnar Transposition (handles uneven final rows without padding).
  2. Padded Columnar Transposition (pads incomplete final rows and records metadata).
- Reversible round-trip decryption.
- Grid visualization helper for educational demonstration.
"""

import math


def validate_columnar_key(key: str) -> tuple[bool, str]:
    """Validate a Columnar Transposition keyword.

    Returns:
        (is_valid, error_message)
    """
    if not isinstance(key, str):
        return False, "Key must be a string."

    clean_key = "".join([c for c in key if c.isalnum()])
    if len(clean_key) < 2:
        return False, "Key must contain at least 2 alphanumeric characters."

    return True, ""


def get_column_order(key: str) -> list[int]:
    """Determine the column reading order from the key.
    Duplicate characters are ordered left-to-right (stable sort).

    Returns:
        List of column indices in the order they should be read.
    """
    clean_key = [c.upper() for c in key if c.isalnum()]
    # Stable sort by character value, preserving original index on ties
    order = sorted(range(len(clean_key)), key=lambda i: clean_key[i])
    return order


def encrypt_columnar(
    plaintext: str,
    key: str,
    pad: bool = False,
    pad_char: str = "X",
) -> tuple[str, dict]:
    """Encrypt plaintext using Columnar Transposition.

    Args:
        plaintext: The input text.
        key: Keyword determining column order.
        pad: If True, pad last row to full width. If False, use irregular transposition.
        pad_char: Character to pad with if pad is True.

    Returns:
        (ciphertext, metadata)
    """
    is_valid, err = validate_columnar_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Columnar key: {err}")

    if not plaintext:
        return "", {"grid": [], "order": [], "pad_len": 0}

    order = get_column_order(key)
    k = len(order)

    pad_len = 0
    text_to_use = plaintext
    if pad:
        rem = len(plaintext) % k
        if rem != 0:
            pad_len = k - rem
            text_to_use = plaintext + (pad_char * pad_len)

    total_len = len(text_to_use)
    num_rows = math.ceil(total_len / k)
    rem_cols = total_len % k  # Number of columns with length num_rows (if not multiple)

    # Build matrix/grid
    grid = []
    idx = 0
    for r in range(num_rows):
        row = []
        for c in range(k):
            if idx < total_len:
                row.append(text_to_use[idx])
                idx += 1
            else:
                row.append(None)
        grid.append(row)

    # Read columns in sorted order
    ciphertext_parts = []
    col_details = []

    for col_idx in order:
        col_chars = []
        for r in range(num_rows):
            char = grid[r][col_idx]
            if char is not None:
                col_chars.append(char)
        col_str = "".join(col_chars)
        ciphertext_parts.append(col_str)
        col_details.append({
            "col_index": col_idx,
            "key_char": [c.upper() for c in key if c.isalnum()][col_idx],
            "chars": col_str,
        })

    ciphertext = "".join(ciphertext_parts)
    metadata = {
        "key": key,
        "order": order,
        "grid": grid,
        "num_rows": num_rows,
        "pad_len": pad_len,
        "col_details": col_details,
        "is_padded": pad,
    }
    return ciphertext, metadata


def decrypt_columnar(
    ciphertext: str,
    key: str,
    pad_len: int = 0,
) -> tuple[str, dict]:
    """Decrypt ciphertext using Columnar Transposition.

    Correctly handles both irregular (unpadded) and padded columnar ciphers.

    Args:
        ciphertext: The encrypted string.
        key: Keyword used for column order.
        pad_len: Number of padding characters added during encryption.

    Returns:
        (decrypted_text, metadata)
    """
    is_valid, err = validate_columnar_key(key)
    if not is_valid:
        raise ValueError(f"Invalid Columnar key: {err}")

    if not ciphertext:
        return "", {"pad_len": 0}

    order = get_column_order(key)
    k = len(order)
    total_len = len(ciphertext)
    num_rows = math.ceil(total_len / k)
    rem_cols = total_len % k  # Columns 0 to rem_cols-1 have length num_rows

    # Determine length of each column in physical order
    col_lengths = [0] * k
    for c in range(k):
        if rem_cols == 0 or c < rem_cols:
            col_lengths[c] = num_rows
        else:
            col_lengths[c] = num_rows - 1

    # Fill characters into columns according to sorted key order
    columns = [[] for _ in range(k)]
    c_idx = 0
    for col_idx in order:
        length = col_lengths[col_idx]
        columns[col_idx] = list(ciphertext[c_idx:c_idx + length])
        c_idx += length

    # Reconstruct grid and read row by row
    grid = []
    plaintext_chars = []
    for r in range(num_rows):
        row = []
        for c in range(k):
            if r < len(columns[c]):
                ch = columns[c][r]
                row.append(ch)
                plaintext_chars.append(ch)
            else:
                row.append(None)
        grid.append(row)

    plaintext = "".join(plaintext_chars)
    if pad_len > 0:
        plaintext = plaintext[:-pad_len]

    metadata = {
        "grid": grid,
        "order": order,
        "pad_len": pad_len,
        "col_lengths": col_lengths,
    }
    return plaintext, metadata
