"""Client session."""

from __future__ import annotations

from labyrinths import utils
from labyrinths.connection.client import ClientToHostConnection
from labyrinths.maze import MazeData
from labyrinths.session.types import ClientInfo, Player
from labyrinths.ui import Widget
from labyrinths.ui.widgets.chat import ChatWidget
from labyrinths.ui.widgets.container import Container
from labyrinths.ui.widgets.mazewindow import MazeWidget


class ClientSession:
    """Client session. Used by UI."""

    def __init__(self, conn: ClientToHostConnection, widget: Widget) -> None:
        self.conn = conn
        self.conn.set_handler(self.handle_packet)
        self.ui = widget
        self.maze_container = Container(self.ui, self.ui.width, self.ui.height, 0, 0)
        self.chat_widget = ChatWidget(self.ui, 300, 200, 0, self.ui.height - 200, self.conn)
        self.maze_widget = MazeWidget(self.maze_container, self.maze_container.width, self.maze_container.height, 0, 0)
        self.maze_widget.hide()
        self.maze_widget.on_move_up = self._move_up
        self.maze_widget.on_move_down = self._move_down
        self.maze_widget.on_move_left = self._move_left
        self.maze_widget.on_move_right = self._move_right
        self.maze: MazeData | None = None
        self.players: dict[int, Player] = {}
        self.clients: dict[int, ClientInfo] = {}
        self.our_player_id: int | None = None

        self.dead = False

        self.name = "Player"
        # TODO: other possible fields: player infos, host info, ping, chat messages, etc.

    def _move_up(self):
        self.conn.send_packet("game.client.movement", {"dir": "up"})

    def _move_down(self):
        self.conn.send_packet("game.client.movement", {"dir": "down"})

    def _move_right(self):
        self.conn.send_packet("game.client.movement", {"dir": "right"})

    def _move_left(self):
        self.conn.send_packet("game.client.movement", {"dir": "left"})

    def update(self):
        self.conn.update()

    def handle_packet(self, ptype: str, data: dict):
        match ptype:
            case "connection.established":
                self.conn.send_packet("session.client.info", {"name": self.name})
            case "session.client_connected":
                self.clients[data["id"]] = ClientInfo(data["name"], data["color"])
                self.chat_widget.put('joined.', self.clients[data["id"]].name, self.clients[data["id"]].color)
            case "session.client_disconnected":
                self.chat_widget.put('left.', self.clients[data["id"]].name, self.clients[data["id"]].color)
                self.clients.pop(data["id"])
            case "session.sync_info":
                self.clients = {item["id"]: ClientInfo(item["name"], item["color"]) for item in data["clients"]}
            case "session.closed":
                from labyrinths.ui.widgets.mainmenu import MainMenu

                if not self.dead:
                    self.dead = True
                    self.maze_widget.close()
                    MainMenu(self.ui, self.ui.width, self.ui.height, 0, 0, "server was closed")
            case "game.new":
                self.maze_widget.show()
                self.maze_widget.solution = None
                self.maze_widget.winner_name = None
                self.maze_widget.winner_color = None
                self.maze = utils.load_from_dict(MazeData, data["maze"])
                self.players.clear()
                self.maze_widget.set_maze(self.maze)
                self.maze_widget.set_players(self.players)
            case "game.winner":
                self.maze_widget.winner_name = self.players[data["id"]].client.name
                self.maze_widget.winner_color = self.players[data["id"]].client.color
            case "game.sync_info":
                self.maze_widget.show()
                self.maze = utils.load_from_dict(MazeData, data["maze"])
                self.players = {
                    item["id"]: Player(self.clients[item["id"]], item["x"], item["y"]) for item in data["players"]
                }
                self.maze_widget.set_maze(self.maze)
                self.maze_widget.set_players(self.players)
            case "game.end":
                self.maze_widget.hide()
            case "game.show_solution":
                self.maze_widget.show_solution()
            case "game.new_player":
                self.players[data["id"]] = Player(self.clients[data["id"]], data["x"], data["y"])
            case "game.remove_player":
                self.players.pop(data["id"])
            case "game.movement":
                self.players[data["id"]].x = data["x"]
                self.players[data["id"]].y = data["y"]
            case "game.chat":
                self.chat_widget.put(data['message'], self.clients[data["id"]].name, self.clients[data["id"]].color)

    def admin_command(self, command: str, data: dict):
        self.conn.send_packet(f"admin.{command}", data)
