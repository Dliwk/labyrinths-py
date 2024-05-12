"""Host connection functionality."""

from __future__ import annotations

import logging
import socket
import traceback
from typing import Callable

from typing_extensions import override

from labyrinths.connection.connection import Connection


class HostConnectionSet:
    """Stores list of host-to-client connections."""

    def __init__(self, addr: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((addr, port))
        self.sock.setblocking(False)
        self.sock.listen(0)

        self.connections: dict[int, HostToClientConnection] = {}
        self._next_client_id = 1

        self.handler: Callable[[int, str, dict], None] | None = None

    def set_handler(self, handler: Callable[[int, str, dict], None]) -> None:
        assert self.handler is None
        self.handler = handler

    def update(self):
        while True:
            try:
                sock, _ = self.sock.accept()
                client_id = self.new_client_id()
                self.connections[client_id] = HostToClientConnection(sock, self, client_id)
            except BlockingIOError:
                break
        for conn in self.connections.values():
            conn.update()

        for client_id in [client_id for client_id, conn in self.connections.items() if conn.dead]:
            del self.connections[client_id]

    def broadcast(self, ptype: str, data: dict):
        for conn in self.connections.values():
            conn.send_packet(ptype, data)

    def new_client_id(self) -> int:
        client_id = self._next_client_id
        self._next_client_id += 1
        return client_id


class HostToClientConnection(Connection):
    """Connection from host to client."""

    def __init__(self, sock: socket.socket, conn_set: HostConnectionSet, client_id: int):
        super().__init__(sock)
        self.conn_set = conn_set
        self.established = False
        self.client_id = client_id
        self.dead = False

    @override
    def onerror(self):
        super().onerror()
        self.disconnect()

    @override
    def do_handle_packet(self, ptype: str, data: dict) -> None:
        if ptype == "connection.client.hello":
            if self.established:
                raise ConnectionError("Got client hello twice")

            self.send_packet("connection.host.hello", {"id": self.client_id})
            self.established = True
        else:
            if self.established:
                self.conn_set.handler(self.client_id, ptype, data)
            else:
                raise ConnectionError("Connection not established yet.")

    def disconnect(self):
        try:
            self.conn_set.handler(self.client_id, "session.client.disconnect", {})
        except Exception:
            logging.debug(f"Exception while handling disconnect\n{traceback.format_exc()}")
        finally:
            self.dead = True
