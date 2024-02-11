"""abicache.py

Core class of abicache package"""

import binascii
import hashlib
import json
import logging
from typing import Any, Dict, List, Literal, Union

from antelopy.cache.chain_interface import ChainInterface
from antelopy.exceptions.exceptions import (
    ABINotCachedError,
    ActionNotFoundError,
    PackageNotDefinedError,
    UnsupportedPackageError,
)
from antelopy.types.abi import Abi
from antelopy.types.serializables import TransactionSerializable


class AbiCache:
    """Cache for imported ABIs

    ...

    Attributes
    ----------
    chain : str
        Antelope chain endpoint to use
    abi_cache : dict[str, Abi]
        internal cache of Abi objects, indexed by account name.

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(
        self,
        chain_endpoint: str,
        chain_package: Union[Literal["aioeos", "eospy", "pyntelope"], None] = None,
    ):
        self.chain = ChainInterface(chain_endpoint)
        logging.debug(f"[ANTELOPY] initialized with chain endpoint: {chain_endpoint}")
        self.chain_id = binascii.unhexlify(self.chain.get_chain_id())
        logging.debug(f"[ANTELOPY] Chain ID: {self.chain_id}")
        self.chain_package = chain_package
        if self.chain_package:
            logging.debug(f"[ANTELOPY] using chain package: {self.chain_package}")
        self._abi_cache: Dict[str, Abi] = {}

    def dump_abi(self, account_name: str, path: str) -> None:
        """Dumps an ABI of an account into path

        Args:
            account_name (str): account name
        """
        raw_abi = self.chain.get_raw_abi(account_name)
        with open(path, "w+", encoding="utf-8") as jfp:
            json.dump(raw_abi, jfp, indent=2)

    def read_abi(self, account_name: str) -> None:
        """Loads an ABI of an account into memory

        Args:
            account_name (str): account name
        """
        raw_abi = self.chain.get_raw_abi(account_name)
        self._abi_cache[account_name] = Abi(name=account_name, **raw_abi)
        logging.debug(f"[ANTELOPY] successfully imported ABI from: {account_name}")

    def read_abi_from_json(self, account_name: str, path: str) -> None:
        """Loads an ABI of an account into memory

        Args:
            account_name (str): account name
        """
        with open(path, "r", encoding="utf-8") as jfp:
            abi = json.load(jfp)
        self._abi_cache[account_name] = Abi(name=account_name, **abi)
        logging.debug(f"[ANTELOPY] successfully imported ABI from: {account_name}")

    def serialize_data(
        self, contract_name: str, contract_action: str, data: Dict[str, Any]
    ) -> bytes:
        """Serializes an action into a hex-encoded bytestring

        Args:
            contract_name (str): smart contract name
            contract_action (str): smart contract action
            data (Dict[str, Any]): action data

        Raises:
            Exception: _description_

        Returns:
            bytes: _description_
        """
        abi = self._abi_cache.get(contract_name)
        if not abi:
            raise ABINotCachedError(
                f"ABI {contract_name} hasn't been cached yet. Use read_abi or read_abi_from_json"
            )
        action = abi.get_action(contract_action)
        if not action:
            raise ActionNotFoundError(
                f"Action {contract_action} not found in ABI for {contract_name}"
            )
        return binascii.hexlify(abi.serialize(action, data))

    def serialize(self, trx: Any):
        """Serializes a transaction for signing

        Args:
            trx (Transaction): The transaction to be signed. Supported packages:
                aioeos: `EosTransaction`

        Returns:
            bytes: the serialized transaction
        """
        if not self.chain_package:
            raise PackageNotDefinedError("""Antelope package hasn't been specified""")
        t = TransactionSerializable(self.chain_package, trx)
        for action in t.transaction.actions:
            if isinstance(action.data, dict):
                # This {"binargs": serialized_data} structure emulates
                # the response from the old `abi_json_to_bin` endpoint.
                abi_bin = {
                    "binargs": self.serialize_data(
                        action.account, action.name, action.data
                    )
                }
                action.data = self.unhexlify(abi_bin["binargs"])
        for action in t.transaction.context_free_actions:
            if isinstance(action.data, dict):
                # This {"binargs": serialized_data} structure emulates
                # the response from the old `abi_json_to_bin` endpoint.
                abi_bin = {
                    "binargs": self.serialize_data(
                        action.account, action.name, action.data
                    )
                }
                action.data = self.unhexlify(abi_bin["binargs"])
        return t.serialize()

    async def async_sign_and_push(
        self, rpc: Any, signing_accounts: List[Any], trx: Any
    ) -> Dict[str, Any]:
        serialized_transaction = self.serialize(trx)
        package_name = self.chain_package
        if package_name == "aioeos":
            digest = hashlib.sha256(
                b"".join((self.chain_id, serialized_transaction, bytes(32)))
            ).digest()
            return await rpc.push_transaction(
                signatures=[account.key.sign(digest) for account in signing_accounts],
                serialized_transaction=(
                    binascii.hexlify(serialized_transaction).decode()
                ),
            )
        raise UnsupportedPackageError("This package isn't supported by Antelopy yet")

    def hexlify(self, data: bytes) -> bytes:
        """Wrapper around binascii.hexlify to avoid extra imports"""
        return binascii.hexlify(data)

    def unhexlify(self, data: Union[bytes, str]) -> bytes:
        """Wrapper around binascii.unhexlify to avoid extra imports"""
        return binascii.unhexlify(data)

    def sha256digest(self, string: bytes) -> bytes:
        """Wrapper around hashlib.sha256().digest()"""
        return hashlib.sha256(string).digest()