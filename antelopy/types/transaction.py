"""transaction_class.py

Contains classes to handle the various different transaction formats used by python libraries

TODO: Conversion from Transaction to Signed
TODO: Conversion from Signed to Packed
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from antelopy.exceptions import UnsupportedPackageError


class Action(BaseModel):
    account: str  # Antelope Name
    name: str  # Antelope Name
    authorization: List[Authorization]
    data: Union[bytes, Dict[str, Any]]


class Authorization(BaseModel):
    actor: str  # Antelope Name
    permission: str  # Antelope Name


class TransactionExtension(BaseModel):
    type: int
    data: bytes


class Transaction(BaseModel):
    expiration: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(seconds=120)
    )
    ref_block_num: int = 0
    ref_block_prefix: int = 0
    max_net_usage_words: int = 0
    max_cpu_usage_ms: int = 0
    delay_sec: int = 0
    context_free_actions: List[Action] = []
    actions: List[Action] = []
    transaction_extensions: List[TransactionExtension] = []

    @classmethod
    def from_ext(cls, package: str, trx: Any):
        if package == "aioeos":
            trx = asdict(trx, dict_factory=dict)
            return cls(**trx)
        if package == "eospy":
            return cls(**trx)

        raise UnsupportedPackageError(
            "This Antelope package isn't currently supported by Antelopy"
        )


class PreSerializedTransaction(Transaction):
    context_free_actions: List[bytes] = []
    actions: List[bytes] = []
    transaction_extensions: List[bytes] = []


class SignedTransaction(Transaction):
    signatures: List[str] = []
    context_free_data: bytes = b""


class PackedTransaction(BaseModel):
    compression: int = 0
    packed_context_free_data: str = (
        ""  # this is just data serialized to Antelope Bytes format
    )
    packed_trx: str = ""
    signatures: List[str] = []
