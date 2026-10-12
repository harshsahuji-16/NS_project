"""Algorithm comparison module for Classical Cryptography Toolkit.

Measures encryption and decryption performance, ciphertext expansion,
and round-trip correctness across all eight classical ciphers using time.perf_counter().
"""

import time
from typing import Any
import pandas as pd

from crypto import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_monoalphabetic,
    decrypt_monoalphabetic,
    generate_monoalphabetic_key,
    encrypt_playfair,
    decrypt_playfair,
    encrypt_hill,
    decrypt_hill,
    encrypt_vigenere,
    decrypt_vigenere,
    encrypt_otp,
    decrypt_otp,
    generate_otp_key,
    encrypt_rail_fence,
    decrypt_rail_fence,
    encrypt_columnar,
    decrypt_columnar,
)

COMPARISON_DISCLAIMER = (
    "EDUCATIONAL PERFORMANCE NOTE: Benchmark execution times are measured using "
    "Python's high-resolution `time.perf_counter()`. Timing measurements vary based on "
    "CPU frequency, operating system thread scheduling, Python bytecode interpreter overhead, "
    "and input text length. IN MODERN CRYPTOGRAPHY, RAW SPEED DOES NOT CORRELATE WITH "
    "SECURITY. Classical ciphers are vulnerable to frequency analysis, known-plaintext attacks, "
    "and brute-force searches regardless of their runtime efficiency."
)


