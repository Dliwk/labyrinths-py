import dataclasses
import json
from typing import Any
import enum


def load_from_dict[T](cls: type[T], data: dict | list | Any) -> T:
    annotations = cls.__annotations__ if hasattr(cls, "__annotations__") else cls
    cls = cls.__origin__ if hasattr(cls, "__origin__") else cls

    if dataclasses.is_dataclass(cls):
        kwargs = {}
        for name, annotation in annotations.items():
            kwargs[name] = load_from_dict(annotation, data[name])
        return cls(**kwargs)
    elif issubclass(cls, enum.Enum):
        return cls(data)
    elif issubclass(cls, list):
        return [load_from_dict(annotations.__args__[0], i) for i in data]
    elif issubclass(cls, dict):
        return {
            key: load_from_dict(annotations.__args__[1], value)
            for key, value in data.items()
        }
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
    elif isinstance(obj, list):
        return [dump_to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {key: dump_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def load[T](cls: type[T], data: str) -> T:
    return load_from_dict(cls, json.loads(data))


def dump(obj: Any) -> str:
    return json.dumps(dump_to_dict(obj))


def transposed[T](lst: list[list[T]]) -> list[list[T]]:
    if not lst:
        return []
    return [[lst[i][j] for i in range(len(lst))] for j in range(len(lst[0]))]
