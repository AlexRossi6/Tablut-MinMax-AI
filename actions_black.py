import random
import functions_black as bl
import copy
def black_checker_actions(board,j,moves,illegal_movess):
    #board is the array that represent the state of the game
    #j is a list containing two indexes (row and column position of the checker)

    L = j[1]
    R = j[1]+1
    U = j[0]
    D = j[0]+1
    camp=0
    if j in illegal_movess:
        camp = board[j[0]][j[1]]

    cond=True
    if U!=0 and board[U-1][j[1]] in [0,1,2,3,4]:
        i=U-1
        while cond and i in range(U-1,-1,-1):
            if board[i][j[1]] in [0,camp]:
                moves.append([j,[i,j[1]]])
                i=i-1
            else:
                 cond=False
    cond=True
    i=D
    if D!=9 and board[D][j[1]] in [0,1,2,3,4]:
        while cond and i in range(D,9):
            if board[i][j[1]] in [0,camp]:
                moves.append([j,[i,j[1]]])
                i+=1
            else:
                cond=False
    cond=True
    i=L-1
    if L!=0 and board[j[0]][L-1] in [0,1,2,3,4]:
        while cond and i in range(L-1,-1,-1):
            if board[j[0]][i]in [0,camp]:
                moves.append([j,[j[0],i]])
                i=i-1
            else:
                cond=False
    cond=True
    i=R
    if R!=9 and board[j[0]][R] in [0,1,2,3,4]:

        while cond and i in range(R,9):
            if board[j[0]][i] in [0,camp]:
                moves.append([j,[j[0],i]])
                i+=1
            else:
                cond=False


    if j not in illegal_movess:
        try:
            moves.remove([j, [4, 4]])
        except ValueError:
            pass
        for i in illegal_movess:
            try:
                moves.remove([j,i])
            except ValueError:
                pass
    else:


        del illegal_movess[((camp-1)*4):(camp*4)]


        try:
            moves.remove([j, [4, 4]])
        except ValueError:
            pass
        for i in illegal_movess:
            try:
                moves.remove([j,i])
            except ValueError:
                pass
    if j[0]==4:
        if j[1]<4:
            for i in range(5,9):
                try:
                    moves.remove([j,[4,i]])
                except ValueError:
                    pass
        else:
            for i in range(0,4):
                try:
                    moves.remove([j,[4,i]])
                except ValueError:
                    pass
    elif j[1]==4:
        if j[0]<4:
            for i in range(5,9):
                try:
                    moves.remove([j,[i,4]])
                except ValueError:
                    pass
        else:
            for i in range(0,4):
                try:
                    moves.remove([j,[i,4]])
                except ValueError:
                    pass
    if j[0] in [1,7]:
        if j[1]<4:
            for i in range(5,9):
                try:
                    moves.remove([j,[j[0],i]])
                except ValueError:
                    pass
        elif j[1]>4:
            for i in range(0,4):
                try:
                    moves.remove([j,[j[0],i]])
                except ValueError:
                    pass
    if j[1] in [1, 7]:
        if j[0] < 4:
            for i in range(5, 9):
                try:
                    moves.remove([j, [i, j[1]]])
                except ValueError:
                    pass
        elif j[0]>4:
            for i in range(0, 4):
                try:
                    moves.remove([j, [i, j[1]]])
                except ValueError:
                    pass






    random.shuffle(moves)
    return moves


def king_actions(board,j,illegal_moves):

    board = bl.convert_board(copy.deepcopy(board),illegal_moves,j)
    L = j[1]
    R = j[1]+1
    U = j[0]
    D = j[0]+1
    k_moves=[]
    cond=True
    if U!=0 and board[U-1][j[1]]==0:
        i=U-1
        while cond and i in range(U-1,-1,-1):
            if board[i][j[1]]==0:
                k_moves.append([i,j[1]])
                i=i-1
            else:
                 cond=False
    cond=True
    i=D
    if D!=9 and board[D][j[1]]==0:
        while cond and i in range(D,9):
            if board[i][j[1]]==0:
                k_moves.append([i,j[1]])
                i+=1
            else:
                cond=False
    cond=True
    i=L-1
    if L!=0 and board[j[0]][L-1] == 0:
        while cond and i in range(L-1,-1,-1):
            if board[j[0]][i]==0:
                k_moves.append([j[0],i])
                i=i-1
            else:
                cond=False
    cond=True
    i=R
    if R!=9 and board[j[0]][R] == 0:

        while cond and i in range(R,9):
            if board[j[0]][i] == 0:
                k_moves.append([j[0],i])
                i+=1
            else:
                cond=False
    for il in illegal_moves:
        try:
            k_moves.remove(il)
        except ValueError:
            pass
    return k_moves