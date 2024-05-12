"""Player class."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ClientInfo:
    name: str
    color: Tuple[int, int, int]


@dataclass
class Player:
    client: ClientInfo
    x: int
    y: int
