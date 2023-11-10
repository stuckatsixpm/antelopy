"""Extra type hinting types"""
from typing import Literal

# The default types for Antelope, and the `struct` module format string where relevant
DEFAULT_TYPES = {
    "bool": "",
    "int8": "B",
    "uint8": "b",
    "int16": "H",
    "uint16": "h",
    "int32": "I",
    "uint32": "i",
    "int64": "Q",
    "uint64": "q",
    "int128": "",  # TODO Struct doesn't natively 128bit support, so split before encoding
    "uint128": "",  # TODO Struct doesn't natively 128bit support, so split before encoding
    "varint32": "",  # TODO # Zigzag, to varuint
    "varuint32": "",  # TODO # varuint, pad to 32 bit
    "float32": "f",
    "float64": "d",
    "float128": "",  # TODO Struct doesn't natively 128bit support, so split before encoding
    "time_point": "",
    "time_point_sec": "",
    "block_timestamp_type": "",  # TODO
    "name": "",
    "bytes": "",
    "string": "",
    "checksum160": "",
    "checksum256": "",
    "checksum512": "",
    "public_key": "",
    "signature": "",
    "symbol": "",
    "symbol_code": "",
    "asset": "",
    "extended_asset": "",  # TODO
}


ValidTypes = Literal[
    "bool",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "int128",
    "uint128",
    "varint32",
    "varuint32",
    "float32",
    "float64",
    "float128",
    "time_point",
    "time_point_sec",
    "block_timestamp_type",
    "name",
    "bytes",
    "string",
    "checksum160",
    "checksum256",
    "checksum512",
    "public_key",
    "signature",
    "symbol",
    "symbol_code",
    "asset",
    "extended_asset",
]
