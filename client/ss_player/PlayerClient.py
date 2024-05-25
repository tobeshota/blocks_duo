from __future__ import annotations
import asyncio
import websockets
import logging

import random

our_peace = [
    'A0', 'B0', 'C0', 'D0', 'D1', 'E0', 'F0', 'F2', 'F3',
    'G0', 'G2', 'H0', 'I0', 'I1', 'J0', 'K0', 'K3', 'K4',
    'L0', 'L2', 'L3', 'L4', 'M0', 'M1', 'M3', 'M4',
    'N0', 'N1', 'O0', 'O2', 'O4', 'P0', 'P2', 'Q0', 'Q2',
    'R0', 'R1', 'R2', 'S0', 'S1', 'U0'
]

logging.basicConfig(filename='game_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# 私たちの用いる次の一手は以下の構成で2文字で表される．
# {ID}{ピースの設置可能点(左ならば左ほどよい)}
our_peace = [
	'A0',
	'B0',
	'C0',
	'D0', 'D1',
	'E0',
	'F0', 'F2', 'F3',
	'G0', 'G2',
	'H0',
	'I0', 'I1',
	'J0',
	'K0', 'K3', 'K4',
	'L0', 'L2', 'L3', 'L4',
	'M0', 'M1', 'M3', 'M4',
	'N0', 'N1',
	'O0', 'O2', 'O4',
	'P0', 'P2'
	'Q0', 'Q2'
	'R0', 'R1', 'R2',
	'S0', 'S1',
	'T0', 'T1', 'T3', 'T4',
	'U0']

class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self.p1Actions = ['U034', 'B037', 'J266', 'M149', 'O763', 'R0A3', 'F0C6', 'K113', 'T021', 'L5D2', 'G251', 'E291', 'D057', 'A053']
        self.p2Actions = ['A0AA', 'B098', 'N0A5', 'L659', 'K33B', 'J027', 'E2B9', 'C267', 'U07C', 'M3AD', 'O2BB', 'R41C']
        self.turn = 0

    @property
    def player_number(self) -> int:
        return self._player_number

    async def close(self):
        await self._socket.close()

    async def play(self):
        while True:
            board = await self._socket.recv()
            our_board = self.convert_board(board) #hirosuzu
            self.log_int_board(our_board) #hirosuzu
            action = self.create_action(board)
            await self._socket.send(action)
            if action == 'X000':
                raise SystemExit


    def convert_board(self, board):
        int_board = []
        # 各行のデータ部分のみを抽出して変換
        for row in board.split('\n')[1:]:
            int_row = []
            for cell in row[1:]:
                if cell == '.':
                    int_row.append(0)
                elif cell == 'o':
                    int_row.append(1)
                elif cell == 'x':
                    int_row.append(4)
            int_board.append(int_row)
        return int_board


    def log_int_board(self, board):
        board_str = '\n'.join(' '.join(map(str, row)) for row in board)
        logging.info(f"Board state:\n{board_str}\n")
    
    def create_action(self, board):
        return 'X000'

    # 重みを決定する関数
    def determine_weight(item):
        if item[0] == 'A':
            return 1
        elif item[0] == 'B':
            return 2
        elif item[0] in ['C', 'D']:
            return 3
        elif item[0] in ['E', 'F', 'G', 'H', 'I']:
            return 4
        else:
            return 5

    # 重みをつけたリストを生成する関数
    def generate_weighted_list(self,items):
        weighted_list = []
        for item in items:
            weight = self.determine_weight(item)
            weighted_list.extend([item] * weight)
        return weighted_list

    # 乱数化し、出力する関数
    def get_random_item(self,items):
        weighted_list = self.generate_weighted_list(items)
        return random.choice(weighted_list)

    # 叩く関数
    def get_unique_random_items(self,items):
        unique_items = set(item[0] for item in items)  # アルファベットごとにユニークなセットを作成
        selected_items = []
        while unique_items:
            random_item = self.get_random_item(items)
            if random_item[0] in unique_items:
                selected_items.append(random_item)
                unique_items.remove(random_item[0])
        return selected_items

    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
