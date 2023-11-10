import hashlib
from binascii import hexlify
from antelopy import AbiCache


def test_serialize_checksums(abi_cache: AbiCache):
    raw_string = "The quick brown fox jumps over the lazy dog."
    # c256 tests hex formatted bytes
    # c512 tests bytes
    data = {
        "c160": hashlib.sha1(raw_string.encode()).hexdigest(),
        "c256": bytes.fromhex(hashlib.sha256(raw_string.encode()).hexdigest()),
        "c512": hashlib.sha512(raw_string.encode()).hexdigest().encode(),
    }
    s = abi_cache.serialize_data("mock", "chksummock", data)
    assert (
        s == data["c160"].encode() + hexlify(data["c256"]) + data["c512"]
    ), "checksum conversion failed"
