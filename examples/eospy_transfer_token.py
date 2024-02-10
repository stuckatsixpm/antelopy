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


if __name__ == "__main__":
    print(transfer_token())
