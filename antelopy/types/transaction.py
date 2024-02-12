"""transaction_class.py

Contains classes to handle the various different transaction formats used by python libraries
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from antelopy.exceptions import UnsupportedPackageError


class Action(BaseModel):
    """Pydantic representation of an Antelope Action object"""

    account: str  # Antelope Name
    name: str  # Antelope Name
    authorization: List[Authorization]
    data: Union[bytes, Dict[str, Any]]


class Authorization(BaseModel):
    """Pydantic representation of an Antelope Authorization object"""

    actor: str  # Antelope Name
    permission: str  # Antelope Name


class TransactionExtension(BaseModel):
    """Pydantic representation of an Antelope TransactionExtension object"""

    type: int
    data: bytes


class Transaction(BaseModel):
    """Pydantic representation of an Antelope Transaction object"""

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
        """Converts transaction data from other packages into an antelopy Transaction

        Args:
            package (str): package name (`aioeos`, `eospy`)
            trx (Any): the transaction data

        Raises:
            UnsupportedPackageError: raised when the package provided
                isn't supported by antelopy

        Returns:
            Transaction: an antelopy Transaction
        """
        if package == "aioeos":
            trx = asdict(trx, dict_factory=dict)
            return cls(**trx)
        if package == "eospy":
            return cls(**trx)

        raise UnsupportedPackageError(
            "This Antelope package isn't currently supported by Antelopy"
        )


class PreSerializedTransaction(Transaction):
    """A partially-serialized transaction

    For internal use for transaction serialization"""

    context_free_actions: List[bytes] = []
    actions: List[bytes] = []
    transaction_extensions: List[bytes] = []


class PackedTransaction(BaseModel):
    """Pydantic representation of a PackedTransaction"""

    packed_trx: Union[bytes, str]
    signatures: List[str] = []
    packed_context_free_data: Union[bytes, str] = ""
    compression: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.packed_trx, bytes):
            self.packed_trx = self.packed_trx.decode()
        if isinstance(self.packed_context_free_data, bytes):
            self.packed_context_free_data = self.packed_context_free_data.decode()
