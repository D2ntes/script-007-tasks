import datetime
import json


def floattime_to_datatime(t: float) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(t)


def bytes2str(b: bytes) -> str:
    return b.decode() if b else None


def str2bytes(s: str) -> bytes:
    return s.encode() if s else None


def json_serialize_helper(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y.%m.%d %H:%M:%S")

    if isinstance(obj, bytes):
        return bytes2str(obj)

    return obj.__dict__


def to_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True, default=json_serialize_helper)
