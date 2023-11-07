from binascii import hexlify
from antelopy.serializers import assets


def test_symbol_to_bytes():
    assert (
        hexlify(assets.symbol_to_bytes(8, "WAX")) == b"0857415800000000"
    ), "Symbol to bytes conversion failed"


def test_asset_string_to_bytes():
    assert (
        hexlify(assets.asset_to_bytes("1234.00000000 WAX"))
        == b"009236bb1c0000000857415800000000"
    ), "Asset string conversion failed"
    assert (
        hexlify(assets.asset_to_bytes("1234.000000 MYTOKEN"))
        == b"80588d4900000000064d59544f4b454e"
    ), "Asset string conversion failed"
