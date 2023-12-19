import binascii
import struct
from datetime import datetime
from typing import Any, Protocol, Tuple, Union

from antelopy.serializers import assets, keys, names, time_points, varints
from antelopy.types.types import DEFAULT_TYPES


def split_and_pack_128(n: int):
    if n < 0:
        n = (1 << 128) + n
    buf = b""
    buf += struct.pack("Q", n & (2**64 - 1))
    buf += struct.pack("Q", n >> 64)
    return buf


class Serializer(Protocol):
    """Base Serializer Protocol"""

    def serialize(self, v: Any) -> bytes:
        ...

    def deserialize(self, v: Any) -> bytes:
        ...


class AssetSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return assets.serialize_asset(v)

    def deserialize(self, v: Any) -> bytes:
        ...


class BooleanSerializer(Serializer):
    def serialize(self, v: bool) -> bytes:
        return b"\x01" if v else b"\x00"

    def deserialize(self, v: Any) -> Any:
        ...


class BytesSerializer(Serializer):
    def serialize(self, v: bytes) -> bytes:
        return VaruintSerializer().serialize(len(v)) + v

    def deserialize(self, v: Any) -> Any:
        ...


class ChecksumSerializer(Serializer):
    def serialize(self, v: Union[str, bytes]) -> bytes:
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
        ...


class NameSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return names.serialize_name(v)

    def deserialize(self, v: bytes) -> str:
        return names.deserialize_name(v)


class NumberSerializer(Serializer):
    def __init__(self, number_type: str):
        self.type = number_type

    def serialize(self, v: Union[int, float, str]) -> bytes:
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
                # TODO: See if I can implement
                raise ValueError("Python doesn't handle float128")
            return split_and_pack_128(v)
        return struct.pack(DEFAULT_TYPES[self.type], v)

    def deserialize(self, v: bytes) -> str:
        ...


class PublicKeySerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return keys.serialize_public_key(v)

    def deserialize(self, v: Any) -> Any:
        ...


class SignatureSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return keys.serialize_signature(v)

    def deserialize(self, v: Any) -> Any:
        ...


class StringSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return VaruintSerializer().serialize(len(v)) + v.encode("utf-8")

    def deserialize(self, v: Any) -> Any:
        ...


class SymbolCodeSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return assets.serialize_symbol_code(v)

    def deserialize(self, v: Any) -> Any:
        ...


class SymbolSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        precision, symbol_name = v.split(",")
        return assets.serialize_symbol(int(precision), symbol_name)

    def deserialize(self, v: Any) -> Any:
        ...


class TimePointSerializer(Serializer):
    def serialize(self, v: Union[int, float, datetime]) -> bytes:
        return time_points.serialize_time_point(v)

    def deserialize(self, v: Any) -> Any:
        ...


class TimePointSecSerializer(Serializer):
    def serialize(self, v: Union[int, float, datetime]) -> bytes:
        return time_points.serialize_time_point_sec(v)

    def deserialize(self, v: Any) -> Any:
        ...


class VarintSerializer(Serializer):
    def serialize(self, v: int) -> bytes:
        return varints.serialize_varint((v << 1) ^ (v >> 31))

    def deserialize(self, v: bytes) -> Tuple[int, bytes]:
        return varints.deserialize_varint(v)


class VaruintSerializer(Serializer):
    def serialize(self, v: int) -> bytes:
        return varints.serialize_varint(v)

    def deserialize(self, v: bytes) -> Tuple[int, bytes]:
        return varints.deserialize_varint(v)