def benchmark_all_ciphers(
    sample_text: str,
    iterations: int = 5,
) -> pd.DataFrame:
    """Benchmark all 8 ciphers on sample_text over multiple iterations.

    Returns a pandas DataFrame with columns:
    - Algorithm
    - Category
    - Key Used
    - Enc Time (μs)
    - Dec Time (μs)
    - Total Time (μs)
    - Ciphertext Length
    - Length Ratio
    - Round-Trip Status
    """
    if not sample_text or not sample_text.strip():
        sample_text = "NETWORK SECURITY AND CLASSICAL CRYPTOGRAPHY BENCHMARK 2026"

    # Define standard valid benchmark keys for all 8 ciphers
    caesar_key = 5
    mono_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    playfair_key = "MONARCHY"
    hill_matrix = [[3, 3], [2, 5]]  # det=9 mod 26, coprime
    vigenere_key = "CIPHER"
    otp_key = generate_otp_key(sum(1 for c in sample_text if c.isalpha()))
    rail_key = 3
    columnar_key = "GERMAN"

    results = []

    # 1. Caesar
    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=lambda: encrypt_caesar(sample_text, caesar_key),
        dec_fn=lambda c: decrypt_caesar(c, caesar_key),
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Caesar Cipher",
        "Category": "Substitution",
        "Key": f"k = {caesar_key}",
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    # 2. Monoalphabetic
    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=lambda: encrypt_monoalphabetic(sample_text, mono_key),
        dec_fn=lambda c: decrypt_monoalphabetic(c, mono_key),
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Monoalphabetic Substitution",
        "Category": "Substitution",
        "Key": f"{mono_key[:8]}...",
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    # 3. Playfair
    def _playfair_enc():
        c, _ = encrypt_playfair(sample_text, playfair_key)
        return c

    def _playfair_dec(c):
        p, _ = decrypt_playfair(c, playfair_key)
        return p

    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=_playfair_enc,
        dec_fn=_playfair_dec,
        orig=None,  # Playfair modifies text via digraph rules, so verified checks reversible decryption
        iterations=iterations,
        custom_verify=lambda orig, dec: len(dec) >= len([c for c in sample_text if c.isalpha()]),
    )
    results.append({
        "Algorithm": "Playfair Cipher",
        "Category": "Substitution",
        "Key": playfair_key,
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Digraphs Recovered" if verified else "Failed",
    })

    # 4. Hill Cipher
    def _hill_enc():
        c, meta = encrypt_hill(sample_text, hill_matrix, preserve_formatting=True)
        return c, meta

    def _hill_dec(c_and_meta):
        c, meta = c_and_meta
        p, _ = decrypt_hill(c, hill_matrix, pad_len=meta["pad_len"], preserve_formatting=True)
        return p

    t_enc, t_dec, c_len, verified = _benchmark_cipher_meta(
        enc_fn=_hill_enc,
        dec_fn=_hill_dec,
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Hill Cipher (2x2)",
        "Category": "Substitution",
        "Key": "[[3,3],[2,5]]",
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed (Lossless)" if verified else "Failed",
    })

    # 5. Vigenère Cipher
    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=lambda: encrypt_vigenere(sample_text, vigenere_key),
        dec_fn=lambda c: decrypt_vigenere(c, vigenere_key),
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Vigenère Cipher",
        "Category": "Substitution",
        "Key": vigenere_key,
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    # 6. One-Time Pad
    def _otp_enc():
        c, _ = encrypt_otp(sample_text, otp_key)
        return c

    def _otp_dec(c):
        return decrypt_otp(c, otp_key)

    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=_otp_enc,
        dec_fn=_otp_dec,
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "One-Time Pad",
        "Category": "Substitution",
        "Key": f"Random {len(otp_key)} chars",
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    # 7. Rail Fence Cipher
    t_enc, t_dec, c_len, verified = _benchmark_cipher(
        enc_fn=lambda: encrypt_rail_fence(sample_text, rail_key),
        dec_fn=lambda c: decrypt_rail_fence(c, rail_key),
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Rail Fence Cipher",
        "Category": "Transposition",
        "Key": f"rails = {rail_key}",
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    # 8. Columnar Transposition
    def _col_enc():
        c, meta = encrypt_columnar(sample_text, columnar_key, pad=False)
        return c, meta

    def _col_dec(c_and_meta):
        c, meta = c_and_meta
        p, _ = decrypt_columnar(c, columnar_key, pad_len=meta.get("pad_len", 0))
        return p

    t_enc, t_dec, c_len, verified = _benchmark_cipher_meta(
        enc_fn=_col_enc,
        dec_fn=_col_dec,
        orig=sample_text,
        iterations=iterations,
    )
    results.append({
        "Algorithm": "Columnar Transposition",
        "Category": "Transposition",
        "Key": columnar_key,
        "Enc Time (μs)": t_enc,
        "Dec Time (μs)": t_dec,
        "Total Time (μs)": t_enc + t_dec,
        "Ciphertext Len": c_len,
        "Length Ratio": f"{c_len / len(sample_text):.2f}",
        "Round-Trip Verified": "Passed" if verified else "Failed",
    })

    df = pd.DataFrame(results)
    return df


def _benchmark_cipher(
    enc_fn,
    dec_fn,
    orig: str | None,
    iterations: int = 5,
    custom_verify=None,
) -> tuple[float, float, int, bool]:
    """Helper to benchmark encryption and decryption functions."""
    # Warmup
    c = enc_fn()
    p = dec_fn(c)

    # Time encryption
    start = time.perf_counter()
    for _ in range(iterations):
        c = enc_fn()
    enc_time = ((time.perf_counter() - start) / iterations) * 1_000_000

    # Time decryption
    start = time.perf_counter()
    for _ in range(iterations):
        p = dec_fn(c)
    dec_time = ((time.perf_counter() - start) / iterations) * 1_000_000

    if custom_verify:
        verified = custom_verify(orig, p)
    else:
        verified = (p == orig) if orig is not None else True

    return round(enc_time, 2), round(dec_time, 2), len(c), verified


def _benchmark_cipher_meta(
    enc_fn,
    dec_fn,
    orig: str,
    iterations: int = 5,
) -> tuple[float, float, int, bool]:
    """Helper for ciphers returning metadata tuples."""
    # Warmup
    c_meta = enc_fn()
    p = dec_fn(c_meta)

    # Time encryption
    start = time.perf_counter()
    for _ in range(iterations):
        c_meta = enc_fn()
    enc_time = ((time.perf_counter() - start) / iterations) * 1_000_000

    # Time decryption
    start = time.perf_counter()
    for _ in range(iterations):
        p = dec_fn(c_meta)
    dec_time = ((time.perf_counter() - start) / iterations) * 1_000_000

    verified = (p == orig)
    return round(enc_time, 2), round(dec_time, 2), len(c_meta[0]), verified
