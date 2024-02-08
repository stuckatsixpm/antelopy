# Serialization with aioeos

Antelopy has full integration for the [aioeos](https://github.com/ulamlabs/aioeos/) package. 

## Simple token transfer
In this example, a simple token transfer is performed. It is assumed that you have used `aioeos` before, and this guide won't cover the usage of the package.

### Initialisation
First, import necessary modules, and then initialize the ABI cache, reading the `eosio.token` account's ABI from chain.

```py hl_lines="10-14" linenums="1"
import asyncio
from decimal import Decimal
from typing import List

from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction
from antelopy import AbiCache

CHAIN_ENDPOINT = "https://waxtestnet.greymass.com"

abi_cache = AbiCache(
    chain_endpoint=CHAIN_ENDPOINT, 
    chain_package="aioeos", 
)
abi_cache.read_abi("eosio.token")
```
Make sure to include the `chain_package` parameter when creating the AbiCache.

### aioeos configuration

Next is defining an RPC, account, and transfer action to use with `aioeos`.

!!! danger
    **Don't put your keys in your code. Hardcoding your private key into your code is a huge security risk.**

    For production environments, check out OWASP's [cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) on secrets management.

    For working locally, check out the [Secrets Management](https://microsoft.github.io/code-with-engineering-playbook/continuous-delivery/secrets-management/) article from Microsoft's *Code With Engineering Playbook* for tips on ways to manage secrets for local development. 

    The private key in the example below is one that was randomly generated for these docs, and is not the real key.

``` py linenums="16"
RPC = EosJsonRpc(CHAIN_ENDPOINT)

# Configuring the WAX account that will be used to sign the transaction.
# DO NOT put your key directly in your code.
wax_account = EosAccount(
    name="professoroak",
    private_key="5J2yE5oNnEfAmdBQtzLTo979ptHXXidmQXNvDcAFP9AJVMKnmkb"
)

# Making the transfer action
transfer_value = Decimal("3.14").quantize(Decimal("1.00000000")) # (1)!
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
```

1. I strongly recommend using python's [decimal](https://docs.python.org/3/library/decimal.html) module to handle numbers, especially when calculating values.  
`Decimal.quantize` can be used to format the value to the correct precision.  
e.g. `Decimal("3.14").quantize(Decimal("1.00000000"))` = `Decimal("3.14000000")`

### Pushing the transaction
We now need to create an async function to handle signing the transaction and pushing it to the blockchain.

``` py hl_lines="8-12" linenums="39" 
async def main():
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
```

!!! info "The `async_sign_and_push` function"
    
    
    The `async_sign_and_push` function in line 46 takes the following arguments:  
    
    | Parameter | Description | Value in example |
    | ------ | ------ | ------ |
    | `rpc` | an `EosJsonRpc` instance | `RPC` |
    | `signing_accounts` | `list` of `EosAccount` instances | `[wax_account]` |
    | `trx` | an `EosTransaction` instance  | `transaction` |
    
    The AbiCache knows from the `#!py chain_package="aioeos"` declaration back in the initialisation step that it will be receiving instances of `aioeos` classes, and handles the serialization and signing of the transaction accordingly. It then uses the RPC that was passed in the function to push the transaction to the blockchain.
    
Finally, we call the async function. The returned response is a `dict` containing the JSON response from the endpoint.

``` py linenums="53"
if __name__ == "__main__":
    response_from_blockchain = asyncio.run(main())
```

### The whole script

``` py linenums="1"
import asyncio
from decimal import Decimal
from typing import List

from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction
from antelopy import AbiCache

CHAIN_ENDPOINT = "https://waxtestnet.greymass.com"

abi_cache = AbiCache(
    chain_endpoint=CHAIN_ENDPOINT, 
    chain_package="aioeos", 
)
abi_cache.read_abi("eosio.token")

RPC = EosJsonRpc(CHAIN_ENDPOINT)

# Configuring the WAX account that will be used to sign the transaction.
# DO NOT put your key directly in your code.
wax_account = EosAccount(
    name="professoroak",
    private_key="5J2yE5oNnEfAmdBQtzLTo979ptHXXidmQXNvDcAFP9AJVMKnmkb"
)

# Making the transfer action
transfer_value = Decimal("3.14").quantize(Decimal("1.00000000")) # (1)!
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

async def main():
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
    response_from_blockchain = asyncio.run(main())
```