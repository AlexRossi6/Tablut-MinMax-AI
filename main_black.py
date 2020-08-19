import connection as C1
import actions_black as act
import json
import sys
import functions_black as bl
import copy
import numpy as np
from useful_functions import create_M,apply_action
from actions_white import actions_white
from heuristic_white import heuristic_white
from actions_king import actions_king
from result import result
from heuristic_king import heuristic_king
import random
import heuristic_black as heu
import time

def main_black(T=60,server='localhost'):

    # white positive
    free_winpath_white=2 #king can go in a position in which could win
    kill_black=1.9
    protection_king=2   #white protecting the king from being killed
    pass_kill= 0.1

    #white negative
    checker_in_escape=0.5
    dangerous_neig_white=0.5
    white_obstructing=1
    white_not_protecting=1.9
    killed = 1.8

    #king positive:
    h_w_win=0
    free_winpath_king=2 #re si porta in posizione vittoria grazie al suo movimento
    king_kills_black=1.8
    pass_kill_king=0.1

    #king negative
    dangerous_neig_king=0.5
    killed_king = 0

    #black:
    h_black_win=500

    #black heuristic
    black_win = 1000
    black_loose = 1000
    black_checker_death=5
    white_checker_death=4
    strategic_position=3
    move_strategic_position=2
    black_near_king=4





    Tablut_dict={'EMPTY':0,'BLACK':'B','WHITE':'W','KING':'K','THRONE':0}
    l1=['a','b','c','d','e','f','g','h','i']
    l2=['1','2','3','4','5','6','7','8','9']
    l3=[]
    for i in l1:
        for j in l2:
            l3.append(i+j)
    Board_dict={}
    ind=0
    for i in range(9):
        for j in range(9):
            Board_dict[str([j,i])]=l3[ind]
            ind+=1

    escape_value=11
    castle_value=50
    empty_camps_value = 98
    full_camps_value = 99
    white_value=10
    black_value=1
    king_value=8




    Tablut_connection = C1.Player(1,'barbarians',server)
    sys.setrecursionlimit(10000)
    while True:
        try :

            board=Tablut_connection.read()
            board = board.decode()
            board = json.loads(board)
            turn = board['turn']
            board=board['board']
            board_java=np.array(board)


            king_indexes = list(zip(*np.where(board_java == 'KING')))
            ik = king_indexes[0][0]
            jk = king_indexes[0][1]
            # king indexes

            if turn == 'BLACK':




                for i in range(9):
                    for j in range(9):

                            board[i][j]=Tablut_dict[board[i][j]]


                indices = [[i, x] for i in range(9) for x in range(9) if board[i][x] == 'B']
                illegal_moves = [[0, 3], [0, 4], [0, 5], [1, 4], [8, 3], [8, 4], [8, 5], [7, 4], [3, 0], [4, 0], [5, 0],
                                 [4, 1], [3, 8], [4, 8], [5, 8], [4, 7],[4,4]]


                moves = []
                for j in indices:
                    board_conv = bl.convert_board(copy.deepcopy(board), illegal_moves, j)
                    moves = act.black_checker_actions(board_conv, j, moves, copy.deepcopy(illegal_moves))


                random.shuffle(moves)

                h_max = -1000000
                move = []
                for action in moves:
                    new_board = bl.move_on_board(board, action)

                    h_b = heu.utility(new_board,action[0], action[1][0], action[1][1], illegal_moves,black_win, black_loose,black_checker_death,white_checker_death,strategic_position,move_strategic_position,black_near_king)

                    #print(h_b, sep=' ', end='', flush=True)


                    M, M_tiles, M_converted = create_M(board_java)
                    #action=np.array(action)
                    M,M_converted=result(M,M_converted,king_indexes,black_value,white_value,castle_value,empty_camps_value, full_camps_value, king_value, action, turn='BLACK')
                    M=np.array(M)
                    white_positions = list(zip(*np.where(M == white_value)))

                    list_actions_white = []
                    for indexes in white_positions:
                        list_actions_white += actions_white(M, indexes[0], indexes[1], 9, 9)

                    king_actions = actions_king(M, ik, jk, 9, 9, escape_value)
                    list_actions_white = np.array(list_actions_white)

                    h_w_max = -10000
                    # random.shuffle(list_actions)  # shuffle method maybe is not going to contain all the actions, but some repeated??
                    pass_kill_king, killed_king = 0.1, 1000
                    pass_kill, killed = 0.1, 4.5

                    for action_king in king_actions:
                        action_king = np.array(action_king)
                        M_result, M_converted_result = apply_action(M, M_converted, action_king)
                        # the Matrix given in output from apply action has still the checkers to be eliminated if killed
                        i = action_king[0, 0]
                        j = action_king[0, 1]
                        ik_result = action_king[1, 0]
                        jk_result = action_king[1, 1]

                        h_w = heuristic_king(M_result, M_tiles, ik_result, jk_result, pass_kill_king, killed_king,h_w_win,
                                             free_winpath_king, dangerous_neig_king, king_kills_black, escape_value,
                                             castle_value, empty_camps_value, full_camps_value, white_value,
                                             black_value, king_value
                                             )

                        if h_w > h_w_max:
                            h_w_max = h_w






                    for white_action in list_actions_white:

                        M_result, M_converted = apply_action(M, M_converted, white_action)
                        h_w = heuristic_white(M_result,M_tiles, white_action, ik, jk, pass_kill_king, killed_king, pass_kill, killed,
                                              free_winpath_white, white_obstructing, checker_in_escape,
                                              dangerous_neig_white, kill_black, protection_king, white_not_protecting,
                                              escape_value, castle_value, empty_camps_value, full_camps_value,
                                              white_value,
                                              black_value, king_value)
                        if h_w >= h_w_max:
                            h_w_max = h_w

                    h= h_b - h_w_max
                    if h > h_max:
                        h_max = h

                        move = action

                #print('actions', moves)
                #print('choosen', h_max)
                #print(np.array(board))

                #print(move)

                #print("{'from':"+Board_dict[str(move[0])]+",'to':"+Board_dict[str(move[1])]+",'turn':'BLACK'}")
                Tablut_connection.send("{'from':"+Board_dict[str(move[0])]+",'to':"+Board_dict[str(move[1])]+",'turn':'BLACK'}")


        except SyntaxError:
            pass


    #prova.send("{'from':'e2','to':'f2','turn':'BLACK'}")
    #prova.send("{'from':'e2','to':'f2','turn':'BLACK'}")
