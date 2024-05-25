import random

our_peace = [
    'A0', 'B0', 'C0', 'D0', 'D1', 'E0', 'F0', 'F2', 'F3',
    'G0', 'G2', 'H0', 'I0', 'I1', 'J0', 'K0', 'K3', 'K4',
    'L0', 'L2', 'L3', 'L4', 'M0', 'M1', 'M3', 'M4',
    'N0', 'N1', 'O0', 'O2', 'O4', 'P0', 'P2', 'Q0', 'Q2',
    'R0', 'R1', 'R2', 'S0', 'S1', 'T0', 'T1', 'T3', 'T4',
    'U0'
]

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
def generate_weighted_list(items):
    weighted_list = []
    for item in items:
        weight = determine_weight(item)
        weighted_list.extend([item] * weight)
    return weighted_list

# 乱数化し、出力する関数
def get_random_item(items):
    weighted_list = generate_weighted_list(items)
    return random.choice(weighted_list)

# 叩く関数
def get_unique_random_items(items):
    unique_items = set(item[0] for item in items)  # アルファベットごとにユニークなセットを作成
    selected_items = []
    while unique_items:
        random_item = get_random_item(items)
        if random_item[0] in unique_items:
            selected_items.append(random_item)
            unique_items.remove(random_item[0])
    return selected_items

# テスト実行
random_items = get_unique_random_items(our_peace)
print(random_items)
