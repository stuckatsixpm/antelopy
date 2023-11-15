import binascii
import hashlib

from antelopy import AbiCache


def test_binascii_unhexlify(abi_cache: AbiCache):
    assert abi_cache.unhexlify(b"0857415800000000") == binascii.unhexlify(
        b"0857415800000000"
    ), "unhexlify wrapper failed"


def test_binascii_hexlify(abi_cache: AbiCache):
    assert abi_cache.hexlify(
        "The quick brown fox jumps over the lazy dog".encode("utf-8")
    ) == binascii.hexlify(
        "The quick brown fox jumps over the lazy dog".encode("utf-8")
    ), "hexlify wrapper failed"


def test_sha256digest(abi_cache: AbiCache):
    # simulate aioeos transaction flow

    assert (
        abi_cache.sha256digest(
            "The quick brown fox jumps over the lazy dog".encode("utf-8")
        )
        == hashlib.sha256(
            "The quick brown fox jumps over the lazy dog".encode("utf-8")
        ).digest()
    ), "unhexlify wrapper failed"
