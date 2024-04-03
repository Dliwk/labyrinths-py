"""Test utility functions."""

import enum
from dataclasses import dataclass

from labyrinths.utils import dump_to_dict, load_from_dict


class MyEnum(enum.Enum):
    INT = 1
    STR = "str"
    BOOL = True


@dataclass
class MyDataclass3:
    enum_field: MyEnum
    int_field: int


@dataclass
class MyDataclass2:
    enum_field: MyEnum
    nested_dataclass_field: MyDataclass3
    int_field: int


@dataclass
class MyDataclass:
    enum_field: MyEnum
    nested_dataclass_field: MyDataclass2
    int_field: int


my_dataclass = MyDataclass(
    enum_field=MyEnum.INT,
    nested_dataclass_field=MyDataclass2(
        enum_field=MyEnum.STR,
        nested_dataclass_field=MyDataclass3(enum_field=MyEnum.BOOL, int_field=3),
        int_field=7,
    ),
    int_field=-3,
)
dict_dataclass = {
    "enum_field": 1,
    "nested_dataclass_field": {
        "enum_field": "str",
        "nested_dataclass_field": {"enum_field": 1, "int_field": 3},
        "int_field": 7,
    },
    "int_field": -3,
}


def test_dump_to_dict():
    dumped = dump_to_dict(my_dataclass)
    assert dumped == dict_dataclass


def test_load_from_dict():
    loaded = load_from_dict(MyDataclass, dict_dataclass)
    assert loaded == my_dataclass
