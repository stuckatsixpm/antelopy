# The ABI Cache

At the core of **antelopy** is the AbiCache class, which stores ABI files and uses them to serialize transaction data into the format required by Antelope smart contracts.

## Initialisation

AbiCache instances must be created with the url for a Antelope chain endpoint.
In this example, a WAX testnet endpoint is used.

```py
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
```

### Initialisation for use with another library

!!! note
    Full integration is currently only supported with **aioeos**

``` py
from antelopy import AbiCache

abi_cache = AbiCache(
    chain_endpoint="https://waxtestnet.greymass.com", 
    chain_package="aioeos", 
)
```

This lets **antelopy** know which library you're working with, as each transactions/actions from each library need to be handled differently.

## Working with ABIs
This section contains examples of how to load ABIs into the AbiCache. It also covers how to write ABIs to the local filesystem for later use, and access the `Abi` objects within the code.

### Reading ABIs from the blockchain
The `read_abi` method of the AbiCache requests a smart contract's ABI from the chain endpoint. This is **not** asynchronous.
The name of the contract account is passed to the function as an argument.
``` py hl_lines="4"
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
abi_cache.read_abi("eosio.token")
```
In this example, the `eosio.token` smart contract is loaded into the cache from the WAX Testnet.

### Reading ABIs from the local filesystem
ABIs can also be read from a local file using `read_abi_from_json`. In addition to the name of the contract account, a path to a json-formatted ABI file is passed to the function.
``` py hl_lines="4"
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
abi_cache.read_abi_from_json("atomicassets", "example_abi_directory/atomicassets.abi")
```

### Accessing ABIs within the AbiCache
**antelopy** takes care of using ABIs to serialize transaction data, however if you wish to access the ABI instance stored within the cache directly, you can use the `get_cached_abi` method. This returns an `Abi` type *(documentation for **antelopy**'s internal types will be added in a future docs update)*.

``` py hl_lines="5"
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
abi_cache.read_abi("atomicassets")
atomicassets_abi = abi_cache.get_cached_abi("atomicassets")
```

### Saving ABIs to the local filesystem
For efficiency, you may wish to save commonly used ABIs locally, so that they don't need to be requested from the chain endpoint each time you initialise the AbiCache.
The `dump_abi` method saves an ABI from the cache locally, taking the name of the contract account and a destination path as arguments.

``` py hl_lines="6"
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
abi_cache.read_abi("eosio.token")

abi_cache.dump_abi("eosio.token", "example_abi_directory/eosio.token.abi")
```

!!! note
    Keep in mind that if the smart contract is updated on chain, you'll likely need to re-download the ABI.



### Getting a JSON `str`` of an ABI
If you want to get a string dump of an ABI, you can use the 

``` py hl_lines="6"
from antelopy import AbiCache

abi_cache = AbiCache(chain_endpoint="https://waxtestnet.greymass.com")
abi_cache.read_abi("eosio.token")

abi_cache.dump_abi_as_json("eosio.token")
```

!!! note
    Keep in mind that if the smart contract is updated on chain, you'll likely need to re-download the ABI.