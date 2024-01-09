"""abi.py
Contains the Abi type classes for ABI interactions"""
import logging
from typing import Any, List, Union, cast

from pydantic import BaseModel

from antelopy.exceptions.exceptions import ActionMissingFieldError, SerializationError
from antelopy.serializers import varints
from antelopy.types.serializables import (
    SERIALIZER_MAP,
    BasicSerializable,
    ListSerializable,
)
from antelopy.types.types import DEFAULT_TYPES, ValidTypes


class AbiBaseClass(BaseModel):
    """Inherited subclass for easy data type checks"""

    type: str = ""
    is_list: bool = False


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
    optional: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.type.endswith("[]"):
            self.is_list = True
            self.type = self.type[:-2]
        if self.type.endswith("$"):
            self.optional = True


class AbiStruct(AbiBaseClass):
    name: str
    base: str
    fields: List[AbiStructField]


class AbiAction(AbiBaseClass):
    name: str
    type: str
    ricardian_contract: str
    fields: List[AbiStructField] = []


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
    types: List[str]


class Abi(AbiBaseClass):
    name: str = ""
    version: str = ""
    types: List[AbiType] = []
    structs: List[AbiStruct] = []
    actions: List[AbiAction] = []
    tables: List[AbiTables] = []
    ricardian_clauses: List[AbiRicardianClauses] = []
    error_messages: List[AbiErrorMessages] = []
    abi_extensions: List[AbiExtensions] = []
    variants: List[AbiVariants] = []
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
        return None

    def find_type(self, name: str) -> Union[AbiType, None]:
        type_options = [nt for nt in self.types if name == nt.new_type_name]
        if type_options:
            return type_options[0]

    def find_struct(self, name: str) -> Union[AbiStruct, None]:
        struct_options = [s for s in self.structs if name == s.name]
        if struct_options:
            return struct_options[0]

    def find_variant(self, name: str) -> Union[AbiVariants, None]:
        variant_options = [v for v in self.variants if name == v.name]
        if variant_options:
            return variant_options[0]

    def serialize(self, action: Union[AbiAction, AbiStruct], data: Any) -> bytes:
        buf = b""
        for field in action.fields:
            value = data.get(field.name)
            if value is None:
                if field.optional:
                    continue
                raise ActionMissingFieldError(
                    f"Action {action.name} is missing field {field.name}"
                )
            buf += self.serialize_field(field, value)
        return buf

    def serialize_field(self, field: AbiStructField, value: Any) -> bytes:
        if field.type not in DEFAULT_TYPES:
            # handle custom types
            if t := self.find_type(field.type):
                logging.debug("%s uses internal type %s" % (field.type, t.type))
                new_field = AbiStructField(
                    name=t.new_type_name, type=t.type, is_list=t.is_list
                )
                if field.is_list:
                    return ListSerializable(
                        [
                            self.serialize_field(new_field, list_val)
                            for list_val in value
                        ],
                        serialized=True,
                    ).serialize()
                return self.serialize_field(new_field, value)
            # handle custom structs
            if s := self.find_struct(field.type):
                logging.debug("%s uses internal struct %s" % (field.type, s.name))
                if field.is_list:
                    return ListSerializable(
                        [self.serialize(s, list_val) for list_val in value],
                        serialized=True,
                    ).serialize()
                return self.serialize(s, value)
            if v := self.find_variant(field.type):
                # handle custom variants
                logging.debug("%s uses internal variant %s" % (field.type, v.name))
                if field.is_list:
                    return ListSerializable(
                        [
                            self.serialize_field(
                                AbiStructField(
                                    name=v.name, type=list_val[0], is_list=field.is_list
                                ),
                                list_val,
                            )
                            for list_val in value
                        ],
                        serialized=True,
                    ).serialize()
                variant_type, new_value = value
                buf = varints.serialize_varint(v.types.index(variant_type))
                new_field = AbiStructField(
                    name=v.name, type=variant_type, is_list=field.is_list
                )
                return buf + self.serialize_field(new_field, new_value)
            raise SerializationError(f"Field {field.name} couldn't be serialized.")
        if field.is_list:
            serializable = ListSerializable(value, field.type)
            return serializable.serialize()

        serializable = BasicSerializable(value, SERIALIZER_MAP[field.type])
        return serializable.serialize()
