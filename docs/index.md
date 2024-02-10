---
hide:
  - navigation
  - toc
  - title
title: Home
---

# antelopy
_Python serializer for Antelope blockchain transaction data_  
_Supported Python versions: 3.8+_


## Overview

Since Leap 3.1, the `abi_json_to_bin` endpoint has been deprecated to ensure the integrity of transaction data. **antelopy** offers an drop-in serialization option to support Python-based interaction with Antelope blockchains.


**antelopy** supports the following libraries.

| Antelope Library                                                   | Support Status                                     | Guide                |
| ------------------------------------------------------------------ | -------------------------------------------------- | -------------------- |
| [aioeos *(github)*](https://github.com/ulamlabs/aioeos/)                      | :material-check: Fully integrated                  | [Link](usage/aioeos.md) |
| [eospy *(github)*](https://github.com/eosnewyork/eospy) _(archived Jan 2024)_ | :material-check: Fully integrated                  | [Link](usage/eospy.md) |
| [pyntelope *(github)*](https://github.com/FACINGS/pyntelope/)                 | :material-progress-alert: To do                    | N/A                  |
