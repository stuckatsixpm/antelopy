import json
import pytest
from antelopy import AbiCache


def test_basic_action(abi_cache: AbiCache):
    mock = {
        "owner": "stuckatsixpm",
        "animal_id": 519,
        "reward_type": "TestReward",
        "reward_card": 111111,
        "quantity": -135,  # Testing Negative Fields
    }
    result = abi_cache.serialize_data(
        contract_name="farmersworld", contract_action="logclaimrs", data=mock
    )
    assert (
        result == b"206b77381b8874c607020000000000000a5465737452657761726407b2010079ff"
    ), f"serialization conversion failed: {result}"


def test_nested_data(abi_cache: AbiCache):
    mock = {
        "authorized_creator": "c4vr2.wam",
        "collection_name": "tag",
        "schema_name": "pet",
        "transferable": True,
        "burnable": True,
        "max_supply": 123,
        "immutable_data": [
            {"key": "name", "value": ["string", "Fire Pumpkin"]},
            {
                "key": "default_img",
                "value": [
                    "string",
                    "QmerYBf3AqYvRH99EQFTda9e11jzTANp25ckVESNroSkFs",
                ],
            },
            {"key": "species", "value": ["string", "Fire Pumpkin"]},
            {
                "key": "description",
                "value": [
                    "string",
                    "Grown from a magical seed and given life through a sacrifice of candy, you've managed to grow your very own Cursed Pumpkin - one imbued with the Fire element! Be wary though, for its curse affects not just your opponent, but you as well!Grown from a magical seed and given life through a sacrifice of candy, you've managed to grow your very own Cursed Pumpkin - one imbued with the Fire element! Be wary though, for its curse affects not just your opponent, but you as well!Grown from a magical seed and given life through a sacrifice of candy, you've managed to grow your very own Cursed Pumpkin - one imbued with the Fire element! Be wary though, for its curse affects not just your opponent, but you as well!",
                ],
            },
            {"key": "rarity", "value": ["string", "Uncommon"]},
            {"key": "element", "value": ["string", "Fire"]},
            {"key": "artist", "value": ["string", "Magic Bean"]},
        ],
    }

    result = abi_cache.serialize_data(
        contract_name="atomicassets", contract_action="createtempl", data=mock
    )
    assert (
        result
        == b"000090860371374100000000000098c9000000000000b2aa01017b00000007046e616d650a0c466972652050756d706b696e0b64656661756c745f696d670a2e516d6572594266334171597652483939455146546461396531316a7a54414e703235636b5645534e726f536b467307737065636965730a0c466972652050756d706b696e0b6465736372697074696f6e0ac70547726f776e2066726f6d2061206d61676963616c207365656420616e6420676976656e206c696665207468726f756768206120736163726966696365206f662063616e64792c20796f75277665206d616e6167656420746f2067726f7720796f75722076657279206f776e204375727365642050756d706b696e202d206f6e6520696d62756564207769746820746865204669726520656c656d656e742120426520776172792074686f7567682c20666f72206974732063757273652061666665637473206e6f74206a75737420796f7572206f70706f6e656e742c2062757420796f752061732077656c6c2147726f776e2066726f6d2061206d61676963616c207365656420616e6420676976656e206c696665207468726f756768206120736163726966696365206f662063616e64792c20796f75277665206d616e6167656420746f2067726f7720796f75722076657279206f776e204375727365642050756d706b696e202d206f6e6520696d62756564207769746820746865204669726520656c656d656e742120426520776172792074686f7567682c20666f72206974732063757273652061666665637473206e6f74206a75737420796f7572206f70706f6e656e742c2062757420796f752061732077656c6c2147726f776e2066726f6d2061206d61676963616c207365656420616e6420676976656e206c696665207468726f756768206120736163726966696365206f662063616e64792c20796f75277665206d616e6167656420746f2067726f7720796f75722076657279206f776e204375727365642050756d706b696e202d206f6e6520696d62756564207769746820746865204669726520656c656d656e742120426520776172792074686f7567682c20666f72206974732063757273652061666665637473206e6f74206a75737420796f7572206f70706f6e656e742c2062757420796f752061732077656c6c21067261726974790a08556e636f6d6d6f6e07656c656d656e740a0446697265066172746973740a0a4d61676963204265616e"
    ), f"serialization conversion failed: {result}"


