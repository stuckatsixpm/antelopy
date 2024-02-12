# Serialization with eospy

Antelopy has full integration for the [eospy](https://github.com/eosnewyork/eospy) package.

!!! warning 
    **eospy** was archived in January 2024. While **antelopy** currently supports **eospy**, the package itself is unlikely to receive updates in future from the developers.


!!! note 
    When installing **eospy**, remember that the package is `libeospy` on PyPI.


## Simple token transfer
In this example, a simple token transfer is performed. It is assumed that you have used **eospy** before, and this guide won't cover the usage of the package.

### Initialisation
First, import necessary modules, and then initialize the ABI cache, reading the `eosio.token` account's ABI from chain.

```py hl_lines="10-14" linenums="1"
from decimal import Decimal

import eospy.cleos
import eospy.keys

from antelopy import AbiCache

CHAIN_ENDPOINT = "https://waxtestnet.greymass.com"

abi_cache = AbiCache(
    chain_endpoint=CHAIN_ENDPOINT,
    chain_package="eospy",
)
abi_cache.read_abi("eosio.token")
```
Make sure to include the `chain_package` parameter when creating the AbiCache.

### eospy configuration

Next is defining an RPC and account to use with **eospy**.

!!! danger
    **Don't put your keys in your code. Hardcoding your private key into your code is a huge security risk.**

    For production environments, check out OWASP's [cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) on secrets management.

    For working locally, check out the [Secrets Management](https://microsoft.github.io/code-with-engineering-playbook/continuous-delivery/secrets-management/) article from Microsoft's *Code With Engineering Playbook* for tips on ways to manage secrets for local development. 

    The private key in the example below is one that was randomly generated for these docs, and is not the real key.

``` py linenums="16"
RPC = eospy.cleos.Cleos(url=CHAIN_ENDPOINT)

# DO NOT put your key directly in your code.
wax_account = eospy.keys.EOSKey("5J2yE5oNnEfAmdBQtzLTo979ptHXXidmQXNvDcAFP9AJVMKnmkb")
```

### Creating the transaction
 
First, the transfer action and an transaction `dict` are created, and then the AbiCache's `sign_and_push` function is used to serialize the transaction, sign it, and send it to the chain endpoint.

``` py hl_lines="22" linenums="22" 
def transfer_token():
    transfer_value = Decimal("3.14").quantize(Decimal("1.00000000"))  # (1)!
    transfer_action_data = {
        "from": "professoroak",
        "to": "officerjenny",
        "quantity": f"{transfer_value} WAX",
        "memo": "This is an example transfer!",
    }
    transfer_action = {
        "account": "eosio.token",
        "name": "transfer",
        "authorization": [
            {
                "actor": "professoroak",
                "permission": "active",
            }
        ],
        "data": transfer_action_data,
    }

    transaction = {"actions": [transfer_action]}
    chain_response = abi_cache.sign_and_push(RPC, [wax_account], transaction)
    return chain_response
```

1. I strongly recommend using python's [decimal](https://docs.python.org/3/library/decimal.html) module to handle numbers, especially when calculating values.  
`Decimal.quantize` can be used to format the value to the correct precision.  
e.g. `Decimal("3.14").quantize(Decimal("1.00000000"))` = `Decimal("3.14000000")`


!!! info "The `sign_and_push` function"
    
    
    The `sign_and_push` function in line 43 takes the following arguments:  
    
    | Parameter | Description | Value in example |
    | ------ | ------ | ------ |
    | `rpc` | an `eospy.cleos.Cleos` instance | `RPC` |
    | `signing_accounts` | `list` of `eospy.keys.Keys` instances | `[wax_account]` |
    | `trx` | a `dict` containing the transaction  | `transaction` |
    
    The AbiCache knows from the `#!py chain_package="eospy"` declaration back in the initialisation step that it will be receiving instances of **eospy** classes, and handles the serialization and signing of the transaction accordingly. It then uses the RPC that was passed in the function to push the transaction to the blockchain.
    
Finally, we call the function. The returned response is a `dict` containing the JSON response from the endpoint.

``` py linenums="47"
if __name__ == "__main__":
    response_from_blockchain = transfer_token()
```

### The whole script

``` py linenums="1"
from decimal import Decimal

import eospy.cleos
import eospy.keys

from antelopy import AbiCache

CHAIN_ENDPOINT = "https://waxtestnet.greymass.com"

abi_cache = AbiCache(
    chain_endpoint=CHAIN_ENDPOINT,
    chain_package="eospy",
)
abi_cache.read_abi("eosio.token")

RPC = eospy.cleos.Cleos(url=CHAIN_ENDPOINT)

# DO NOT put your key directly in your code.
wax_account = eospy.keys.EOSKey("5J2yE5oNnEfAmdBQtzLTo979ptHXXidmQXNvDcAFP9AJVMKnmkb")


def transfer_token():
    transfer_value = Decimal("3.14").quantize(Decimal("1.00000000"))
    transfer_action_data = {
        "from": "professoroak",
        "to": "officerjenny",
        "quantity": f"{transfer_value} WAX",
        "memo": "This is an example transfer!",
    }
    transfer_action = {
        "account": "eosio.token",
        "name": "transfer",
        "authorization": [
            {
                "actor": "professoroak",
                "permission": "active",
            }
        ],
        "data": transfer_action_data,
    }

    transaction = {"actions": [transfer_action]}
    chain_response = abi_cache.sign_and_push(RPC, [wax_account], transaction)
    return chain_response


if __name__ == "__main__":
    response_from_blockchain = transfer_token()
```