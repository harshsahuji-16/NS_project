"""Classical Cryptography Toolkit - Cryptographic Algorithms Package.

This package provides implementations of eight classical ciphers:
Substitution Ciphers:
- Caesar Cipher
- Monoalphabetic Substitution Cipher
- Playfair Cipher
- Hill Cipher (2x2 Matrix)
- Vigenère Cipher
- One-Time Pad (Vernam Cipher)

Transposition Ciphers:
- Rail Fence Cipher
- Columnar Transposition Cipher
"""

from .caesar import encrypt_caesar, decrypt_caesar
from .monoalphabetic import (
    encrypt_monoalphabetic,
    decrypt_monoalphabetic,
    generate_monoalphabetic_key,
    validate_monoalphabetic_key,
)
from .playfair import (
    encrypt_playfair,
    decrypt_playfair,
    generate_playfair_matrix,
)
from .hill import (
    encrypt_hill,
    decrypt_hill,
    validate_hill_matrix,
    invert_matrix_mod26,
)
from .vigenere import (
    encrypt_vigenere,
    decrypt_vigenere,
    validate_vigenere_key,
)
from .one_time_pad import (
    encrypt_otp,
    decrypt_otp,
    generate_otp_key,
    validate_otp_key,
)
from .rail_fence import (
    encrypt_rail_fence,
    decrypt_rail_fence,
    validate_rail_fence_key,
)
from .columnar_transposition import (
    encrypt_columnar,
    decrypt_columnar,
    validate_columnar_key,
)

__all__ = [
    "encrypt_caesar",
    "decrypt_caesar",
    "encrypt_monoalphabetic",
    "decrypt_monoalphabetic",
    "generate_monoalphabetic_key",
    "validate_monoalphabetic_key",
    "encrypt_playfair",
    "decrypt_playfair",
    "generate_playfair_matrix",
    "encrypt_hill",
    "decrypt_hill",
    "validate_hill_matrix",
    "invert_matrix_mod26",
    "encrypt_vigenere",
    "decrypt_vigenere",
    "validate_vigenere_key",
    "encrypt_otp",
    "decrypt_otp",
    "generate_otp_key",
    "validate_otp_key",
    "encrypt_rail_fence",
    "decrypt_rail_fence",
    "validate_rail_fence_key",
    "encrypt_columnar",
    "decrypt_columnar",
    "validate_columnar_key",
]
