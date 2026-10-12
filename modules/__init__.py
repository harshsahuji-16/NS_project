"""Modules package for Classical Cryptography Toolkit."""

from .validation import (
    validate_cipher_input,
    validate_key_for_cipher,
)
from .file_handler import (
    create_encrypted_file_content,
    parse_encrypted_file_content,
    encrypt_text_file,
    decrypt_text_file,
)
from .comparison import (
    benchmark_all_ciphers,
)

__all__ = [
    "validate_cipher_input",
    "validate_key_for_cipher",
    "create_encrypted_file_content",
    "parse_encrypted_file_content",
    "encrypt_text_file",
    "decrypt_text_file",
    "benchmark_all_ciphers",
]
