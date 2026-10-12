"""Rail Fence (Zigzag) Cipher implementation.

The Rail Fence Cipher is a transposition cipher that writes characters in a
zigzag diagonal pattern across a specified number of parallel rails, then
reads off each rail horizontally.
Features:
- Handles empty strings and boundary rail counts (rails = 1, rails >= text length).
- Preserves spaces, punctuation, digits, and casing.
- Exact reversible matrix-based reconstruction for decryption.
- Visual zigzag grid helper for educational display.
"""


def validate_rail_fence_key(rails: int, text_len: int = 0) -> tuple[bool, str]:
    """Validate number of rails for Rail Fence cipher."""
    if not isinstance(rails, int):
        return False, "Number of rails must be an integer."
    if rails < 1:
        return False, "Number of rails must be at least 1."
    return True, ""


def encrypt_rail_fence(plaintext: str, rails: int) -> str:
    """Encrypt plaintext using Rail Fence transposition cipher.

    Preserves all characters, spaces, casing, and punctuation.
    """
    is_valid, err = validate_rail_fence_key(rails, len(plaintext))
    if not is_valid:
        raise ValueError(f"Invalid Rail Fence key: {err}")

    if rails == 1 or len(plaintext) <= rails or len(plaintext) == 0:
        return plaintext

    rail_lists = [[] for _ in range(rails)]
    current_rail = 0
    direction = 1  # 1 for down, -1 for up

    for char in plaintext:
        rail_lists[current_rail].append(char)
        current_rail += direction

        if current_rail == rails - 1:
            direction = -1
        elif current_rail == 0:
            direction = 1

    return "".join("".join(r) for r in rail_lists)


def decrypt_rail_fence(ciphertext: str, rails: int) -> str:
    """Decrypt ciphertext using Rail Fence transposition cipher.

    Reconstructs the zigzag pattern and reads plaintext sequentially.
    """
    is_valid, err = validate_rail_fence_key(rails, len(ciphertext))
    if not is_valid:
        raise ValueError(f"Invalid Rail Fence key: {err}")

    if rails == 1 or len(ciphertext) <= rails or len(ciphertext) == 0:
        return ciphertext

    n = len(ciphertext)
    # Create marker grid
    grid = [[None for _ in range(n)] for _ in range(rails)]

    # Mark zigzag path
    current_rail = 0
    direction = 1
    for c in range(n):
        grid[current_rail][c] = '*'
        current_rail += direction
        if current_rail == rails - 1:
            direction = -1
        elif current_rail == 0:
            direction = 1

    # Fill cipher characters into marked positions row-by-row
    c_idx = 0
    for r in range(rails):
        for c in range(n):
            if grid[r][c] == '*':
                grid[r][c] = ciphertext[c_idx]
                c_idx += 1

    # Read characters following the zigzag path
    plaintext = []
    current_rail = 0
    direction = 1
    for c in range(n):
        plaintext.append(grid[current_rail][c])
        current_rail += direction
        if current_rail == rails - 1:
            direction = -1
        elif current_rail == 0:
            direction = 1

    return "".join(plaintext)


def get_rail_fence_grid(text: str, rails: int, max_cols: int = 40) -> list[str]:
    """Generate visual ascii representation of zigzag pattern for educational display."""
    if rails < 1 or not text:
        return []

    display_text = text[:max_cols]
    n = len(display_text)
    grid = [[' ' for _ in range(n)] for _ in range(rails)]

    if rails == 1:
        return [display_text]

    current_rail = 0
    direction = 1
    for c in range(n):
        grid[current_rail][c] = display_text[c]
        current_rail += direction
        if current_rail == rails - 1:
            direction = -1
        elif current_rail == 0:
            direction = 1

    lines = []
    for r in range(rails):
        lines.append("".join(grid[r]))
    return lines
