from __future__ import annotations

import binascii
import struct
from datetime import datetime
from typing import Any, List, Protocol, Tuple, Union, TYPE_CHECKING
from antelopy.exceptions import ActionDataNotSerializedError, UnsupportedPackageError
from antelopy.serializers import assets, keys, names, time_points, varints
from antelopy.types.transaction import PreSerializedTransaction

from antelopy.types.types import DEFAULT_TYPES

if TYPE_CHECKING:
    from antelopy.types.transaction import Action, Authorization, TransactionExtension


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


class ActionSerializer(Serializer):
    def serialize(self, v: Action) -> bytes:
        buf = b''
        a=AuthorizationSerializer()
        buf += NameSerializer().serialize(v.account)
        buf += NameSerializer().serialize(v.name)
        buf += ListSerializer().serialize([a.serialize(auth) for auth in v.authorization])
        if isinstance(v.data,bytes):
            buf += VaruintSerializer().serialize(len(v.data))+v.data
        else:
            raise ActionDataNotSerializedError("Action data needs to be serialized before the action can be serialized")
        # account: str
        # name: str
        # authorization: List[Authorization]
        # data: Union[bytes,Dict[str, Any]]
        return buf

    def deserialize(self, v: Any) -> bytes:
        ...


class AssetSerializer(Serializer):
    def serialize(self, v: str) -> bytes:
        return assets.serialize_asset(v)

    def deserialize(self, v: Any) -> bytes:
        ...

class AuthorizationSerializer(Serializer):
    def serialize(self, v: Authorization) -> bytes:
        n = NameSerializer()
        return n.serialize(v.actor)+n.serialize(v.permission)

    def deserialize(self, v: Any) -> bytes:
        return super().deserialize(v)

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


class ListSerializer(Serializer):
    def serialize(self, v: List[bytes]) -> bytes:
        return varints.serialize_varint(len(v)) + b"".join(v)

    def deserialize(self, v: bytes) -> str:
        return names.deserialize_name(v)


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

class TransactionSerializer(Serializer):
    def serialize(self, t: PreSerializedTransaction):
        buf = b''
        buf += TimePointSecSerializer().serialize(t.expiration)
        buf += NumberSerializer("uint16").serialize(t.ref_block_num)
        buf += NumberSerializer("uint32").serialize(t.ref_block_prefix)
        buf += VaruintSerializer().serialize(t.max_net_usage_words)
        buf += NumberSerializer("uint8").serialize(t.max_cpu_usage_ms)
        buf += VaruintSerializer().serialize(t.delay_sec)
        
        # must be serialized
            
        buf += ListSerializer().serialize(t.context_free_actions)
        buf += ListSerializer().serialize(t.actions)
        buf += ListSerializer().serialize(t.transaction_extensions)

            # expiration: TimePointSec = field(
            #     default_factory=lambda: datetime.now() + timedelta(seconds=120)
            # )
            # ref_block_num: UInt16 = 0
            # ref_block_prefix: UInt32 = 0

            # max_net_usage_words: VarUInt = 0
            # max_cpu_usage_ms: UInt8 = 0
            # delay_sec: VarUInt = 0
            # context_free_actions: List[EosAction] = field(default_factory=list)
            # actions: List[EosAction] = field(default_factory=list)
            # transaction_extensions: List[EosExtension] = field(default_factory=list)
        return buf

    def deserialize(self, v: Any) -> bytes:
        return super().deserialize(v)

class TransactionExtensionSerializer(Serializer):
    def serialize(self, v: TransactionExtension) -> bytes:
        return NumberSerializer("uint16").serialize(v.type)+v.data

    def deserialize(self, v: Any) -> bytes:
        return super().deserialize(v)

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
