"""Hill Cipher implementation (2x2 Matrix Modulo 26).

The Hill Cipher is a polygraphic substitution cipher based on linear algebra.
Features:
- Validates that the 2x2 key matrix determinant is coprime with 26.
- Generates clear, specific rejection reasons for singular/non-invertible matrices.
- Computes modular matrix inverse modulo 26.
- Handles odd-length alphabetic text with padding ('X').
- Preserves padding metadata for lossless round-trip recovery.
- Supports both raw uppercase block mode and text formatting preservation.
"""

from .utils import mod_inverse, gcd


def validate_hill_matrix(matrix: list[list[int]]) -> tuple[bool, str, int]:
    """Validate a 2x2 key matrix for Hill Cipher modulo 26.

    Returns:
        (is_valid, message, determinant_mod26)
    """
    if not isinstance(matrix, (list, tuple)) or len(matrix) != 2:
        return False, "Matrix must be a 2x2 structure (2 rows).", 0

    if not all(isinstance(row, (list, tuple)) and len(row) == 2 for row in matrix):
        return False, "Each row of the matrix must have exactly 2 integer elements.", 0

    try:
        a = int(matrix[0][0])
        b = int(matrix[0][1])
        c = int(matrix[1][0])
        d = int(matrix[1][1])
    except (ValueError, TypeError):
        return False, "All matrix entries must be valid integers.", 0

    det = (a * d - b * c) % 26

    if det == 0:
        return False, f"Determinant is 0 mod 26. The matrix is singular and cannot be inverted.", det

    g = gcd(det, 26)
    if g != 1:
        if det % 2 == 0:
            return (
                False,
                f"Determinant ({det}) is even, sharing a common factor 2 with 26. "
                f"No modular inverse exists mod 26.",
                det,
            )
        elif det % 13 == 0:
            return (
                False,
                f"Determinant ({det}) is a multiple of 13, sharing a common factor 13 with 26. "
                f"No modular inverse exists mod 26.",
                det,
            )
        else:
            return (
                False,
                f"Determinant ({det}) shares factor {g} with 26. gcd({det}, 26) = {g} != 1.",
                det,
            )

    inv_det = mod_inverse(det, 26)
    if inv_det is None:
        return False, f"No modular inverse exists for determinant {det} mod 26.", det

    return True, f"Matrix is valid! Determinant = {det}, modular inverse of det = {inv_det}.", det


def invert_matrix_mod26(matrix: list[list[int]]) -> list[list[int]]:
    """Compute the inverse of a 2x2 matrix modulo 26."""
    is_valid, msg, det = validate_hill_matrix(matrix)
    if not is_valid:
        raise ValueError(f"Matrix is not invertible mod 26: {msg}")

    inv_det = mod_inverse(det, 26)
    a, b = matrix[0][0] % 26, matrix[0][1] % 26
    c, d = matrix[1][0] % 26, matrix[1][1] % 26

    # Classical 2x2 adjugate: [[d, -b], [-c, a]]
    inv_a = (d * inv_det) % 26
    inv_b = ((-b % 26) * inv_det) % 26
    inv_c = ((-c % 26) * inv_det) % 26
    inv_d = (a * inv_det) % 26

    return [[inv_a, inv_b], [inv_c, inv_d]]


