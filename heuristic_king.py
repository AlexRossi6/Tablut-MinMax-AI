from useful_functions import check_killed_king, create_M, kill_opponent


def heuristic_king(M,M_tiles, ik, jk, pass_kill, killed,h_w_win,free_winpath=50, dangerous_neig=0.5,king_kills_black=6,escape_value=11, castle_value=50, empty_camps_value = 98, full_camps_value = 99, white_value=10,
                    black_value=1,king_value=8):
    h=0.1


    if M_tiles[ik, jk] == escape_value:
        return h_w_win

        # about the king:
        # USEFUL CHESSBOARD KNOWLEDGES:
    if 0 < ik < 8 and 0 < jk < 8:
        #print('check king')
        # cells values summed between king and the end of the chessboard included:
        left_end_king = sum(M[ik, jk - 1::-1])
        right_end_king = sum(M[ik, jk + 1:])
        up_end_king = sum(M[ik - 1::-1, jk])
        down_end_king = sum(M[ik + 1:, jk])
        #print(M)
        #print('l_k:', left_end_king)
        #print('r_k:', right_end_king)
        #print('u_k', up_end_king)
        #print('d_k:', down_end_king)

        #######################################
        # position in which we can win in the next move:
        free=0
        if left_end_king == escape_value:
            h += free_winpath
            free+=1

            #print('winning tile for the king in the left', h)
        # white between king and right escape
        if right_end_king == escape_value:
            h += free_winpath
            free+=1
            #print('winning tile for the king in the right', h)
        # white between king and upper escape
        if up_end_king == escape_value:
            h += free_winpath
            free+=1
            #print('winning tile for the king in the up', h)
        # white between king and upper escape
        if down_end_king == escape_value:
            h += free_winpath
            free+=1
            #print('winning tile for the king in the down', h)

        if free>=2:
            return h_w_win-50


        #######################################
        # if there's the opportunity to kill the king:###
        h += check_killed_king(ik, jk, M, castle_value, empty_camps_value, full_camps_value, black_value, pass_kill,killed,king_value)
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

        h += kill_opponent(ik, jk, M,M_tiles, black_value, white_value, castle_value, full_camps_value, empty_camps_value,
                           king_value, king_kills_black)
        #print('after kill_opponent/final value:', h)
        # about the white checker:
    return h