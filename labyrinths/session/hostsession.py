"""Host session"""

import random

from labyrinths import utils
from labyrinths.connection.host import HostConnectionSet
from labyrinths.game.game import Game
from labyrinths.session.types import ClientInfo, Player


class HostSession:
    """Host session. Hosts games."""

    def __init__(self, conn_set: HostConnectionSet):
        self.conn_set = conn_set
        self.admin_ids: list[int] = []
        self.conn_set.set_handler(self.handle_packet)
        self.clients: dict[int, ClientInfo] = {}

        self.game: Game | None = None

    def handle_admin_command(self, command: str, data: dict) -> None:
        if command == "new_game":
            self.game = Game(data["w"], data["h"], data.get("algo", "kruskal"))
            self.conn_set.broadcast("game.new", {"maze": utils.dump_to_dict(self.game.maze)})
            for client_id, client in self.clients.items():
                player = Player(self.clients[client_id], 0, 0)
                self.game.players[client_id] = player
                self.conn_set.broadcast("game.new_player", {"id": client_id, "x": player.x, "y": player.y})

    def get_color(self):
        return random.choice([(35, 153, 255), (153, 102, 204), (252, 40, 71), (121, 179, 170), (135, 206, 250)])

    def handle_packet(self, client_id: int, ptype: str, data: dict) -> None:
        if ptype.startswith("admin."):
            if client_id in self.admin_ids:
                self.handle_admin_command(ptype.removeprefix("admin."), data)
            return
        match ptype:
            case "session.client.info":
                self.clients[client_id] = ClientInfo(data["name"], self.get_color())

                conn = self.conn_set.connections[client_id]

                conn.send_packet(
                    "session.sync_info",
                    {
                        "clients": [
                            {"id": other_client_id, "name": client_info.name, "color": client_info.color}
                            for other_client_id, client_info in self.clients.items()
                        ]
                    },
                )

                if self.game:
                    conn.send_packet(
                        "game.sync_info",
                        {
                            "maze": utils.dump_to_dict(self.game.maze),
                            "players": [
                                {"id": player_id, "x": player.x, "y": player.y}
                                for player_id, player in self.game.players.items()
                            ],
                        },
                    )

                self.conn_set.broadcast(
                    "session.client_connected",
                    {"id": client_id, "name": self.clients[client_id].name, "color": self.clients[client_id].color},
                )

                if self.game:
                    self.game.players[client_id] = player = Player(self.clients[client_id], 0, 0)
                    self.conn_set.broadcast("game.new_player", {"id": client_id, "x": player.x, "y": player.y})

            case "session.client.disconnect":
                if client_id in self.clients.keys():
                    self.clients.pop(client_id)
                    self.conn_set.broadcast("session.client_disconnected", {"id": client_id})
                    if self.game and client_id in self.game.players.keys():
                        self.game.players.pop(client_id)
                        self.conn_set.broadcast("game.remove_player", {"id": client_id})

            case "game.client.movement":
                result = self.game.handle_movement(client_id, data["dir"])
                if result is not None:
                    self.conn_set.broadcast("game.movement", {"id": client_id, "x": result[0], "y": result[1]})
                if self.game.winner_id is not None and not self.game.ended:
                    self.game.ended = True
                    self.conn_set.broadcast("game.winner", {"id": self.game.winner_id})
                    self.conn_set.broadcast("game.show_solution", {})

            case "game.client.chat":
                self.conn_set.broadcast("game.chat", {"id": client_id, **data})
