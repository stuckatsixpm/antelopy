from typing import Any, Dict, List, Protocol

from antelopy.types import serializers


class Serializable(Protocol):
    def serialize(self):
        ...

    def deserialize(self):
        ...


class BasicSerializable(Serializable):
    def __init__(self, value: Any, serialization_strategy: serializers.Serializer):
        self.value = value
        self.strategy = serialization_strategy

    def serialize(self):
        return self.strategy.serialize(self.value)

    def deserialize(self):
        return self.strategy.deserialize(self.value)


class ListSerializable(Serializable):
    def __init__(
        self, values: List[Serializable], serialization_strategy: serializers.Serializer
    ):
        self.values = values
        self.strategy = serialization_strategy

    def serialize(self):
        serialized_values = [v.serialize() for v in self.values]
        return self.strategy.serialize(serialized_values)

    def deserialize(self):
        return self.strategy.deserialize(self.values)


class DictSerializable(Serializable):
    def __init__(
        self,
        values: Dict[str, Serializable],
        serialization_strategy: serializers.Serializer,
    ):
        self.values = values
        self.strategy = serialization_strategy

    def serialize(self):
        return self.strategy.serialize(self.values)

    def deserialize(self):
        return self.strategy.deserialize(self.values)


SERIALIZER_MAP = {
    "asset": serializers.AssetSerializer(),
    "bool": serializers.BooleanSerializer(),
    "bytes": serializers.BytesSerializer(),
    "checksum160": serializers.ChecksumSerializer(),
    "checksum256": serializers.ChecksumSerializer(),
    "checksum512": serializers.ChecksumSerializer(),
    "float32": serializers.NumberSerializer("float32"),
    "float64": serializers.NumberSerializer("float64"),
    "int8": serializers.NumberSerializer("int8"),
    "int16": serializers.NumberSerializer("int16"),
    "int32": serializers.NumberSerializer("int32"),
    "int64": serializers.NumberSerializer("int64"),
    "int128": serializers.NumberSerializer("int128"),
    "name": serializers.NameSerializer(),
    "public_key": serializers.PublicKeySerializer(),
    "signature": serializers.SignatureSerializer(),
    "string": serializers.StringSerializer(),
    "symbol": serializers.SymbolSerializer(),
    "symbol_code": serializers.SymbolCodeSerializer(),
    "time_point": serializers.TimePointSerializer(),
    "time_point_sec": serializers.TimePointSecSerializer(),
    "uint8": serializers.NumberSerializer("uint8"),
    "uint16": serializers.NumberSerializer("uint16"),
    "uint32": serializers.NumberSerializer("uint32"),
    "uint64": serializers.NumberSerializer("uint64"),
    "uint128": serializers.NumberSerializer("uint128"),
    "varint32": serializers.VarintSerializer(),
    "varuint32": serializers.VaruintSerializer(),
}
