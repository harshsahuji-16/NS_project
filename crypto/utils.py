"""Mathematical and text utilities for classical ciphers."""

import math


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean Algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse(a: int, m: int = 26) -> int | None:
    """Compute modular multiplicative inverse of a modulo m.
    Returns x such that (a * x) % m == 1, or None if no inverse exists.
    """
    a = a % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return (x % m + m) % m


def gcd(a: int, b: int) -> int:
    """Greatest Common Divisor of two integers."""
    return math.gcd(a, b)


def is_coprime_with_26(n: int) -> bool:
    """Check whether an integer n is coprime with 26."""
    return math.gcd(n % 26, 26) == 1
