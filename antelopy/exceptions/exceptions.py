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

class ActionDataNotSerializedError(Exception):
    """Action hasn't been serialized yet"""


class ActionMissingFieldError(Exception):
    """Missing field in action serialization"""


class PackageNotDefinedError(Exception):
    """Raised when Antelope package hasn't been specified"""

class SerializationError(Exception):
    """Field was unable to be serialized"""

class UnsupportedPackageError(Exception):
    """This Antelope package used isn't currently supported by Antelopy"""
