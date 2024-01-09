"""transaction_class.py

Contains classes to handle the various different transaction formats used by python libraries

TODO: Conversion from Transaction to Signed
TODO: Conversion from Signed to Packed
"""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel


class Action(BaseModel):
    account: str
    name: str
    authorization: List[Authorization]
    data: Dict[str, Any]


class Authorization(BaseModel):
    actor: str
    permission: str


class TransactionExtension(BaseModel):
    actor: str
    permission: str


class Transaction(BaseModel):
    expiration: str
    ref_block_num: int = 0
    ref_block_prefix: int = 0
    max_net_usage_words: int = 0
    max_cpu_usage_ms: int = 0
    delay_sec: int = 0
    context_free_actions: List[Action] = []
    actions: List[Action] = []
    transaction_extensions: List[TransactionExtension] = []


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
