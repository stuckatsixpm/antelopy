"""keys.py

Utility functions to serialize EOS keys and signatures into bytes"""

import struct
from datetime import datetime


def serialize_time_point(value:int|float|datetime) -> bytes:
    """Converts a datetime or datetime.timestamp float to serialized bytes with millisecond precision

    Args:
        timestamp (float | datetime): ts
    """    
    if isinstance(value,int):
        pass
    elif isinstance(value,float):
        value = int(value*1000)
    elif isinstance(value,datetime):
        value = int(value.timestamp()*1000)
    else:
        raise TypeError(f"Expected int, float, or datetime. Got {type(value)}")
    return struct.pack("Q",value)

def serialize_time_point_sec(value:int|float|datetime) -> bytes:
    """Converts a datetime or datetime.timestamp float to serialized bytes with second precision

    Args:
        timestamp (float | datetime): ts
    """    
    if isinstance(value,int):
        pass
    elif isinstance(value,float):
        value = int(value)
    elif isinstance(value,datetime):
        value = int(value.timestamp())
    else:
        raise TypeError(f"Expected int, float, or datetime. Got {type(value)}")
    return struct.pack("I",value)
