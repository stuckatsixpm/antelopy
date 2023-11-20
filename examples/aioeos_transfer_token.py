"""aioeos_example.py

A brief example of how to use antelopy with aioeos to push a WAX transfer transaction to chain

Note: aioeos is NOT packaged with antelopy, and can be installed with `pip install aioeos`

Currently, aioeos' serializer is used to serialize the final transaction, however this
functionality will be available in antelopy when v0.2.0 is released.
"""

import asyncio
from decimal import Decimal

from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction, serializer

from antelopy import AbiCache

CHAIN_ENDPOINT = "https://wax.greymass.com"
RPC = EosJsonRpc(url=CHAIN_ENDPOINT)
abi_cache = AbiCache(chain_endpoint=CHAIN_ENDPOINT)
abi_cache.read_abi("eosio.token")


# Don't hard-code keys in production!
wax_account = EosAccount(
    name="testaccount1",
    private_key="your private key",
)


async def serialize_sign_and_push(transaction: EosTransaction):
    for action in transaction.actions:
        if isinstance(action.data, dict):
            # This {"binargs": serialized_data} structure emulates
            # the response from the old `abi_json_to_bin` endpoint.
            abi_bin = {
                "binargs": abi_cache.serialize_data(
                    action.account, action.name, action.data
                )
            }
            action.data = abi_cache.unhexlify(abi_bin["binargs"])

    chain_id = await RPC.get_chain_id()
    serialized_transaction = serializer.serialize(transaction)

    digest = abi_cache.sha256digest(
        b"".join((chain_id, serialized_transaction, bytes(32)))
    )

    return await RPC.push_transaction(
        signatures=[key.sign(digest) for key in [wax_account.key]],
        serialized_transaction=(abi_cache.hexlify(serialized_transaction).decode()),
    )


async def main():
    # I strongly recommend using Decimal if you're calculating the values.
    # Decimal.quantize formats the value to the correct precision.
    # e.g. Decimal("1.5").quantize(Decimal("1.00000000")) = Decimal("1.50000000")
    transfer_value = Decimal("1.5").quantize(Decimal("1.00000000"))
    transfer_action = EosAction(
        account="eosio.token",
        name="transfer",
        authorization=[wax_account.authorization("active")],
        data={
            "from": wax_account.name,
            "to": "testaccount2",
            "quantity": f"{transfer_value} WAX",
            "memo": "This is an example transfer!",
        },
    )

    block = await RPC.get_head_block()
    transaction = EosTransaction(
        ref_block_num=block["block_num"] & 65535,
        ref_block_prefix=block["ref_block_prefix"],
        actions=[transfer_action],
    )

    # This is a dict containing the response from the endpoint
    chain_response = await serialize_sign_and_push(transaction)
    return chain_response


if __name__ == "__main__":
    asyncio.run(main())
