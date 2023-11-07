"""assets.py

Utility functions for assets and symbols"""

import struct
from decimal import Decimal


# Symbol consists of precision,symbol_name uint8, string
# String gets padded to uint64
def symbol_to_bytes(precision: int, symbol_name: str) -> bytes:
    """Converts a precision and symbol (token name) to bytes for serialization

    Args:
        precision (int): precision of the token
        symbol_name (str): token name (max 7 characters)

    Returns:
        bytes: serialized data
    """
    precision_byte = struct.pack("B", precision)
    symbol_bytes = symbol_name.encode()
    while len(symbol_bytes) < 7:
        symbol_bytes += b"\x00"
    return precision_byte + symbol_bytes


# Formated as 1.000000 WAX
def asset_to_bytes(asset_string: str) -> bytes:
    """Converts an asset string to bytes for serialization

    Args:
        asset_string (str): string to encode, e.g. "1.23450000 WAX"

    Returns:
        bytes: serialized data
    """
    quantity, symbol_name = asset_string.split(" ")
    if "." not in quantity:
        precision = 0
    else:
        precision = len(quantity.split(".")[1])
    amount = int(Decimal(quantity) * 10**precision)
    amount_bytes = struct.pack("Q", amount)
    symbol_bytes = symbol_to_bytes(precision, symbol_name)
    return amount_bytes + symbol_bytes
