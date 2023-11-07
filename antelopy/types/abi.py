import struct
from typing import Any, cast

from pydantic import BaseModel

from ..exceptions.exceptions import ActionMissingFieldError
from ..serializers import keys, names, varints, time_points
from .types import DEFAULT_TYPES, ValidTypes


class AbiBaseClass(BaseModel):
    """Inherited subclass for easy data type checks"""

    type: str = ""
    is_list: bool = False

    def __str__(self):
        return self.type


class AbiType(AbiBaseClass):
    """Types that extend to the standard Antelope types."""

    new_type_name: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.type.endswith("[]"):
            self.is_list = True
            self.type = self.type[:-2]


class AbiStructField(AbiBaseClass):
    name: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.type.endswith("[]"):
            self.is_list = True
            self.type = self.type[:-2]

    def __str__(self):
        return self.type


class AbiStruct(AbiBaseClass):
    name: str
    base: str
    fields: list[AbiStructField]


class AbiAction(AbiBaseClass):
    name: str
    type: str
    ricardian_contract: str
    fields: list[AbiStructField] = []


class AbiTables(AbiBaseClass):
    ...


class AbiRicardianClauses(AbiBaseClass):
    ...


class AbiErrorMessages(AbiBaseClass):
    ...


class AbiExtensions(AbiBaseClass):
    ...


class AbiVariants(AbiBaseClass):
    name: str
    types: list[str]


class Abi(AbiBaseClass):
    name: str = ""
    version: str = ""
    types: list[AbiType] = []
    structs: list[AbiStruct] = []
    actions: list[AbiAction] = []
    tables: list[AbiTables] = []
    ricardian_clauses: list[AbiRicardianClauses] = []
    error_messages: list[AbiErrorMessages] = []
    abi_extensions: list[AbiExtensions] = []
    variants: list[AbiVariants] = []
    # action_results: list = []

    def __init__(self, name: str, **data: Any):
        super().__init__(**data)
        self.name = name
        for action in self.actions:
            for s in self.structs:
                if action.name == s.name:
                    action.fields = s.fields
                    break

    def get_action(self, action_name: str):
        actions = [a for a in self.actions if a.name == action_name]
        if actions:
            return actions[0]

    def resolve_data_type(self, field: AbiType | AbiStructField | str):
        # if field.type in DEFAULT_TYPES:
        #     return field.type
        field_type = str(field)
        if type_options := [t for t in self.types if field_type == t.new_type_name]:
            return type_options[0]
        if struct_options := [s for s in self.structs if field_type == s.name]:
            return struct_options[0]
        if variant_options := [v for v in self.variants if field_type == v.name]:
            return variant_options[0]

        raise Exception

    def serialize_default(self, t: ValidTypes, value: Any) -> bytes:
        """Serializes default Antelope types

        Args:
            t (str): type name
            value (_type_): the basic value to be serialized

        Returns:
            bytes: _description_
        """
        buf = b""
        if t == "name":
            buf += names.serialize_name(value)
        elif t in (
            "uint8",
            "uint16",
            "uint32",
            "uint64",
            "int8",
            "int16",
            "int32",
            "int64",
        ):
            if not isinstance(value, int):
                value = int(value)
            if value < 0:
                bit_length = int(t.split("int")[1])
                value = (1 << bit_length) + value  # quick two's compliment
            buf += struct.pack(DEFAULT_TYPES[t], value)
        elif t in ("float32", "float64"):
            if not isinstance(value, float):
                value = float(value)
            buf += struct.pack(DEFAULT_TYPES[t], value)
        elif t == "string":
            if not isinstance(value, str):
                raise ValueError(
                    f"Expected a string for this field, got {type(value)} instead"
                )
            buf += varints.serialize_varint(len(value)) + value.encode("utf-8")
        elif t == "bool":
            buf += b"\x01" if value else b"\x00"
        elif t == "public_key":
            buf += keys.serialize_public_key(value)
        elif t == "signature":
            buf += keys.serialize_signature(value)
        elif t == "time_point":
            buf += time_points.serialize_time_point(value)
        elif t == "time_point_sec":
            buf += time_points.serialize_time_point_sec(value)
        else:
            raise Exception(f"Type {t} isn't handled yet")
        return buf

    def serialize_list(self, t: AbiType, value: list[Any]) -> bytes:
        buf = b""
        buf += varints.serialize_varint(len(value))
        for i in value:
            if t.type in DEFAULT_TYPES:
                buf += self.serialize_default(cast(ValidTypes, t.type), i)
            else:
                new_type = self.resolve_data_type(t.type)
                if isinstance(new_type, AbiStruct):
                    buf += self.serialize(new_type, i)
                else:
                    buf += self.serialize_non_default(new_type, i)

        return buf

    def serialize_variant(self, variant_types: list[str], value: Any):
        buf = b""

        value_type, v = value
        buf += varints.serialize_varint(variant_types.index(value_type))
        if value_type in DEFAULT_TYPES:
            buf += self.serialize_default(value_type, v)
        else:
            new_type = self.resolve_data_type(value_type)
            if isinstance(new_type, AbiStruct):
                buf += self.serialize(new_type, v)
            else:
                buf += self.serialize_non_default(new_type, v)
        return buf

    def serialize_non_default(
        self, t: AbiType | AbiStructField | AbiVariants, value: Any
    ) -> bytes:
        buf = b""
        # handle types which are just renamed default types
        if t.is_list:
            buf += self.serialize_list(cast(AbiType, t), value)
            return buf
        if isinstance(t.type, str) and t.type in DEFAULT_TYPES:
            buf += self.serialize_default(cast(ValidTypes, t.type), value)
            return buf
        if type_options := [nt for nt in self.types if t.type == nt.new_type_name]:
            buf += self.serialize_non_default(type_options[0], value)
        elif struct_options := [s for s in self.structs if t.type == s.name]:
            s = struct_options[0]
            buf += self.serialize(s, value)
        elif variant_options := [v for v in self.variants if t.type == v.name]:
            variant = variant_options[0]
            buf += self.serialize_variant(variant.types, value)
        return buf

    def serialize(self, action: AbiAction | AbiStruct, data: Any) -> bytes:
        buf = b""
        for field in action.fields:
            value = data.get(field.name)
            if value is None:
                raise ActionMissingFieldError(
                    f"Action {action.name} is missing field {field.name}"
                )

            if field.type in DEFAULT_TYPES and not field.is_list:
                buf += self.serialize_default(cast(ValidTypes, field.type), value)
                # t = [t for t in self.types if t.new_type_name == field.type][0]
                continue
            buf += self.serialize_non_default(field, value)
        return buf
