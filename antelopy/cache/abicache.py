"""abicache.py

Core class of abicache package"""

import json
from binascii import hexlify
from typing import Any
from ..exceptions.exceptions import ABINotCachedError, ActionNotFoundError
from ..types.abi import Abi, Abi
from .chain_interface import ChainInterface


class AbiCache:
    def __init__(self, chain_endpoint: str):
        self.chain = ChainInterface(chain_endpoint)
        self.abi_cache: dict[str, Abi] = {}

    def dump_abi(self, account_name: str, path: str) -> None:
        """Dumps an ABI of an account into path

        Args:
            account_name (str): account name
        """
        raw_abi = self.chain.get_raw_abi(account_name)
        with open(path, "w+") as jfp:
            json.dump(raw_abi, jfp, indent=2)

    def read_abi(self, account_name: str) -> None:
        """Loads an ABI of an account into memory

        Args:
            account_name (str): account name
        """
        raw_abi = self.chain.get_raw_abi(account_name)
        self.abi_cache[account_name] = Abi(name=account_name, **raw_abi)

    def read_abi_from_json(self, account_name: str, path: str) -> None:
        """Loads an ABI of an account into memory

        Args:
            account_name (str): account name
        """
        with open(path, "r") as jfp:
            abi = json.load(jfp)
        self.abi_cache[account_name] = Abi(name=account_name, **abi)

    def serialize_data(
        self, contract_name: str, contract_action: str, data: dict[str, Any]
    ) -> bytes:
        """Serializes an action into a hex-encoded bytestring

        Args:
            contract_name (str): smart contract name
            contract_action (str): smart contract action
            data (dict[str, Any]): action data

        Raises:
            Exception: _description_

        Returns:
            bytes: _description_
        """
        abi = self.abi_cache.get(contract_name)
        if not abi:
            raise ABINotCachedError(
                f"ABI {contract_name} hasn't been cached yet. Use read_abi or read_abi_from_json"
            )
        action = abi.get_action(contract_action)
        if not action:
            raise ActionNotFoundError(
                f"Action {contract_action} not found in ABI for {contract_name}"
            )
        return hexlify(abi.serialize(action, data))
