from binascii import hexlify
from antelopy.serializers import assets

def test_serialize_symbol_code():
    assert (
        hexlify(assets.serialize_symbol_code("WAX"))
        == b"57415800000000"
    ), "Asset string conversion failed"
    assert (
        hexlify(assets.serialize_symbol_code("MYTOKEN"))
        == b"4d59544f4b454e"
    ), "Asset string conversion failed"

def test_serialize_symbol():
    assert (
        hexlify(assets.serialize_symbol(8, "WAX")) == b"0857415800000000"
    ), "Symbol to bytes conversion failed"


def test_serialize_asset():
    assert (
        hexlify(assets.serialize_asset("1234.00000000 WAX"))
        == b"009236bb1c0000000857415800000000"
    ), "Asset string conversion failed"
    assert (
        hexlify(assets.serialize_asset("1234.000000 MYTOKEN"))
        == b"80588d4900000000064d59544f4b454e"
    ), "Asset string conversion failed"
