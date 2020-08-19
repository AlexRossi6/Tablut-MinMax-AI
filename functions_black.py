import copy
import actions_black as act


def white_checker_death(state,r,c,illegal_moves):


    if r not in [7,8] and state[r + 1][c] == 'W' and (state[r + 2][c]=='B' or [r+1,c] in [[1,3],[2,4],[1,5],[5,1],[5,7]]):
        return True
    elif r not in [0,1] and state[r - 1][c] == 'W' and (state[r - 2][c] == 'B' or [r-1,c] in [[3, 1], [7, 3], [6, 4], [7, 5], [3, 7]]):
        return True
    elif c not in [0,1] and state[r][c - 1] == 'W' and (state[r][c-2] == 'B' or [r,c-1] in [[1, 5], [3, 1], [4, 2], [5, 1], [7, 5]]):
        return True
    elif c not in [7,8] and state[r][c + 1] == 'W' and (state[r][c+2] == 'B' or [r,c+1] in [[1, 3], [3, 7], [4, 6], [5, 7], [7, 3]]):
        return True
    else:


        return False

def apply_whitedeath(state,r,c):
    if r not in [7,8] and state[r + 1][c] == 'W' and (state[r + 2][c]=='B' or [r+1,c] in [[1,3],[2,4],[1,5],[5,1],[5,7]]):
        state[r+1][c]=0
        return state
    elif r not in [0,1] and state[r - 1][c] == 'W' and (state[r - 2][c] == 'B' or [r-1,c] in [[3, 1], [7, 3], [6, 4], [7, 5], [3, 7]]):
        state[r - 1][c] = 0
        return state
    elif c not in [0,1] and state[r][c - 1] == 'W' and (state[r][c-2] == 'B' or [r,c-1] in [[1, 5], [3, 1], [4, 2], [5, 1], [7, 5]]):
        state[r][c-1] = 0
        return state
    elif c not in [7,8] and state[r][c + 1] == 'W' and (state[r][c+2] == 'B' or [r,c+1] in [[1, 3], [3, 7], [4, 6], [5, 7], [7, 3]]):
        state[r][c+1] = 0
        return state
    return 'error'


def black_checker_death(board,illegal_moves):
    indices = [[i, x] for i in range(9) for x in range(9) if board[i][x] == 'B']

    for move_to in indices:
        U=move_to[0]+1
        D=move_to[0]-1
        R=move_to[1]+1
        L=move_to[1]-1
        if U!=9 and D not in [-1,0] and (board[U][move_to[1]] in ['K','W'] or ([U,move_to[1]] in illegal_moves and move_to not in illegal_moves)) and board[D][move_to[1]]==0:

            check=0
            j=D-1
            while check == 0 and j in range(D-1, -1,-1):
                check=board[j][move_to[1]]
                j= j-1
            if check in ['W','K']:

                return True
            if R!=9 and board[D][R] !='B' :
                check = 0
                j = R
                while check == 0 and j in range(R , 9):
                    check = board[D][j]
                    j = j + 1
                if check in ['W', 'K']:

                    return True
            if L!=-1 and board[D][L] != 'B':
                check = 0
                j = L

                while check == 0 and j in range(L , -1, -1):
                    check = board[D][j]
                    j = j - 1
                if check in ['W', 'K']:

                    return True


        if D!= -1 and U not in [8,9] and (board[D][move_to[1]] in ['K','W'] or ([D, move_to[1]] in illegal_moves and move_to not in illegal_moves)) and board[U][move_to[1]] == 0:

            check = 0
            j = U + 1
            while check==0 and j in range(U + 1,9):
                check = board[j][move_to[1]]
                j =j + 1
            if check in ['W','K']:
                return True
            if R!=9 and board[U][R] != 'B':
                check = 0
                j = R
                while check == 0 and j in range(R , 9):
                    check = board[U][j]
                    j = j + 1
                if check in ['W', 'K']:
                    return True
            if L!=-1 and board[U][L] != 'B':
                check = 0
                j = L
                while check == 0 and j in range(L , -1, -1):
                    check = board[U][j]
                    j = j - 1
                if check in ['W', 'K']:
                    return True

        if R != 9 and L not in[-1,0] and (board[move_to[0]][R] in ['W','K'] or ([move_to[0],R] in illegal_moves and move_to not in illegal_moves)) and board[move_to[0]][L] == 0:

            check = 0
            j = L- 1
            while check == 0 and j in range(L - 1, -1, -1):
                check = board[move_to[0]][j]
                j = j - 1
            if check in ['W','K']:
                return True
            if U!=9 and board[U][L]!='B':
                check = 0
                j = U
                while check == 0 and j in range(U , 9):
                    check = board[j][L]
                    j = j + 1
                if check in ['W', 'K']:
                    return True
            if D!=-1 and board[D][L]!='B':
                check = 0
                j = D
                while check == 0 and j in range(D , -1, -1):
                    check = board[j][L]
                    j = j - 1
                if check in ['W', 'K']:
                    return True

        if L != -1 and R not in [9,8] and (board[move_to[0]][L] in ['W','K'] or ([move_to[0], L] in illegal_moves and move_to not in illegal_moves)) and board[move_to[0]][R]==0:
            check = 0
            j = R +1
            while check == 0 and j in range(R+1,9):
                check = board[move_to[0]][j]
                j = j + 1
                if check in ['W','K']:
                    return True

            if U!=9 and board[U][R] != 'B':
                check = 0
                j = U
                while check == 0 and j in range(U , 9):
                    check = board[j][R]
                    j = j + 1
                if check in ['W', 'K']:
                    return True
            if D!= -1 and board[D][R] != 'B':
                check = 0
                j = D
                while check == 0 and j in range(D , -1, -1):
                    check = board[j][move_to[1]]
                    j = j - 1
                if check in ['W', 'K']:
                    return True

    return False



