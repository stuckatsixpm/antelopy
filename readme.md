# antelopy

![Workflow Badge](https://github.com/stuckatsixpm/antelopy/actions/workflows/main.yml/badge.svg?branch=main) ![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue) ![PyPI](https://img.shields.io/pypi/v/antelopy?label=PyPI)

*v0.1.5 - initial release*

Drop-in Python ABI cache for Antelope chains with local serialization support. 

## Features
* Serialization of Antelope built-in types
* Caches ABIs for faster serialization of actions
* Support for ABI custom types/variants

## Basic Usage:
*Note: Reading ABIs uses `requests` and is not asynchronous.*

### Instaliation

```bash
pip install antelopy
```

### Example with aioeos
**Loading a contract's ABI into the cache:**
```py
from antelopy import AbiCache

CHAIN_ENDPOINT = "https://wax.eosphere.io"

# Create ABI Cache and read the Atomic Assets contract ABI
abicache = AbiCache(chain_endpoint=CHAIN_ENDPOINT)
abicache.read_abi("atomicassets")
```


**Serializing, signing, and pushing a transaction** *(modified version of aioeos' built-in `EosTransaction.sign_and_push_transaction` function)*
```py
import asyncio
import binascii
import hashlib
from antelopy import AbiCache
from aioeos import EosAccount, EosJsonRpc, EosTransaction, serializer

CHAIN_ENDPOINT = "https://wax.eosphere.io"

# Create ABI Cache and read the Atomic Assets contract ABI
abicache = AbiCache(chain_endpoint=CHAIN_ENDPOINT)
abicache.read_abi("atomicassets")

# Fake Account
wax_account = EosAccount(
    name="testaccount1",
    private_key="your private key"
)

# 
rpc = EosJsonRpc(CHAIN_ENDPOINT)

transaction = EosTransaction(
    # transaction data
)
async def serialize_sign_and_push(transaction: EosTransaction):
    for action in transaction.actions: 
        if isinstance(action.data, dict):
            # This {"binargs": serialized_data} structure emulates
            # the response from the old `abi_json_to_bin` endpoint.
            abi_bin = {"binargs":abicache.serialize_data(action.account,action.name, action.data)}
            action.data = binascii.unhexlify(abi_bin['binargs'])

    chain_id = await RPC.get_chain_id()
    serialized_transaction = serializer.serialize(transaction)

    digest = hashlib.sha256(
        b''.join((chain_id, serialized_transaction, bytes(32)))
    ).digest()

    return await RPC.push_transaction(
        signatures=[key.sign(digest) for key in [wax_account.key]],
        serialized_transaction=(
            binascii.hexlify(serialized_transaction).decode()
        )
    )

await serialize_sign_and_push(transaction)
```

## Todo:
* Implement remaining types
* refactor serializers to class based approach, similar to [aioeos](https://github.com/ulamlabs/aioeos/blob/master/aioeos/serializer.py)
* Implement better type hinting for serialization
* Expand test coverage
* Add examples for aioeos, eospy, and pyantelope