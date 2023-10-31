from binascii import hexlify, unhexlify
from antelopy.serializers import varints

def test_encode_varint():
    assert hexlify(varints.encode_int(12345823)) == b'dfc3f105', "Varint encoding failed."

def test_decode_varint():
    assert varints.decode_buf(unhexlify("dfc3f105")) == (12345823,b''), "Varint decoding failed."

def test_decode_varint_with_continuation():
    assert varints.decode_buf(unhexlify("96011246")) == (150,b'\x12\x46'), "Varint decoding failed."