def king_win_2(board,k_ind1,illegal_moves):

    k_moves=act.king_actions(copy.deepcopy(board),k_ind1,illegal_moves)
    for k_ind0 in k_moves:

        if board[k_ind0[0]][0:k_ind0[1]] == [0 for i in range(0, k_ind0[1])] and (board[k_ind0[0]][(k_ind0[1]+1):9] == [0 for i in range((k_ind0[1]+1), 9)] or [board[i][k_ind0[1]] for i in range(0,k_ind0[0])]==[0 for i in range(0,k_ind0[0])] or [board[i][k_ind0[1]] for i in range(k_ind0[0]+1,9)]==[0 for i in range(k_ind0[0]+1,9)]):
            return True
        elif board[k_ind0[0]][(k_ind0[1]+1):9] == [0 for i in range((k_ind0[1]+1), 9)] and (board[k_ind0[0]][0:k_ind0[1]] == [0 for i in range(0, k_ind0[1])] or [board[i][k_ind0[1]] for i in range(0,k_ind0[0])]==[0 for i in range(0,k_ind0[0])] or [board[i][k_ind0[1]] for i in range(k_ind0[0]+1,9)]==[0 for i in range(k_ind0[0]+1,9)]):
            return True
        elif [board[i][k_ind0[1]] for i in range(0,k_ind0[0])]==[0 for i in range(0,k_ind0[0])] and (board[k_ind0[0]][0:k_ind0[1]] == [0 for i in range(0, k_ind0[1])] or board[k_ind0[0]][(k_ind0[1]+1):9] == [0 for i in range((k_ind0[1]+1), 9)] or [board[i][k_ind0[1]] for i in range(k_ind0[0]+1,9)]==[0 for i in range(k_ind0[0]+1,9)]):
            return True
        elif [board[i][k_ind0[1]] for i in range(k_ind0[0]+1,9)]==[0 for i in range(k_ind0[0]+1,9)] and (board[k_ind0[0]][0:k_ind0[1]] == [0 for i in range(0, k_ind0[1])] or board[k_ind0[0]][(k_ind0[1]+1):9] == [0 for i in range((k_ind0[1]+1), 9)] or [board[i][k_ind0[1]] for i in range(0,k_ind0[0])]==[0 for i in range(0,k_ind0[0])]):
            return True



    return False


def king_3(state,k_ind):

    if k_ind in [[4,3],[4,5],[3,4],[5,4]]:
        ro=k_ind[0]
        co=k_ind[1]
        if state[ro+1][co] in ['K','B'] and state[ro-1][co] in ['K','B'] and state[ro][co+1] in ['K','B'] and state[ro][co + 1] in ['K','B']:
            return True
    else:
        return False



def convert_board(board,illegal_moves,black):


    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                board[i][j] = 5

    board[black[0]][black[1]]=0
    for h in illegal_moves[0:4]:

        if board[h[0]][h[1]] == 0:
            board[h[0]][h[1]] = 1
    for h in illegal_moves[4:8]:
        if board[h[0]][h[1]] == 0:
            board[h[0]][h[1]] = 2
    for h in illegal_moves[8:12]:
        if board[h[0]][h[1]] == 0:
            board[h[0]][h[1]] = 3
    for h in illegal_moves[12:16]:
        if board[h[0]][h[1]] == 0:
            board[h[0]][h[1]] = 4
    return(board)

def move_on_board(state,move):
    board = copy.deepcopy(state)
    board[move[0][0]][move[0][1]] = 0
    board[move[1][0]][move[1][1]] = 'B'
    return board