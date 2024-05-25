from __future__ import annotations
import asyncio
import websockets
import logging
import numpy as np
from collections import deque
import random

logging.basicConfig(filename='game_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self.p1Actions = ['U034', 'B037', 'J266', 'M149', 'O763', 'R0A3', 'F0C6', 'K113', 'T021', 'L5D2', 'G251', 'E291', 'D057', 'A053']
        self.p2Actions = ['A0AA', 'B098', 'N0A5', 'L659', 'K33B', 'J027', 'E2B9', 'C267', 'U07C', 'M3AD', 'O2BB', 'R41C']
        self.items=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","U"]
        self.p1turn = 0
        self.p2turn = 0
        self.us = 1
        self.enemy = 4

    @property
    def player_number(self) -> int:
        return self._player_number

    async def close(self):
        await self._socket.close()

    async def play(self):
        while True:
            board = await self._socket.recv()
            our_board = self.convert_board(board)  # hirosuzu
            action = self.create_action(our_board)
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

    def create_action(self, board):
        actions: list[str]
        turn: int

        if self.p1turn == 0 or self.p2turn == 0:
            if self.player_number == 1:
                return "T254"
            self.us = 4
            self.enemy = 1
            return "T699"
      
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

    def determine_weight( item):
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

    def generate_weighted_list(self):
        weighted_list = []
        for item in self.items:
            weight = self.determine_weight(item)
            weighted_list.extend([item] * weight)
        return weighted_list

    def get_random_item(self, items):
        weighted_list = self.generate_weighted_list(items)
        return random.choice(weighted_list)

    # def get_unique_random_items(self, items):
    #     unique_items = set(item[0] for item in items)  # アルファベットごとにユニークなセットを作成
    #     selected_items = []
    #     while unique_items:
    #         random_item = self.get_random_item(items)
    #         if random_item[0] in unique_items:
    #             selected_items.append(random_item)
    #             unique_items.remove(random_item[0])
    #     return selected_items


class ArrayManipulator:
    def __init__(self, array):
        self.original_array = np.array(array)
        self.array = np.array(array)
        self.base = [7, 7]

    def rotate_flip(self, angle, flip):
        result = self.original_array

        if angle == 90:
            result = np.rot90(result, k=-1)
            self.base = [8, 7]
        elif angle == 180:
            result = np.rot90(result, k=2)
            self.base = [8, 8]
        elif angle == 270:
            result = np.rot90(result, k=1)
            self.base = [7, 8]
        else:
            self.base = [7, 7]

        if flip:
            result = np.flip(result, axis=1)
            self.base = [self.base[1], self.base[0]]

        self.array = result

    def __getitem__(self, index):
        angle = (index % 4) * 90
        flip = (index // 4) % 2 == 1
        self.rotate_flip(angle, flip)
        return {"array": self.array, "base": self.base}


def get_neighbors(rows, cols, r, c):
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors


def is_adjacent(array):
    rows, cols = array.shape
    visited = np.zeros_like(array, dtype=bool)

    # Find the first '1' to start the BFS
    start = None
    for r in range(rows):
        for c in range(cols):
            if array[r, c] == 1:
                start = (r, c)
                break
        if start:
            break

    if not start:
        return True  # No '1's in the array

    # Perform BFS
    queue = deque([start])
    visited[start[0], start[1]] = True
    ones_count = np.sum(array == 1)
    connected_count = 0

    while queue:
        r, c = queue.popleft()
        connected_count += 1

        for nr, nc in get_neighbors(rows, cols, r, c):
            if array[nr, nc] == 1 and not visited[nr, nc]:
                visited[nr, nc] = True
                queue.append((nr, nc))

    return connected_count == ones_count


def is_adjacent_with_values(array, value1, value2):
    rows, cols = array.shape
    visited = np.zeros_like(array, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if array[r, c] == value1:
                queue = deque([(r, c)])
                visited[r, c] = True

                while queue:
                    cr, cc = queue.popleft()

                    for nr, nc in get_neighbors(rows, cols, cr, cc):
                        if array[nr, nc] == value2:
                            return True
                        if array[nr, nc] == value1 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))

    return False


def can_set_position(our_board, position, NONE=0, US=1, ENEMY=3):
    if our_board[position[0]][position[1]] > NONE:
        return False
    for i in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        if position[0] + i[0] < 0 or position[0] + i[0] >= len(our_board) or position[1] + i[1] < 0 or position[1] + i[1] >= len(our_board[0]):
            continue
        if our_board[position[0] + i[0]][position[1] + i[1]] in [US, ENEMY]:
            return True
    return False


def can_set_block(our_board, block, NONE=0, US=1, ENEMY=3):
    for i in block["pos"]:
        if not can_set_position(our_board, i, NONE, US, ENEMY):
            return False
    return True


def test_block(our_board, block, NONE=0, US=1, ENEMY=3):
    array_manipulator = ArrayManipulator(block["array"])
    for i in range(8):
        array = array_manipulator[i]
        base = [block["base"][0] - array["base"][0], block["base"][1] - array["base"][1]]
        positions = []
        for r in range(len(array["array"])):
            for c in range(len(array["array"][0])):
                if array["array"][r][c] == 1:
                    new_position = [base[0] + r, base[1] + c]
                    if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= len(our_board) or new_position[1] >= len(our_board[0]):
                        continue
                    positions.append(new_position)
        if len(positions) == 4 and can_set_block(our_board, {"pos": positions}, NONE, US, ENEMY):
            return positions
    return []
