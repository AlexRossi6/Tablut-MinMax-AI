import numpy as np


def actions_white(M,i,j,n_rows,n_col):
    # it takes in input the state and a matrix M which has the camps and castle (or anyway tiles not allowed to the white checker)
    # positions with value 1.
    # Then put value 1 in the position of each checkers in the chessboard
    # and finally compute the DESTINATION INDEXES ALLOWED TO THE CHECKER IN POSITION i,j
    # n_rows=number of rows in the chessboard
    # n_rows=number of columns in the chessboard


    list_actions=[]
    #modify M

    #move up:
    up= -1
    while i+up>0 and M[i + up, j ] == 0:
       list_actions.append([[i,j],[i + up, j]])
       up -= 1

    # move down:
    down = +1
    while i+down<n_rows and M[i + down , j] == 0:
        list_actions.append([[i,j],[i + down , j]])
        down += 1

    # move left:
    left = -1
    while j+left >= 0 and M[i , j + left] == 0:
       list_actions.append([[i,j],[i , j + left]])
       left -= 1

    # move down:
    right = +1
    while j+right < n_col and M[i , j + right] == 0:
        list_actions.append([[i,j],[i , j + right]])
        right += 1

    return list_actions











