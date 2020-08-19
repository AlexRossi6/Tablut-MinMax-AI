# idea: I do an heuristic which needs to indicate the evaluation of the state wrt to a particular checker (of index i,j).
# So must be associated to the checker that you want to move thanks to the action which makes you explore a new state.

from useful_functions import check_killed,check_killed_king, create_M,protection,first_obstacles,kill_opponent
from time import time


def heuristic_white(M,M_tiles, action, ik, jk, pass_kill_king, killed_king, pass_kill,killed, free_winpath=50,white_obstructing=10, checker_in_escape=0.5,dangerous_neig=0.5,kill_black=6,protection_king=10,white_not_protecting=10, escape_value=11, castle_value=50, empty_camps_value = 98, full_camps_value = 99, white_value=10,
                    black_value=1,king_value=8):
    import numpy as np

    #tic= time()

    i = action[1, 0]
    j = action[1, 1]

    old_i = action[0,0]
    old_j = action[0,1]

    # i and j are the indexes of the checkers that i should move
    # ik and jk the king position
    # our_move=1 if we are in this state because of our move
    #the values must be given in order to have escape_values+white_value different from a possible combination with other tiles
    #because of the heuristic 'if white i between escape and king'.

    h = 0
    ########################################################
    #########################################################
    # about the king:
    # USEFUL CHESSBOARD KNOWLEDGES:
    if 0 < ik < 8 and 0 < jk < 8:
        # cells values summed between king and the end of the chessboard included:
        #print(ik,jk)
        left_end_king = sum(M[ik, jk - 1::-1])
        right_end_king = sum(M[ik, jk + 1:])
        up_end_king = sum(M[ik - 1::-1, jk])
        down_end_king = sum(M[ik + 1:, jk])


        #######################################
        # position in which we can win in the next move:
        if left_end_king == escape_value:
            h += free_winpath
            #print('winning tile for the king in the left', str(h))
        # white between king and right escape
        if right_end_king == escape_value:
            h += free_winpath
            #print('winning tile for the king in the right', str(h))
        # white between king and upper escape
        if up_end_king == escape_value:
            h += free_winpath
            #print('winning tile for the king in the up', str(h))
        # white between king and upper escape
        if down_end_king == escape_value:
            h += free_winpath
            #print('winning tile for the king in the down', str(h))

            # one white between victory:
        if left_end_king == escape_value + white_value:
            h -= white_obstructing
            #print('white obstructing victory', str(h))
        # white between king and right escape
        if right_end_king == escape_value + white_value:
            h -= white_obstructing
            #print('white obstructing victory', str(h))
        # white between king and upper escape
        if up_end_king == escape_value + white_value:
            h -= white_obstructing
           #print('white obstructing victory', str(h))
        # white between king and upper escape
        if down_end_king == escape_value + white_value:
            h -= white_obstructing
           #print('white obstructing victory', str(h))

        #######################################
        # if there's the opportunity to kill the king:###
        h += check_killed_king(ik, jk, M, castle_value, empty_camps_value, full_camps_value, black_value,
                         pass_kill_king, killed_king,king_value)
        #print('after king-check_killed', str(h))

        # about the neighbourhood of the king:
        # left neighbour
        l_neig_k = M[ik, jk - 1]
        r_neig_k = M[ik, jk + 1]
        u_neig_k = M[ik - 1, jk]
        d_neig_k = M[ik + 1, jk]

        if l_neig_k == empty_camps_value or l_neig_k == full_camps_value or l_neig_k == black_value:
            h -= dangerous_neig
            #print('dangerous neigh for the king', str(h))
        if r_neig_k == empty_camps_value or r_neig_k == full_camps_value or r_neig_k == black_value:
            h -= dangerous_neig
            #print('dangerous neigh for the king', str(h))
        if u_neig_k == empty_camps_value or u_neig_k == full_camps_value or u_neig_k == black_value:
            h -= dangerous_neig
            #print('dangerous neigh for the king', str(h))
        if d_neig_k == empty_camps_value or d_neig_k == full_camps_value or d_neig_k == black_value:
            h -= dangerous_neig
            #print('dangerous neigh for the king', str(h))

        ######################################################
        #####################################################
        # about the white checker:

        # if the checker occupies a escape position is not good:
        if M[i, j] == escape_value:
            h -= checker_in_escape
            #print('checker in escape tile', str(h))
    #########
    # useful informations to check if white can be killed :
    # white obstacles:

    ################################################################
    # white being killed
    # white neighbours:
    if 0 < i < 8 and 0 < j < 8:
        h += check_killed(i, j, M, castle_value, empty_camps_value, full_camps_value, black_value, pass_kill, killed,king_value)
        #print('after white-check_killed in position',i,j,' heur: ' ,str(h))

    # i am not considering the case of double killing (because rare)




    #protection h+ if the white is protecting, h- if the white is close to the king with no reason.


    k_left_obst,lij, k_right_obst,rij, k_up_obst,uij, k_down_obst,dij = first_obstacles(ik, jk, M)

    h += protection(k_left_obst, i, j,lij, M, white_value, black_value, full_camps_value,protection_king,white_not_protecting)
    h += protection(k_right_obst, i, j,rij, M, white_value, black_value, full_camps_value,protection_king,white_not_protecting)
    h += protection(k_down_obst, i, j,dij, M, white_value, black_value, full_camps_value,protection_king,white_not_protecting)
    h += protection(k_up_obst, i, j,uij, M, white_value, black_value, full_camps_value,protection_king,white_not_protecting)
    #print('after protection_king:',h)

    #black_killed:
    h += kill_opponent(i,j,M,M_tiles,black_value,white_value,castle_value,full_camps_value,empty_camps_value,king_value,kill_black)
    #print('after kill_opponent/final value:',h)


    #print(time()-tic)  #in seconds.
    return h




#note:
######################################
## white protecting the king:
# it's randomly thanks to the fact that the other states in which the king could be killed are negatives
# while the random ones have value 0.
# if the king it's killed too easily this must be changed (maybe depends on the fact that when the checker protect it
# the value of that state is negative because to protect it the white is between the king and the escape)

####################################
# white killing:
# if i give it positive values i risk that the killing has priority on the protection, so better try to kill thanks
# to randomness


# try it:
