"""exceptions.py

Exceptions to help flag errors with serialization"""

class ABINotFoundError(Exception):
    """No ABI found for account"""


class ABINotCachedError(Exception):
    """ABI hasn't been cached yet"""


class AccountNotFoundError(Exception):
    """This account couldn't be found"""


class ActionNotFoundError(Exception):
    """Action not found in ABI"""


class ActionMissingFieldError(Exception):
    """Missing field in action serialization"""
