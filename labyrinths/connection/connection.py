"""Base connection class."""

import gzip
import json
import logging
import socket
import struct
import traceback
from abc import abstractmethod

logger = logging.getLogger(__name__)


class Connection:
    """Base connection class. Hold common functionality."""

    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.sock.setblocking(False)
        self.current_packet: bytes | None = None
        self.current_packet_length: int = 0
        self.errored = False

    def _handle_packet(self, packet: bytes):
        try:
            self.handle_packet(json.loads(gzip.decompress(packet).decode()))
        except Exception:
            logger.debug(
                f"Exception while handling packet: {gzip.decompress(packet).decode()}\n{traceback.format_exc()}"
            )
            self.onerror()

    def handle_packet(self, raw_data: dict):
        ptype, data = raw_data["t"], raw_data["d"]
        if ptype not in ("game.new", "game.sync_info"):
            logger.debug(f"Received packet: {ptype}: {data} ")
        self.do_handle_packet(ptype, data)

    def _send_packet(self, packet: bytes):
        self.sock.send(struct.pack("!I", len(packet)) + packet)

    def send_packet(self, ptype: str, data: dict):
        if ptype not in ("game.new", "game.sync_info"):
            logger.debug(f"Sending packet: {ptype}: {data}")
        self._send_packet(gzip.compress(json.dumps({"t": ptype, "d": data}).encode()))

    def onerror(self):
        self.errored = True

    def update(self):
        while not self.errored:
            try:
                self._handle_packet_part()
            except BlockingIOError:
                break
            except Exception:
                logger.debug(f"Exception while handling packet (low-level)\n{traceback.format_exc()}")
                self.onerror()

    def _handle_packet_part(self):
        if self.current_packet is None:
            self.current_packet_length = struct.unpack("!I", self.sock.recv(4))[0]
            self.current_packet = b""
        self.current_packet += self.sock.recv(self.current_packet_length - len(self.current_packet))
        if self.current_packet_length == len(self.current_packet):
            packet = self.current_packet
            self.current_packet = None
            self._handle_packet(packet)

    @abstractmethod
    def do_handle_packet(self, ptype: str, data: dict) -> None: ...
