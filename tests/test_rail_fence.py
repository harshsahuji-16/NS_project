"""Unit tests for Rail Fence Cipher."""

import pytest
from crypto.rail_fence import (
    encrypt_rail_fence,
    decrypt_rail_fence,
    validate_rail_fence_key,
    get_rail_fence_grid,
)


def test_rail_fence_known_reference():
    """Verify standard textbook example with 3 rails."""
    plaintext = "DEFEND THE EAST WALL"
    rails = 3
    ciphertext = encrypt_rail_fence(plaintext, rails)
    assert ciphertext != plaintext

    decrypted = decrypt_rail_fence(ciphertext, rails)
    assert decrypted == plaintext


def test_rail_fence_boundary_rails():
    """Verify behavior for rails = 1 and rails >= text length."""
    text = "SECURITY"
    assert encrypt_rail_fence(text, 1) == text
    assert decrypt_rail_fence(text, 1) == text

    assert encrypt_rail_fence(text, 20) == text
    assert decrypt_rail_fence(text, 20) == text


def test_rail_fence_empty_string():
    """Verify empty string handling."""
    assert encrypt_rail_fence("", 4) == ""
    assert decrypt_rail_fence("", 4) == ""


def test_rail_fence_invalid_rails():
    """Verify rejection of invalid rails (0, negative, non-integer)."""
    valid, msg = validate_rail_fence_key(0)
    assert valid is False

    with pytest.raises(ValueError):
        encrypt_rail_fence("Test", 0)

    with pytest.raises(ValueError):
        decrypt_rail_fence("Test", -2)


def test_rail_fence_grid_helper():
    """Verify ascii zigzag generator."""
    lines = get_rail_fence_grid("HELLOWORLD", 3)
    assert len(lines) == 3
    assert len(lines[0]) == 10
