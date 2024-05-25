from __future__ import annotations
import asyncio
import websockets


# 私たちの用いる次の一手は以下の構成で2文字で表される．
# {ID}{ピースの設置可能点(左ならば左ほどよい)}
our_peace = [
	"A0",
	"B0",
	"C0",
	"D0", "D1",
	"E0",
	"F0", "F2", "F3",
	"G0", "G2",
	"H0",
	"I0", "I1",
	"J0",
	"K0", "K3", "K4",
	"L0", "L2", "L3", "L4",
	"M0", "M1", "M3", "M4",
	"N0", "N1",
	"O0", "O2", "O4",
	"P0", "P2"
	"Q0", "Q2"
	"R0", "R1", "R2",
	"S0", "S1",
	"T0", "T1", "T3", "T4",
	"U0"]


class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self.p1Actions = ['U034', 'B037', 'J266', 'M149', 'O763', 'R0A3', 'F0C6', 'K113', 'T021', 'L5D2', 'G251', 'E291', 'D057', 'A053']
        self.p2Actions = ['A0AA', 'B098', 'N0A5', 'L659', 'K33B', 'J027', 'E2B9', 'C267', 'U07C', 'M3AD', 'O2BB', 'R41C']
        self.p1turn = 0
        self.p2turn = 0

    @property
    def player_number(self) -> int:
        return self._player_number

    async def close(self):
        await self._socket.close()

    async def play(self):
        while True:
            board = await self._socket.recv()
            action = self.create_action(board)
            await self._socket.send(action)
            if action == 'X000':
                raise SystemExit

    def create_action(self, board):
        actions: list[str]
        turn: int

        if self.player_number == 1:
            actions = self.p1Actions
            turn = self.p1turn
            self.p1turn += 1
        else:
            actions = self.p2Actions
            turn = self.p2turn
            self.p2turn += 1

        if len(actions) > turn:
            return actions[turn]
        else:
            # パスを選択
            return 'X000'

    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
