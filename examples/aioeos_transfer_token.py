"""aioeos_transfer_token.py

See https://antelopy.stuckatsixpm.com/latest/usage/aioeos for the corresponding
tutorial/explanation.

"""

import asyncio
from decimal import Decimal

from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction
from antelopy import AbiCache

CHAIN_ENDPOINT = "https://waxtestnet.greymass.com"

abi_cache = AbiCache(
    chain_endpoint=CHAIN_ENDPOINT, 
    chain_package="aioeos", 
)
abi_cache.read_abi("eosio.token")

RPC = EosJsonRpc(CHAIN_ENDPOINT)

# DO NOT put your key directly in your code.
wax_account = EosAccount(
    name="professoroak",
    private_key="5J2yE5oNnEfAmdBQtzLTo979ptHXXidmQXNvDcAFP9AJVMKnmkb"
)

async def transfer_token():
    transfer_value = Decimal("3.14").quantize(Decimal("1.00000000"))
    transfer_action = EosAction(
        account="eosio.token",
        name="transfer",
        authorization=[wax_account.authorization("active")],
        data={
            "from": wax_account.name,
            "to": "officerjenny",
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
    chain_response = await abi_cache.async_sign_and_push(
        RPC, 
        [wax_account], 
        transaction
    )
    return chain_response

if __name__ == "__main__":
    response_from_blockchain = asyncio.run(transfer_token())