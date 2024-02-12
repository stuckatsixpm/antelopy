"""base58.py

Implementation of base58 encoding because no version of base58 is compatible
with aioeos, eospy, and pyntelope :P
"""

from typing import Union

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(b: Union[bytes, str]) -> bytes:
    """Converts string or bytes to Base58 encoded bytes

    Args:
        b (Union[bytes, str]): input value

    Returns:
        bytes: b58 encoded bytes
    """
    if isinstance(b, str):
        b = b.encode("ascii")
    r = b""
    zeros = 0
    for i in b:
        if i == 0:
            zeros += 1
        else:
            break
    n = int.from_bytes(b, "big")
    while n:
        n, mod = divmod(n, 58)
        r = ALPHABET[mod].encode() + r
    return b"1" * zeros + r


def b58decode(b: Union[bytes, str]) -> bytes:
    """Converts b58 encoded bytes or str to ascii bytes

    Args:
        b (Union[bytes, str): b58 encoded input

    Returns:
        bytes: bytes
    """
    if isinstance(b, str):
        b = b.encode("ascii")
    ones = 0
    for i in b:
        if chr(i) == "1":
            ones += 1
        else:
            break
    r = 0
    p = 1
    for i in b:
        r += (58 ** (len(b) - p)) * ALPHABET.index(chr(i))
        p += 1
    return b"\x00" * ones + r.to_bytes((r.bit_length() + 7) // 8, "big")
