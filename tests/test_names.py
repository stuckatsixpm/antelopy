from binascii import hexlify, unhexlify
from antelopy.serializers import names


def test_string_to_name():
    assert (
        hexlify(names.serialize_name("stuckatsixpm")) == b"206b77381b8874c6"
    ), "Name conversion from string to bytes failed"
    assert (
        hexlify(names.serialize_name("c4vr2.wam")) == b"0000908603713741"
    ), "Name conversion from string to bytes failed"
    assert (
        hexlify(names.serialize_name("abcdefg12345a")) == b"56c810812d95d031"
    ), "Name conversion from string to bytes failed"


def test_name_to_string():
    assert (
        names.deserialize_name(unhexlify("206b77381b8874c6")) == "stuckatsixpm"
    ), "Name conversion from bytes to string failed"
    assert (
        names.deserialize_name(unhexlify("0000908603713741")) == "c4vr2.wam"
    ), "Name conversion from bytes to string failed"
    assert (
        names.deserialize_name(unhexlify("56c810812d95d031")) == "abcdefg12345a"
    ), "Name conversion from bytes to string failed"
