"""names.py

Utility functions for serializing and deserializing Antelope names.

Based off eosjs
"""


def char_to_symbol(c:int) -> int:
    """utility encoder from character int to symbol int
    """
    if ord("a") <= c <= ord("z"):
        return c - ord("a") + 6
    if ord("1") <= c <= ord("5"):
        return c - ord("1") + 1
    return 0


def symbol_to_char(s:int) -> str:
    """Utility encoder from symbol int to str"""
    if 6 <= s <= 31:
        return chr(ord("a") + s - 6)
    elif 1 <= s <= 5:
        return chr(ord("1") + s - 1)
    return "."


def str_to_name(s: str) -> bytes:
    """Converts the string representation to an 8 byte Antelope name"""
    a = bytearray(8)
    bit = 63
    for i in range(len(s)):
        c = char_to_symbol(ord(s[i]))
        if bit < 5:
            c = c << 1
        for j in range(4, -1, -1):
            if bit >= 0:
                a[bit // 8] |= ((c >> j) & 1) << (bit % 8)
                bit -= 1
    return a


def name_to_str(v: bytes):
    """Converts an Antelope name (8 bytes) to string"""
    result = ""
    bit = 63
    while bit >= 0:
        c = 0
        for i in range(0, 5):
            if bit >= 0:
                c = (c << 1) | ((v[bit // 8] >> bit % 8) & 1)
                bit -= 1
        result += symbol_to_char(c)
    result = result.rstrip(".")
    return result
