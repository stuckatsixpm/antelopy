# antelopy

![PyPI](https://img.shields.io/pypi/v/antelopy?label=PyPI) ![Workflow Badge](https://github.com/stuckatsixpm/antelopy/actions/workflows/main.yml/badge.svg?branch=main) ![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

**Documentation:** [https://antelopy.stuckatsixpm.com](https://antelopy.stuckatsixpm.com)  
**Source Code:** [https://github.com/stuckatsixpm/antelopy](https://github.com/stuckatsixpm/antelopy)

---

**antelopy** serializes transaction data for Antelope blockchains, integrating with existing Python packages for ease of use.

In the Antelope's Leap 3.1 release, the `abi_json_to_bin` endpoint was deprecated to ensure the integrity of transaction data. However, available options for interacting with Antelope chains with Python all rely on this endpoint for the serialization step. **antelopy** is designed to handle this process in a non-intrusive way, minimizing changes users of **aioeos** and **eospy** need to make.

## Key Features

- Serialize transaction data in preparation for transaction
- Read ABIs from the blockchain or file, with the option to save for reuse
- Integration wrappers around **aioeos** and **eospy**

**antelopy** supports the following libraries.

| Antelope Library | Support Status                  | Usage Guide             | Repository                                    |
| ---------------- | ------------------------------- | ----------------------- | --------------------------------------------- |
| **aioeos**       | ✔ Fully integrated              | [Link](usage/aioeos.md) | [Link](https://github.com/ulamlabs/aioeos/)   |
| **eospy**        | ✔ Fully integrated[^1]          | [Link](usage/eospy.md)  | [Link](https://github.com/eosnewyork/eospy)   |
| **pyntelope**    | ✘ Waiting for dependency update | N/A                     | [Link](https://github.com/FACINGS/pyntelope/) |

## Basic Usage:

### Installation

```bash
pip install antelopy
```

### Usage

Visit our [documentation](https://antelopy.stuckatsixpm.com) for various examples of how to use **antelopy**!

### Support
**antelopy** is possible thanks to funding from:

[![WAX Labs](docs/_resources/wax_labs_logo.svg)](https://labs.wax.io/)
