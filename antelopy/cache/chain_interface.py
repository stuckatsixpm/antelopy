from typing import Any, Dict

import requests

from antelopy.exceptions.exceptions import ABINotFoundError, AccountNotFoundError


class ChainInterface:
    def __init__(self, chain_endpoint: str):
        self.session = requests.Session()
        self.endpoint = chain_endpoint

    def get_raw_abi(self, account_name: str) -> Dict[str, Any]:
        """Reads a raw ABI file from chain

        Args:
            account_name (str): name of account with ABI

        Raises:
            AccountNotFoundError: Account not found on chain
            Exception: Panic #
            ABINotFoundError: Account has no ABI

        Returns:
            Dict[str,Any]: _description_
        """
        r = self.session.post(
            f"{self.endpoint}/v1/chain/get_abi", json={"account_name": account_name}
        )
        s = r.status_code
        if s == 500:
            # TODO: Add specific errors
            raise AccountNotFoundError(
                f"Couldn't find account {account_name}. Error JSON" + "\n" + r.json()
            )
        if s == 200:
            pass
        else:
            raise Exception("Couldn't get data from chain")
        if raw_abi := r.json().get("abi"):
            return raw_abi
        raise ABINotFoundError(f"Couldn't retrieve ABI for {account_name}")

    def get_chain_id(self) -> str:
        """Gets the chain ID from the connected endpoint

        Args:
            account_name (str): name of account with ABI


        Returns:
            bytes: the chain id
        """
        r = self.session.post(f"{self.endpoint}/v1/chain/get_info")
        s = r.status_code

        if s == 200:
            pass
        else:
            raise Exception("Couldn't get data from chain")
        return r.json().get("chain_id")
