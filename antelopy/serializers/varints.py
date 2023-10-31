""" varints.py

Varint Implementation based off https://github.com/fmoo/python-varint
"""


def encode_int(n: int) -> bytes:
    """Encodes a positive integer as a varint

    Args:
        n (int): the integer to encode

    Returns:
        bytes: encoded int
    """
    buf = b""
    while True:
        chunk = n & 0x7F
        n >>= 7
        if n:
            buf += (chunk | 0x80).to_bytes(1, "little")
        else:
            buf += chunk.to_bytes(1, "little")
            break
    return buf


# Stream conversion isn't needed for this project, and iterating
# over the buffer to decode the varint is faster
def decode_buf(n: bytes) -> tuple[int, bytes]:
    """Decodes a varint from bytes"""
    result = 0
    pos = 0
    reader = iter(n)
    for byte in reader:
        result += (byte & 0x7F) << pos
        if not byte & 0x80:
            break
        pos += 7
    return result, bytes(reader)
