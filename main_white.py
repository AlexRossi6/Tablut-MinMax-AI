# cd onedrive/desktop/tablut/tablutcompetition/tablut
import connection as C1
import json
import sys
from useful_functions import create_M,apply_action
import numpy as np
from actions_white import actions_white
from heuristic_white import heuristic_white
from actions_king import actions_king
from heuristic_king import heuristic_king
from result import result
import actions_black as act
import functions_black as bl
import random
import heuristic_black as heu
import copy
from conv_matrix import conv_matrix
import time


# heuristic parameters (only absolute values)


# white positive
def main_white(T=60,server='localhost'):

    free_winpath=4  #king can go in a position in which could win
    kill_black=4
    protection_king=10   #white protecting the king from being killed
    pass_kill= 0.1

    #white negative
    checker_in_escape=0.5
    dangerous_neig=0.5
    white_obstructing=1
    white_not_protecting=4
    killed = 4

    #king positive:
    h_w_win=10000
    free_winpath=10
    king_kills_black=3
    pass_kill_king=0.1

    #king negative
    dangerous_neig=0.5
    killed_king = 100000

    #black positive:
    black_win = 1000,
    white_checker_death = 4
    strategic_position = 3
    black_near_king = 4

    #black negative:
    black_loose = 4
    black_checker_death = 5
    move_strategic_position = 2





    Tablut_dict = {'EMPTY': 0, 'BLACK': 'B', 'WHITE': 'W', 'KING': 'K', 'THRONE': 0}
    l1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    l2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    l3 = []

    for i in l1:
        for j in l2:
            l3.append(i + j)  # all possible movements in the java coordinates A1, B1....

    Board_dict = {}
    ind = 0
    for i in range(9):
        for j in range(9):
            Board_dict[str([j, i])] = l3[ind]  # key: A1 value: 00.... (movements)
            ind += 1

    escape_value = 11
    castle_value = 50
    empty_camps_value = 98
    full_camps_value = 99
    white_value = 10
    black_value = 1
    king_value = 8




    Tablut_connection = C1.Player(0, 'barbarians',server)  # 1=black, 0=white
    sys.setrecursionlimit(10000)

    next = True
    first_move = True
    while next:
        #next=input('Wanna see next state?')
        try:

            board = Tablut_connection.read()
            board = board.decode()
            board = json.loads(board)
            turn = board['turn']
            board = board['board']  # array 2D with labels 'EMPTY','BLACK','WHITE','KING','THRONE'
            board = np.array(board)

            out=False

           #print('NEW STATE:\n', board)

            king_indexes = list(zip(*np.where(board == 'KING')))  # king indexes
            ik = king_indexes[0][0]
            jk = king_indexes[0][1]

            if turn == 'WHITE':




                if first_move:
                    move = [[4, 3], [7, 3]]
                    first_move = False
                else:
                    # tic= time()
                    M, M_tiles, M_converted = create_M(board)
                    #print('current M:\n', M)

                    white_positions = list(zip(*np.where(M == white_value)))

                    list_actions = []
                    for indexes in white_positions:
                        list_actions += actions_white(M, indexes[0], indexes[1], 9, 9)
                    # each element in the list_actions has this format: [old_index_i,old_index_j],[new_index_i,new_index_j]
                    # which rapresent the movement to do for a checker

                    king_actions = actions_king(M, ik, jk, 9, 9, escape_value)
                    #print('king actions:\n', king_actions)
                    # list_actions += king_actions
                    list_actions = np.array(list_actions)

                    h_max = -10000
                    list_actions=np.random.permutation(list_actions)
                    king_actions = np.random.permutation(king_actions)

                    for action_king in king_actions:
                        action_king = np.array(action_king)
                        M_action_app_k, M_conv_action_app_k = apply_action(M, M_converted, action_king)
                        # the Matrix given in output from apply action has still the checkers to be eliminated if killed
                        i = action_king[0, 0]
                        j = action_king[0, 1]
                        ik_result = action_king[1, 0]
                        jk_result = action_king[1, 1]

                        h_w = heuristic_king(M_action_app_k, M_tiles, ik_result, jk_result, pass_kill_king, killed_king,h_w_win,
                                             free_winpath, dangerous_neig,king_kills_black,
                                              escape_value, castle_value, empty_camps_value, full_camps_value, white_value,
                                              black_value)
                        if h_w==h_w_win:
                            move=action_king
                            #print('king wins with move:',move)
                            out=True
                            break

                        M_new, M_new_conv = result(M, M_converted, king_indexes, black_value, white_value,
                                                        castle_value, empty_camps_value, full_camps_value, king_value, action_king,
                                                        turn)

                        #print('resulting matrix for the action',action_king)
                        #print(M_new)

                        # black :

                        M_black_conv = conv_matrix(M_new_conv)

                        indices = [[i, x] for i in range(9) for x in range(9) if M_black_conv[i][x] == 'B']
                        illegal_moves = [[0, 3], [0, 4], [0, 5], [1, 4], [8, 3], [8, 4], [8, 5], [7, 4], [3, 0], [4, 0],[5, 0], [4, 1], [3, 8], [4, 8], [5, 8], [4, 7], [4, 4]]



                        list_black_actions = []
                        for j in indices:
                            board_black = bl.convert_board(copy.deepcopy(M_black_conv), illegal_moves,j)

                            list_black_actions = act.black_checker_actions(board_black.tolist(), j, list_black_actions, copy.deepcopy(illegal_moves))

                        h_black_max=-100000
                        for black_action in list_black_actions:


                            new_state = bl.move_on_board(M_black_conv, black_action)
                            h_b = heu.utility(new_state.tolist(), black_action[0], black_action[1][0], black_action[1][1], illegal_moves)

                            #print('heuristic black value for the action',black_action,' : ',h_b)
                            if h_b==black_win:
                                h_black_max=h_b
                                #print('if you do the king action', action_king, ' then the black could do this: ',black_action, 'which has this heuristic: ',h_b)
                                break

                            if  h_b > h_black_max:
                                 h_black_max = h_b
                                 #print('if you do the king action', action_king, ' then the black could do this: ',black_action, 'which has this heuristic: ',h_b)




                        h=h_w - h_black_max
                        if h > h_max:
                            h_max = h
                            move = action_king


                    if not(out):

                        for action in list_actions:
                            #print('action white:', action)
                            M_action_app,M_conv_action_app = apply_action(M, M_converted, action)
                            h_w = heuristic_white(M_action_app,M_tiles, action, ik, jk, pass_kill_king, killed_king, pass_kill, killed,
                                                  free_winpath,white_obstructing, checker_in_escape,dangerous_neig,kill_black,protection_king,white_not_protecting,
                                                escape_value, castle_value, empty_camps_value,
                                                full_camps_value, white_value, black_value, king_value)

                            M_new, M_new_conv = result(M, M_converted, king_indexes, black_value, white_value,
                                                       castle_value, empty_camps_value, full_camps_value, king_value,
                                                       action,
                                                       turn)
                            #print('result matrix after applying the action white',action)
                            #print(M_new)

                            M_black_conv = conv_matrix(M_new_conv)
                            indices = [[i, x] for i in range(9) for x in range(9) if M_black_conv[i][x] == 'B']
                            illegal_moves = [[0, 3], [0, 4], [0, 5], [1, 4], [8, 3], [8, 4], [8, 5], [7, 4], [3, 0], [4, 0],
                                             [5, 0], [4, 1], [3, 8], [4, 8], [5, 8], [4, 7], [4, 4]]



                            list_black_actions = []
                            for j in indices:
                                board_black = bl.convert_board(copy.deepcopy(M_black_conv), illegal_moves,j)
                                list_black_actions = act.black_checker_actions(board_black.tolist(), j, list_black_actions,
                                                                               copy.deepcopy(illegal_moves))

                            h_black_max=-100000
                            for black_action in list_black_actions:
                                new_state = bl.move_on_board(board_black, black_action)
                                h_b = heu.utility(M_black_conv.tolist(), black_action[0], black_action[1][0], black_action[1][1],
                                                  illegal_moves)

                                #print('heuristic black value for the action',black_action,' : ',h_b)

                                if h_b == black_win:
                                    h_black_max = h_b
                                    #print('if you do the white action', action, ' then the black could do this: ',
                                          #black_action, 'which has this heuristic: ',h_b)
                                    break

                                if h_b > h_black_max:
                                    h_black_max = h_b
                                    #print('if you do the white action', action, ' then the black could do this: ',
                                          #black_action, 'which has this heuristic: ',h_b)

                            h = h_w - h_black_max
                            if h > h_max:
                                h_max = h
                                move = action

                move=np.array(move)
                move = [[move[0,0],move[0,1]],[move[1,0],move[1,1]]]
                #print('best action:',move)
                #Mnew, M_conv_new = result(M, M_converted, king_indexes, black_value, white_value, castle_value,
                                          #empty_camps_value,
                                          #full_camps_value, king_value, move, turn)
                #print('M_predicted for the white action ',move, '\n',M)
                #print('M_conv_predicted:','\n',M_conv_new)


                #print("{'from':" + Board_dict[str(move[0])] + ",'to':" + Board_dict[str(move[1])] + ",'turn':'WHITE'}")
                Tablut_connection.send("{'from':"+Board_dict[str(move[0])]+",'to':"+Board_dict[str(move[1])]+",'turn':'WHITE'}")


                # print(time()-tic)  #in seconds.


            #if turn == 'BLACK':
             #    Mnew, M_conv_new = result(M, M_converted, king_indexes, black_value, white_value, castle_value,
                                      #empty_camps_value,
                                      #full_camps_value, king_value, move, turn)
              #   print('M_predicted for the white action ', move, '\n', M)
               #  print('M_conv_predicted:', '\n', M_conv_new)

        except SyntaxError:
            pass


    #prova.send("{'from':'e2','to':'f2','turn':'BLACK'}")
#prova.send("{'from':'e2','to':'f2','turn':'BLACK'}")