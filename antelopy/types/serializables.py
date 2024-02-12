"""serializables.py

Contains classes to hold serializable data"""

from typing import Any, Dict, List, Protocol

from antelopy.types import serializers
from antelopy.types.transaction import PreSerializedTransaction, Transaction


class Serializable(Protocol):
    """Protocol class for serializable classes"""

    def serialize(self) -> bytes:
        """Protocol template for serializable classes"""
        raise NotImplementedError("This hasn't been implemented yet")

    def deserialize(self):
        """Protocol template for serializable classes"""
        raise NotImplementedError("This hasn't been implemented yet")


class BasicSerializable(Serializable):
    """Helper class for serializing basic types"""

    def __init__(self, value: Any, serialization_strategy: serializers.Serializer):
        self.value = value
        self.strategy = serialization_strategy

    def serialize(self):
        """Serialize the serializable's value"""
        return self.strategy.serialize(self.value)

    def deserialize(self):
        """Deserialize the serializable's value"""
        raise NotImplementedError("This hasn't been implemented yet")


class ListSerializable(Serializable):
    """Helper class for serializing lists"""

    def __init__(
        self, values: List[Any], field_type: str = "", serialized: bool = False
    ):
        self.values = values
        self.serialized = serialized
        strategy = SERIALIZER_MAP.get(field_type)
        self.strategy = strategy

    def serialize(self):
        """Serialize the serializable's value"""
        if self.strategy and not self.serialized:
            serialized_values = [self.strategy.serialize(v) for v in self.values]
        else:
            serialized_values = [bytes(b) for b in self.values]
        return serializers.ListSerializer().serialize(serialized_values)

    def deserialize(self):
        """Deserialize the serializable's value"""
        raise NotImplementedError("This hasn't been implemented yet")


class DictSerializable(Serializable):
    """Helper class for serializing dicts or key/value structures"""

    def __init__(
        self,
        values: Dict[str, Serializable],
        serialization_strategy: serializers.Serializer,
    ):
        self.values = values
        self.strategy = serialization_strategy

    def serialize(self):
        """Serialize the serializable's value"""
        return self.strategy.serialize(self.values)

    def deserialize(self):
        """Deserialize the serializable's value"""
        raise NotImplementedError("This hasn't been implemented yet")


class TransactionSerializable(Serializable):
    """Helper class for serializing transactions"""

    def __init__(self, package: str, transaction: Any):
        self.transaction = Transaction.from_ext(package, transaction)

    def serialize(self) -> bytes:
        """Serialize the serializable's value"""
        t = serializers.TransactionExtensionSerializer()
        a = serializers.ActionSerializer()
        preserialized_trx = PreSerializedTransaction(
            expiration=self.transaction.expiration,
            ref_block_num=self.transaction.ref_block_num,
            ref_block_prefix=self.transaction.ref_block_prefix,
            max_net_usage_words=self.transaction.max_net_usage_words,
            max_cpu_usage_ms=self.transaction.max_cpu_usage_ms,
            delay_sec=self.transaction.delay_sec,
            context_free_actions=[
                a.serialize(action) for action in self.transaction.context_free_actions
            ],
            actions=[a.serialize(action) for action in self.transaction.actions],
            transaction_extensions=[
                t.serialize(trx_ext)
                for trx_ext in self.transaction.transaction_extensions
            ],
        )
        return serializers.TransactionSerializer().serialize(preserialized_trx)

    def deserialize(self):
        """Deserialize the serializable's value"""
        raise NotImplementedError("This hasn't been implemented yet")


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
