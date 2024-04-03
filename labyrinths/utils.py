"""Utility functions for different purposes."""

import dataclasses
import enum
import json
import typing
from types import GenericAlias
from typing import Any, TypeVar

# Mypy doesn't support PEP695 generics yet.
T = TypeVar("T")


# Hard to static type this function, giving up.
@typing.no_type_check
def load_from_dict(cls: type[T] | GenericAlias, data: dict | list | Any) -> T:
    """Load arbitrary annotated class from a dict."""
    annotations: dict[str, Any] | GenericAlias = cls.__annotations__ if hasattr(cls, "__annotations__") else cls
    cls = cls.__origin__ if hasattr(cls, "__origin__") else cls  # type: ignore

    print(cls, type(cls))
    if dataclasses.is_dataclass(cls):
        kwargs = {}
        for name, annotation in annotations.items():
            kwargs[name] = load_from_dict(annotation, data[name])
        return cls(**kwargs)
    elif issubclass(cls, enum.Enum):
        return cls(data)
    elif issubclass(cls, list):
        return [load_from_dict(annotations.__args__[0], i) for i in data]
    # elif issubclass(cls, dict):
    #     return {key: load_from_dict(annotations.__args__[1], value) for key, value in data.items()}
    else:
        return cls(data)


def dump_to_dict(obj: Any) -> dict | Any:
    """Dump arbitrary object to a dict."""
    if dataclasses.is_dataclass(obj):
        result = {}
        for name, value in obj.__dict__.items():
            result[name] = dump_to_dict(value)
        return result
    elif isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, list):
        return [dump_to_dict(i) for i in obj]
    # elif isinstance(obj, dict):
    #     return {key: dump_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def load(cls: type[T], data: str) -> T:
    """Load arbitrary annotated class from a json string."""
    return load_from_dict(cls, json.loads(data))


def dump(obj: Any) -> str:
    """Dump arbitrary object into a json string."""
    return json.dumps(dump_to_dict(obj))