def encrypt_hill(
    plaintext: str,
    matrix: list[list[int]],
    preserve_formatting: bool = True,
) -> tuple[str, dict]:
    """Encrypt plaintext using Hill cipher (2x2 matrix mod 26).

    Args:
        plaintext: The input text.
        matrix: 2x2 key matrix.
        preserve_formatting: If True, preserves spaces, non-letters, and original casing.
                             If False, returns pure uppercase alphabetic ciphertext.

    Returns:
        (ciphertext, metadata_dict)
    """
    is_valid, err_msg, det = validate_hill_matrix(matrix)
    if not is_valid:
        raise ValueError(f"Invalid Hill matrix: {err_msg}")

    a, b = matrix[0][0] % 26, matrix[0][1] % 26
    c, d = matrix[1][0] % 26, matrix[1][1] % 26

    # Extract alphabetic letters
    letters = []
    positions = []
    cases = []
    for idx, ch in enumerate(plaintext):
        if ch.isalpha():
            letters.append(ch.upper())
            positions.append(idx)
            cases.append(ch.isupper())

    pad_len = 0
    if len(letters) % 2 != 0:
        letters.append('X')
        pad_len = 1

    cipher_letters = []
    vector_steps = []

    for i in range(0, len(letters), 2):
        p1 = ord(letters[i]) - ord('A')
        p2 = ord(letters[i + 1]) - ord('A')

        c1 = (a * p1 + b * p2) % 26
        c2 = (c * p1 + d * p2) % 26

        ch1 = chr(c1 + ord('A'))
        ch2 = chr(c2 + ord('A'))

        cipher_letters.extend([ch1, ch2])
        vector_steps.append({
            "vector_in": [p1, p2],
            "chars_in": letters[i] + letters[i + 1],
            "vector_out": [c1, c2],
            "chars_out": ch1 + ch2,
        })

    if preserve_formatting:
        res = list(plaintext)
        # Replace original letter positions
        for i in range(len(positions)):
            enc_char = cipher_letters[i]
            if not cases[i]:
                enc_char = enc_char.lower()
            res[positions[i]] = enc_char

        # If padded, append the padded character
        if pad_len > 0:
            res.append(cipher_letters[-1])
        ciphertext = "".join(res)
    else:
        ciphertext = "".join(cipher_letters)

    metadata = {
        "matrix": matrix,
        "det": det,
        "pad_len": pad_len,
        "preserve_formatting": preserve_formatting,
        "raw_blocks": ["".join(cipher_letters[i:i + 2]) for i in range(0, len(cipher_letters), 2)],
        "steps": vector_steps,
        "original_alpha_len": len(letters) - pad_len,
    }

    return ciphertext, metadata


def decrypt_hill(
    ciphertext: str,
    matrix: list[list[int]],
    pad_len: int = 0,
    preserve_formatting: bool = True,
) -> tuple[str, dict]:
    """Decrypt ciphertext using Hill cipher (2x2 matrix mod 26).

    Args:
        ciphertext: The ciphertext string.
        matrix: 2x2 key matrix.
        pad_len: Number of padding characters added during encryption (0 or 1).
        preserve_formatting: If True, preserves non-alphabetic characters and casing.

    Returns:
        (decrypted_text, metadata_dict)
    """
    is_valid, err_msg, det = validate_hill_matrix(matrix)
    if not is_valid:
        raise ValueError(f"Invalid Hill matrix: {err_msg}")

    inv_matrix = invert_matrix_mod26(matrix)
    ia, ib = inv_matrix[0][0], inv_matrix[0][1]
    ic, id = inv_matrix[1][0], inv_matrix[1][1]

    letters = []
    positions = []
    cases = []
    for idx, ch in enumerate(ciphertext):
        if ch.isalpha():
            letters.append(ch.upper())
            positions.append(idx)
            cases.append(ch.isupper())

    if len(letters) % 2 != 0:
        raise ValueError("Hill ciphertext alphabetic length must be even.")

    plain_letters = []
    vector_steps = []

    for i in range(0, len(letters), 2):
        c1 = ord(letters[i]) - ord('A')
        c2 = ord(letters[i + 1]) - ord('A')

        p1 = (ia * c1 + ib * c2) % 26
        p2 = (ic * c1 + id * c2) % 26

        ch1 = chr(p1 + ord('A'))
        ch2 = chr(p2 + ord('A'))

        plain_letters.extend([ch1, ch2])
        vector_steps.append({
            "vector_in": [c1, c2],
            "chars_in": letters[i] + letters[i + 1],
            "vector_out": [p1, p2],
            "chars_out": ch1 + ch2,
        })

    if preserve_formatting:
        res = list(ciphertext)
        total_orig_chars = len(positions) - pad_len

        # Fill recovered characters
        for i in range(total_orig_chars):
            rec_char = plain_letters[i]
            if not cases[i]:
                rec_char = rec_char.lower()
            res[positions[i]] = rec_char

        # Remove the padded character if one was appended
        if pad_len > 0 and len(res) > 0:
            res.pop()
        plaintext = "".join(res)
    else:
        if pad_len > 0:
            plaintext = "".join(plain_letters[:-pad_len])
        else:
            plaintext = "".join(plain_letters)

    metadata = {
        "inv_matrix": inv_matrix,
        "det": det,
        "pad_len": pad_len,
        "steps": vector_steps,
    }

    return plaintext, metadata
