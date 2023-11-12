"""keys.py

Utility functions to serialize EOS keys and signatures into bytes"""

import struct
from ..utils.base58 import b58decode, b58encode

KEY_TYPES = {
    "k1": 0,
    "r1": 1,
    "wa": 2,
}
# TODO: add reverse implementations, and potentially key length validation
# based on eosjs-numeric.ts (EOSIO/eosjs)


def serialize_public_key(s: str):
    """Converts string key (EOS...) to bytes with leading key-type byte"""
    buf = b""
    if s[:3] == "EOS":
        key_type = KEY_TYPES["k1"]
        buf += struct.pack("b", key_type)
        buf += b58decode(s[3:])[:-4]
    elif s[:3] == "PUB":
        key_type = KEY_TYPES[s[4:6].lower()]
        sig = s[7:]
        buf = b""
        buf += struct.pack("b", key_type)
        buf += b58decode(sig)[:-4]
    return buf


def serialize_signature(s: str):
    """Converts string signature (SIG_XX_...) to bytes with leading key-type byte"""
    key_type = KEY_TYPES[s[4:6].lower()]
    sig = s[7:]
    buf = b""
    buf += struct.pack("b", key_type)
    buf += b58decode(sig)[:-4]
    return buf
