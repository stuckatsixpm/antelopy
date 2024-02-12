"""serializers.py

contains serialization strategies for converting various python representations
of data to Antelope serialized data"""

from __future__ import annotations

import binascii
import struct
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Protocol, Tuple, Union

from antelopy.exceptions import ActionDataNotSerializedError
from antelopy.serializers import assets, keys, names, time_points, varints
from antelopy.types.transaction import PreSerializedTransaction
from antelopy.types.types import DEFAULT_TYPES

if TYPE_CHECKING:
    from antelopy.types.transaction import Action, Authorization, TransactionExtension


def split_and_pack_128(n: int):
    """Utility function to split a 16 byte int into 2 8-byte ints

    Args:
        n (int): int to pack

    Returns:
        _type_: little_endian 128-bit data
    """
    if n < 0:
        n = (1 << 128) + n
    buf = b""
    buf += struct.pack("Q", n & (2**64 - 1))
    buf += struct.pack("Q", n >> 64)
    return buf


class Serializer(Protocol):
    """Protocol template for serializaton strategies"""

    def serialize(self, v: Any) -> bytes:
        """Protocol template for serializaton function"""
        raise NotImplementedError("This hasn't been implemented yet")

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class ActionSerializer(Serializer):
    """Serialization strategy class for Action types"""

    def serialize(self, v: Action) -> bytes:
        buf = b""
        a = AuthorizationSerializer()
        buf += NameSerializer().serialize(v.account)
        buf += NameSerializer().serialize(v.name)
        buf += ListSerializer().serialize(
            [a.serialize(auth) for auth in v.authorization]
        )
        if isinstance(v.data, bytes):
            buf += VaruintSerializer().serialize(len(v.data)) + v.data
        else:
            raise ActionDataNotSerializedError(
                "Action data needs to be serialized before the action can be serialized"
            )
        # account: str
        # name: str
        # authorization: List[Authorization]
        # data: Union[bytes,Dict[str, Any]]
        return buf

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class AssetSerializer(Serializer):
    """Serialization strategy class for Asset types"""

    def serialize(self, v: str) -> bytes:
        """Serialize the data to Antelope-compatible asset format

        Args:
            v (str): the Asset to be serialized

        Returns:
            bytes: the serialized data
        """
        return assets.serialize_asset(v)

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class AuthorizationSerializer(Serializer):
    """Serialization strategy class for Authorizat types"""

    def serialize(self, v: Authorization) -> bytes:
        """Serialize the data to Antelope-compatible Authorization format

        Args:
            v (Authorization): the Authorization to be serialized

        Returns:
            bytes: the serialized data
        """
        n = NameSerializer()
        return n.serialize(v.actor) + n.serialize(v.permission)

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class BooleanSerializer(Serializer):
    """Serialization strategy class for Boolean types"""

    def serialize(self, v: bool) -> bytes:
        """Serialize the data to Antelope-compatible Boolean format

        Args:
            v (bool): the Boolean to be serialized

        Returns:
            bytes: the serialized data
        """
        return b"\x01" if v else b"\x00"

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class BytesSerializer(Serializer):
    """Serialization strategy class for Bytes types"""

    def serialize(self, v: bytes) -> bytes:
        """Serialize the data to Antelope-compatible Bytes format

        Args:
            v (stbytesr): the Bytes to be serialized

        Returns:
            bytes: the serialized data
        """
        return VaruintSerializer().serialize(len(v)) + v

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class ChecksumSerializer(Serializer):
    """Serialization strategy class for Checksum types"""

    def serialize(self, v: Union[str, bytes]) -> bytes:
        """Serialize the data to Antelope-compatible Checksum format

        Args:
            v (Union[str, bytes]): the Checksum to be serialized

        Returns:
            bytes: the serialized data
        """
        if isinstance(v, str):
            return bytes.fromhex(v)
        try:
            v = binascii.unhexlify(v)
        except binascii.Error:
            ...
        if len(v) in [20, 32, 64]:
            return v
        raise ValueError("serializing checksums expects str or bytes format")

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class ListSerializer(Serializer):
    """Serialization strategy class for List types"""

    def serialize(self, v: List[bytes]) -> bytes:
        """Serialize a list of serialized data to Antelope-compatible List format

        Args:
            v (List[bytes]): the list of data

        Returns:
            bytes: the serialized data
        """
        return varints.serialize_varint(len(v)) + b"".join(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class NameSerializer(Serializer):
    """Serialization strategy class for Name types"""

    def serialize(self, v: str) -> bytes:
        """Serialize a plaintext name to Antelope-compatible Name format

        Args:
            v (str): the plaintext name

        Returns:
            bytes: the serialized data
        """
        return names.serialize_name(v)

    def deserialize(self, v: bytes) -> str:
        """deserialize a Name from bytes to str

        Args:
            v (bytes): the encoded name

        Returns:
            str: the plaintext name
        """
        return names.deserialize_name(v)


class NumberSerializer(Serializer):
    """Serialization strategy class for Number types"""

    def __init__(self, number_type: str):
        self.type = number_type

    def serialize(self, v: Union[int, float, str]) -> bytes:
        """Serialize a number to Antelope-compatible format

        Args:
            v (Union[int, float, str]): the number to be serialized

        Raises:
            ValueError: raised when serialization fails. See error
                message for specific details

        Returns:
            bytes: the serialized data
        """
        if isinstance(v, str):
            if "int" in self.type:
                v = int(v)
            elif "float" in self.type:
                v = float(v)
            else:
                raise ValueError(
                    f"Value {v} could not be converted to an integer or float"
                )
        if self.type.endswith("128"):
            if isinstance(v, float):
                # see antelopy/types/types comments for float128
                raise ValueError("Python doesn't handle float128")
            return split_and_pack_128(v)
        return struct.pack(DEFAULT_TYPES[self.type], v)

    def deserialize(self, v: bytes) -> str:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class PublicKeySerializer(Serializer):
    """Serialization strategy class for PublicKey types"""

    def serialize(self, v: str) -> bytes:
        """Serializes a public key to Antelope-compatible format

        Args:
            v (str): The public key as text. Expects EOS_ or PUB_ key format.

        Returns:
            bytes: the serialized data
        """
        return keys.serialize_public_key(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class SignatureSerializer(Serializer):
    """Serialization strategy class for Signature types"""

    def serialize(self, v: str) -> bytes:
        """Serializes a signature to Antelope-compatible format

        Args:
            v (str): The signature in SIG_ format

        Returns:
            bytes: the serialized data
        """
        return keys.serialize_signature(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class StringSerializer(Serializer):
    """Serialization strategy class for String types"""

    def serialize(self, v: str) -> bytes:
        """Serializes a string to Antelope-compatible format

        Args:
            v (str): the string

        Returns:
            bytes: the serialized data
        """
        return VaruintSerializer().serialize(len(v)) + v.encode("utf-8")

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class SymbolCodeSerializer(Serializer):
    """Serialization strategy class for SymbolCode types"""

    def serialize(self, v: str) -> bytes:
        """Serializes a symbol code to Antelope-compatible format

        Args:
            v (str): the symbol code (e.g. `WAX`, `EOS`)

        Returns:
            bytes: the serialized data
        """
        return assets.serialize_symbol_code(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class SymbolSerializer(Serializer):
    """Serialization strategy class for Symbol types"""

    def serialize(self, v: str) -> bytes:
        """Serializes a Symbol to Antelope-compatible format

        Args:
            v (str): The symbol (e.g. `8, WAX`, `6, GUILD`)

        Returns:
            bytes: the serialized data
        """
        precision, symbol_name = v.split(",")
        return assets.serialize_symbol(int(precision), symbol_name)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class TimePointSerializer(Serializer):
    """Serialization strategy class for TimePoint types"""

    def serialize(self, v: Union[int, float, datetime]) -> bytes:
        """Serializes a time point to Antelope-compatible format with
        millisecond precision

        Args:
            v (Union[int, float, datetime]): the timepoint object

        Returns:
            bytes: the serialized data
        """
        return time_points.serialize_time_point(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class TimePointSecSerializer(Serializer):
    """Serialization strategy class for TimePointSec types"""

    def serialize(self, v: Union[int, float, datetime]) -> bytes:
        """Serializes a time point to Antelope-compatible format with second precision

        Args:
            v (Union[int, float, datetime]): the timepoint object

        Returns:
            bytes: the serialized data
        """
        return time_points.serialize_time_point_sec(v)

    def deserialize(self, v: Any) -> Any:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class TransactionSerializer(Serializer):
    """Serialization strategy class for Transactio types"""

    def serialize(self, v: PreSerializedTransaction) -> bytes:
        """Serializes a transaction. Action data and extensions must already
        be serialized.

        Args:
            v (PreSerializedTransaction): The partially-serialized transaction

        Returns:
            bytes: the serialized transaction
        """
        buf = b""
        buf += TimePointSecSerializer().serialize(v.expiration)
        buf += NumberSerializer("uint16").serialize(v.ref_block_num)
        buf += NumberSerializer("uint32").serialize(v.ref_block_prefix)
        buf += VaruintSerializer().serialize(v.max_net_usage_words)
        buf += NumberSerializer("uint8").serialize(v.max_cpu_usage_ms)
        buf += VaruintSerializer().serialize(v.delay_sec)

        # must be serialized
        buf += ListSerializer().serialize(v.context_free_actions)
        buf += ListSerializer().serialize(v.actions)
        buf += ListSerializer().serialize(v.transaction_extensions)
        return buf

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class TransactionExtensionSerializer(Serializer):
    """Serialization strategy class for TransactionExtension types"""

    def serialize(self, v: TransactionExtension) -> bytes:
        """Serializes a transaction extension to Antelope-compatible format

        Args:
            v (TransactionExtension): the extension

        Returns:
            bytes: the serialized extension
        """
        return NumberSerializer("uint16").serialize(v.type) + v.data

    def deserialize(self, v: Any) -> bytes:
        """Protocol template for deserialization function"""
        raise NotImplementedError("This hasn't been implemented yet")


class VarintSerializer(Serializer):
    """Serialization strategy class for Varint types"""

    def serialize(self, v: int) -> bytes:
        """Serializes a varint to Antelope-compatible format

        Args:
            v (int): the value to serialize

        Returns:
            bytes: the serialized data
        """
        return varints.serialize_varint((v << 1) ^ (v >> 31))

    def deserialize(self, v: bytes) -> Tuple[int, bytes]:
        return varints.deserialize_varint(v)


class VaruintSerializer(Serializer):
    """Serialization strategy class for Varuint types"""

    def serialize(self, v: int) -> bytes:
        """Serializes a varuint to Antelope-compatible format

        Args:
            v (int): the value to serialize

        Returns:
            bytes: the serialized data
        """
        return varints.serialize_varint(v)

    def deserialize(self, v: bytes) -> Tuple[int, bytes]:
        return varints.deserialize_varint(v)
