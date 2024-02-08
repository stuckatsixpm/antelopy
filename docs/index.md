---
hide:
  - navigation
  - toc
  - title
title: Home
---

# Antelopy

_Python serializer for Antelope blockchain transaction data_

## Overview

Since Leap 3.1, the `abi_json_to_bin` endpoint has been deprecated to ensure the integrity of transaction data. Antelopy offers an drop-in serialization option to support Python-based interaction with Antelope blockchains.


Antelopy supports the following libraries.

| Antelope Library                                                   | Support Status                                     | Guide                |
| ------------------------------------------------------------------ | -------------------------------------------------- | -------------------- |
| [aioeos](https://github.com/ulamlabs/aioeos/)                      | :material-check: Fully integrated                  | [Link](usage/aioeos.md) |
| [eospy](https://github.com/eosnewyork/eospy) _(archived Jan 2024)_ | :material-progress-pencil: Serialization supported | [Link](usage/eospy.md) |
| [pyntelope](https://github.com/FACINGS/pyntelope/)                 | :material-progress-alert: To do                    | N/A                  |
