import pytest

from antelopy import AbiCache


@pytest.fixture
def abi_cache():
    cache = AbiCache(chain_endpoint="https://wax.eosphere.io")
    # read from file
    cache.read_abi_from_json("craft.tag", "tests/data/craft.tag.abi")
    cache.read_abi_from_json("atomicassets", "tests/data/atomicassets.abi")
    cache.read_abi_from_json("farmersworld", "tests/data/farmersworld.abi")
    # read from chain
    cache.read_abi("atomictoolsx")
    return cache
