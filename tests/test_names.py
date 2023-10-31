from binascii import hexlify, unhexlify
from antelopy.serializers import names


def test_string_to_name():
    assert (
        hexlify(names.str_to_name("stuckatsixpm")) == b'206b77381b8874c6'
    ), "Name conversion from string to bytes failed"
    assert (
        hexlify(names.str_to_name("c4vr2.wam")) == b'0000908603713741'
    ), "Name conversion from string to bytes failed"


def test_name_to_string():
    assert (
        names.name_to_str(unhexlify("206b77381b8874c6")) == "stuckatsixpm"
    ), "Name conversion from bytes to string failed"
    assert (
        names.name_to_str(unhexlify("0000908603713741")) == "c4vr2.wam"
    ), "Name conversion from bytes to string failed"
