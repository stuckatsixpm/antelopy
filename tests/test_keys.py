from binascii import hexlify
from antelopy.serializers import keys


def test_string_to_public_key():
    assert (
        hexlify(
            keys.string_to_public_key(
                "EOS5o5CnexdMvaV83fbmNBQVhUAi6zuJQHm3vY4p2L2fzH7VUGp7p"
            )
        )
        == b"00027765c671e9a9dc0053796a96a5d2e80a04e97f97ea28e53efddb455157a7da1c"
    ), "EOS Public Key to Key bytes failed"


def test_string_to_signature():
    assert (
        hexlify(
            keys.string_to_signature(
                "SIG_K1_K9Dr5zUy9qsvySPQ4fWFRXKuadDPcXo3hRkeyo4gMuE8D6uaRZbiWiCuZHEB51X1aoqP8q1jUGSVAW7Qxydu6GvDvKzfRt"
            )
        )
        == b"001f6ac18f71903cc23d6aad1f7798b50ca93516c4e170ec42e6a254c07d22b589d24d84142cfd1b1dfd36ba112d633111cdb897df26fb9f414ff8f4c2703fd6b0f8"
    ), "K1 Signature failed conversion"
