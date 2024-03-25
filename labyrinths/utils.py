import dataclasses
import json
from typing import Any
import enum


def load_from_dict[T](cls: type[T], data: dict | Any) -> T:
    if dataclasses.is_dataclass(cls):
        kwargs = {}
        for name, annotation in cls.__annotations__.items():
            kwargs[name] = load_from_dict(annotation, data[name])
        return cls(**kwargs)
    elif issubclass(cls, enum.Enum):
        return cls(data)
    else:
        return cls(data)


def dump_to_dict(obj: Any) -> dict | Any:
    if dataclasses.is_dataclass(obj):
        result = {}
        for name, value in obj.__dict__.items():
            result[name] = dump_to_dict(value)
        return result
    elif isinstance(obj, enum.Enum):
        return obj.value
    else:
        return obj


def load[T](cls: type[T], data: str) -> T:
    return load_from_dict(cls, json.loads(data))


def dump(obj: Any) -> str:
    return json.dumps(dump_to_dict(obj))
