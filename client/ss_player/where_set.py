import numpy as np
from collections import deque
from rotate_flip import ArrayManipulator

def get_neighbors(rows,cols,r, c):
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

        for nr, nc in get_neighbors(rows,cols,r, c):
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

                    for nr, nc in get_neighbors(rows,cols,cr, cc):
                        if array[nr, nc] == value2:
                            return True
                        if array[nr, nc] == value1 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))

    return False


def can_set_with_block(our_board, position, NONE=0, US=1, ENEMY=3):
    if our_board[position[0]][position[1]] > NONE:
        return False
    for i in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        if position[0] + i[0] < 0 or position[0] + i[0] >= len(our_board) or position[1] + i[1] < 0 or position[1] + i[1] >= len(our_board[0]):
            continue
        if our_board[position[0] + i[0]][position[1] + i[1]] == US:
            return False
    return True

def can_set_block(our_board, position, our_peace):
    set_block = shift_array(shift_array(our_peace.array, -our_peace.position), position) * 2
    if not is_adjacent(set_block):
        return False
    our_board = our_board + set_block
    if contains_only_specified_values(our_board, [0, 1, 4]):
        return False
    return True

def can_set_position(our_board, position, NONE=0, US=1, ENEMY=4):
    if our_board[position[0]][position[1]] > NONE:
        return False
    for i in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        if position[0] + i[0] < 0 or position[0] + i[0] >= len(our_board) or position[1] + i[1] < 0 or position[1] + i[1] >= len(our_board[0]):
            continue
        if our_board[position[0] + i[0]][position[1] + i[1]] == US:
            return False
    for i in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
        if position[0] + i[0] < 0 or position[0] + i[0] >= len(our_board) or position[1] + i[1] < 0 or position[1] + i[1] >= len(our_board[0]):
            continue
        if our_board[position[0] + i[0]][position[1] + i[1]] == ENEMY:
            return True
    return False

def where_set(our_board,NONE=0, US=1, ENEMY=4):
    ret = []
    for pindex, p in enumerate(our_board):
        for qindex, q in enumerate(p):
            if can_set_position(our_board, [pindex, qindex],NONE=0, US=1, ENEMY=4):
                ret.append([pindex, qindex])
    return ret

def shift_array(array, shift):
    shift_vertical, shift_horizontal = shift
    shifted_array = np.roll(array, shift=shift_vertical, axis=0)  # 行方向のシフト
    shifted_array = np.roll(shifted_array, shift=shift_horizontal, axis=1)  # 列方向のシフト
    return shifted_array

def contains_only_specified_values(array, valid_values):
    valid_values_set = set(valid_values)
    unique_values = np.unique(array)
    
    for value in unique_values:
        if value not in valid_values_set:
            return False
    return True


def test_block(our_board, our_peace, type=0):
    set_position = where_set(our_board)
    for i in set_position:
        test_array = ArrayManipulator(our_peace)[type]
        if can_set_block(our_board, i, test_array) and is_adjacent_with_values(our_board):
            return {
                'position': i,
                'array': test_array
            }
    return False

def get_position(set_array):
    top=1000
    left=1000
    for i in range(len(set_array)):
        for j in range(len(set_array[i])):
            if set_array[i][j] == 2:
                if i < top:
                    top = i
                if j < left:
                    left = j
    return [top, left]
