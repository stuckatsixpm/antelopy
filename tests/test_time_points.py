from binascii import hexlify
from datetime import datetime
from antelopy.serializers import time_points


def test_serialize_time_point():
    assert (
        hexlify(
            time_points.serialize_time_point(1699338215965)
        )
        == b"1d6273a88b010000"
    ), "time_point conversion from int failed"
    assert (
        hexlify(
            time_points.serialize_time_point(1699338215.965562)
        )
        == b"1d6273a88b010000"
    ), "time_point conversion from float failed"
    assert (
        hexlify(
            time_points.serialize_time_point(datetime.fromtimestamp(1699338215.965562))
        )
        == b"1d6273a88b010000"
    ), "time_point conversion from datetime failed"

def test_serialize_time_point_sec():
    assert (
        hexlify(
            time_points.serialize_time_point_sec(1699338215)
        )
        == b"e7d74965"
    ), "time_point_sec conversion from int failed"
    assert (
        hexlify(
            time_points.serialize_time_point_sec(1699338215.965562)
        )
        == b"e7d74965"
    ), "time_point_sec conversion from float failed"
    assert (
        hexlify(
            time_points.serialize_time_point_sec(datetime.fromtimestamp(1699338215.965562))
        )
        == b"e7d74965"
    ), "time_point_sec conversion from datetime failed"