def test_nested_numbers(abi_cache: AbiCache):
    # I couldn't find an on-chain contract that had float datatypes
    mock = {
        "authorized_creator": "c4vr2.wam",
        "collection_name": "tag",
        "schema_name": "pet",
        "transferable": True,
        "burnable": True,
        "max_supply": 123,
        "immutable_data": [
            {"key": "name", "value": ["uint8", 12]},
            {"key": "name", "value": ["int8", -12]},
            {"key": "name", "value": ["float32", 12.34]},
            {"key": "name2", "value": ["float32", -12.34]},
        ],
    }

    result = abi_cache.serialize_data(
        contract_name="atomicassets", contract_action="createtempl", data=mock
    )
    assert (
        result
        == b"000090860371374100000000000098c9000000000000b2aa01017b00000004046e616d65040c046e616d6500f4046e616d6508a4704541056e616d653208a47045c1"
    ), f"serialization conversion failed: {result}"


def test_complex_structure(abi_cache: AbiCache):
    with open(r"tests\data\storehouse.blend", "r") as json_file:
        mock = json.load(json_file)
        mock["display_data"] = json.dumps(
            {
                "name": f"Storehouse",
                "image": "QmdR6g5kpRK7yiQKZZuJkN4qEiSKBgcdx5CmQKTpgVmU6E",
                "description": """*Test of work*""",
            }
        )

    result = abi_cache.serialize_data(
        contract_name="craft.tag", contract_action="createblend", data=mock
    )
    assert (
        result
        == b"000033195c052fe500000000000098c90300bd780b0000000000000098c90100000000000100000000000098c900f25472328727450a323578204c756d6265720206616d6f756e740102323508636f6e74656e747301064c756d6265720100000000000100000000000098c900f25472328727450b323578204d61736f6e72790206616d6f756e740102323508636f6e74656e747301074d61736f6e7279010000000000000101010000000100d4780b000001000000404821650000000000000000727b226e616d65223a202253746f7265686f757365222c2022696d616765223a2022516d64523667356b70524b377969514b5a5a754a6b4e34714569534b426763647835436d514b547067566d553645222c20226465736372697074696f6e223a20222a54657374206f6620776f726b2a227d0000000000000000"
    ), f"serialization conversion failed: {result}"


def test_key_serialization(abi_cache: AbiCache):
    mock = {
        "creator": "2hcoo.c.wam",
        "asset_ids": ["1099525200476"],
        "key": "EOS5o5CnexdMvaV83fbmNBQVhUAi6zuJQHm3vY4p2L2fzH7VUGp7p",
        "memo": "",
    }

    result = abi_cache.serialize_data(
        contract_name="atomictoolsx", contract_action="announcelink", data=mock
    )
    assert (
        result
        == b"00a4e100014a511300027765c671e9a9dc0053796a96a5d2e80a04e97f97ea28e53efddb455157a7da1c015c1acf000001000000"
    ), f"serialization conversion failed: {result}"


def test_sig_serialization(abi_cache: AbiCache):
    mock = {
        "claimer": "ok5e4.wam",
        "claimer_signature": "SIG_K1_KffgT96G1YtVPanSXvScJxYFideekGzBbL7RvP2jzJaYbkK8YTW1Wwg8ngDH1qtnDy2H2cFxxveivgqYPkUjD8B8Muvgut",
        "link_id": 2736738,
    }

    result = abi_cache.serialize_data(
        contract_name="atomictoolsx", contract_action="claimlink", data=mock
    )
    assert (
        result
        == b"62c22900000000000000908603a20aa400205377f146bd493e579aede69a77ba0fe51f94aa2b559de838ee354291d800908c60248991332d48f492717226cd37f6c75bdf3d14b79178e381099166a1878c25"
    ), f"serialization conversion failed: {result}"
