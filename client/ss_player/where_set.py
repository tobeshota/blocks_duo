def can_set_position(our_board,position,NONE=0,US=1,ENEMY=3):
    if our_board[position[0]][position[1]] >NONE:
        return False
    for i in [[-1,0],[1,0],[0,-1],[0,1]]:
        if position[0]+i[0]<0 or position[0]+i[0]>=len(our_board) or position[1]+i[1]<0 or position[1]+i[1]>=len(our_board[0]):
            continue
        if our_board[position[0]+i[0]][position[1]+i[1]]==US:
            return False
    for i in [[-1,-1],[-1,1],[1,-1],[1,1]]:
        if position[0]+i[0]<0 or position[0]+i[0]>=len(our_board) or position[1]+i[1]<0 or position[1]+i[1]>=len(our_board[0]):
            continue
        if our_board[position[0]+i[0]][position[1]+i[1]]==ENEMY:
            return True
    return False

def where_set(our_board):
    ret=[]
    for pindex,p in enumerate(our_board):
        for qindex,q in enumerate(p):
            if can_set_position(our_board,[pindex,qindex]):
                ret.append([pindex,qindex])
    return ret

def can_set_block(our_board,position,our_peace):
    pass