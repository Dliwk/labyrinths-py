"""Client-to-host connection."""

import socket
from typing import Callable

from typing_extensions import override

from labyrinths.connection.connection import Connection


class ClientToHostConnection(Connection):
    """Client-to-host connection."""

    def __init__(self, host: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.setblocking(False)
        super().__init__(sock)

        self.established = False
        self.client_id: int | None = None
        self.send_packet("connection.client.hello", {})

        self.handler: Callable[[str, dict], None] | None = None

    def set_handler(self, handler: Callable[[str, dict], None]):
        assert self.handler is None
        self.handler = handler

    @override
    def onerror(self):
        self.handler("session.closed", {})

    @override
    def do_handle_packet(self, ptype: str, data: dict) -> None:
        if ptype == "connection.host.hello":
            if self.established:
                raise ConnectionError("Got host hello twice.")
            self.established = True
            self.client_id = data["id"]
            self.handler("connection.established", {})
        else:
            if self.established:
                self.handler(ptype, data)
            else:
                raise ConnectionError("Connection not established yet.")
