import struct
from typing import Any, Protocol, Tuple, Union

from antelopy.serializers import names, varints
from antelopy.types.types import DEFAULT_TYPES

def split_and_pack_128(n:int):
    if n < 0:
        n = (1 << 128) + n
    buf = b""
    buf += struct.pack("Q",n&(2**64-1))
    buf += struct.pack("Q",n >> 64)
    return buf

class Serializer(Protocol):
    """Base Serializer Protocol"""

    def serialize(self, v: Any) -> Any:
        ...

    def deserialize(self, v: Any) -> Any:
        ...


class NameSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return names.serialize_name(v)

    def deserialize(self, v: bytes) -> str:
        return names.deserialize_name(v)


class NumberSerializer(Serializer):
    def __init__(self, type: str):
        self.type = type

    def serialize(self, n: Union[int, float, str]) -> bytes:
        if isinstance(n,str):
            if "int" in self.type:
                n = int(n)
            elif "float" in self.type:
                n = float(n)
            else:
                raise ValueError(f"Value {n} could not be converted to an integer or float")
        if self.type.endswith("128"):
            if isinstance(n,float):
                # TODO: See if I can implement
                raise ValueError("Python doesn't do float128s")
            else:
                return split_and_pack_128(n)
        return struct.pack(DEFAULT_TYPES[self.type], n)

    def deserialize(self, v: bytes) -> str:
        ...


class BooleanSerializer(Serializer):
    def serialize(self, v: bool) -> bytes:
        return b"\x01" if v else b"\x00"

    def deserialize(self, v: Any) -> Any:
        ...

class StringSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return VaruintSerializer().serialize(len(v)) + v.encode("utf-8")

    def deserialize(self, v: Any) -> Any:
        ...

class BytesSerializer(Serializer):
    def serialize(self, v: bytes) -> bytes:
        return VaruintSerializer().serialize(len(v)) + v

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
