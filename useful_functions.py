################################################################
import numpy as np
def create_M(state_matrix):
    import numpy as np

    empty_value = 0
    escape_value = 11
    castle_value = 50
    empty_camps_value = 98
    full_camps_value = 99
    white_value = 10
    black_value = 1
    corner_value = 100
    king_value = 8

    M_converted = state_matrix
    state_matrix[state_matrix == 'EMPTY'] = empty_value
    state_matrix[state_matrix == 'BLACK'] = black_value
    state_matrix[state_matrix == 'WHITE'] = white_value
    state_matrix[state_matrix == 'KING'] = king_value
    state_matrix[state_matrix == 'THRONE'] = 0  #because it's better to do M[4,4]=castle_value

    M_tiles = np.zeros((9, 9), dtype='int')

    # left camps
    M_tiles[3:6, 0] = empty_camps_value
    M_tiles[4, 1] = empty_camps_value
    # right camps
    M_tiles[3:6, 8] = empty_camps_value
    M_tiles[4, 7] = empty_camps_value
    # upper camps
    M_tiles[0, 3:6] = empty_camps_value
    M_tiles[1, 4] = empty_camps_value
    # lower camps
    M_tiles[8, 3:6] = empty_camps_value
    M_tiles[7, 4] = empty_camps_value
    # castle
    M_tiles[4, 4] = castle_value

    escape_indexes = np.array(
        [[0, 1], [0, 2], [0, 6], [0, 7], [1, 0], [2, 0], [6, 0], [7, 0], [8, 1], [8, 2], [8, 6], [8, 7],
         [1, 8], [2, 8], [6, 8], [7, 8]])

    for ind in escape_indexes:
        M_tiles[ind[0], ind[1]] = escape_value
    # corners:
    M_tiles[[0, 8, 8, 0], [0, 8, 0, 8]] = corner_value
    #print('M_tiles:\n',M_tiles)
    #print('M_converted:\n',M_converted)
    M = M_tiles + np.array(M_converted,dtype=int)
    return M , M_tiles , M_converted

###############################################################################
##########################################
################

def apply_action(M,M_converted,action):
    M = np.array(M, dtype=int)
    action=np.array(action)
    M_converted = np.array(M_converted, dtype=int)
    checker_moved_value=M_converted[action[0, 0], action[0, 1]]
    M[action[1, 0], action[1, 1]] += checker_moved_value
    M[action[0, 0], action[0, 1]] -= checker_moved_value
    M_converted[action[1, 0], action[1, 1]] += checker_moved_value
    M_converted[action[0, 0], action[0, 1]] -= checker_moved_value
    return M,M_converted


##########################################################
#######################################
###########
def first_obstacles(i, j, M):
    #returns the first kind of element !=0 on each direction wrt the element in i,j.
    left_obst, right_obst, up_obst, down_obst = 0, 0, 0, 0
    ind = 1
    li,lj,ri,rj=0,0,0,0
    ui,uj,di,dj=0,0,0,0
    o1, o2, o3, o4 = False, False, False, False
    while True:
        if (j-ind)>0:
             if left_obst == 0 and M[i, j - ind] != 0:  # because there are no empty cell in the perimeter so I'm sure that I look into M only until I've reached the limits of the chessboard
                left_obst = M[i, j - ind]
                li=i
                lj=j-ind
                o1 = True  # to say to exit the loop
        else:
            o1 = True

        if (j+ind)<9:
            if right_obst == 0 and M[i, j + ind] != 0:
                right_obst = M[i, j + ind]
                ri,rj=i,j+ind
                o2 = True
        else:
            o2=True

        if (i-ind)>0:
            if up_obst == 0 and M[i - ind, j] != 0:
                up_obst = M[i - ind, j]
                ui,uj=i-ind,j
                o3 = True
        else:
            o3=True

        if (i+ind)<9:
            if down_obst == 0 and M[i + ind, j] != 0:
                down_obst = M[i + ind, j]
                di,dj=i+ind,j
                o4 = True
        else:
            o4=True

            if o1 and o2 and o3 and o4:
                break
        ind += 1

    return left_obst,[li,lj], right_obst,[ri,rj], up_obst,[ui,uj], down_obst,[di,dj]

#######################################################
#######################
#########

def check_killed(i, j, M, castle_value, empty_camps_value, full_camps_value, opponent_value, pass_kill,killed,king_value):
    # opponent value must be black_value if you are white and viceversa.
    # attention: it doesn't work if the checker is in the border of the chessboard (you should put more check conditions
    # to avoid error in the indexing of the matrix to include that case)
    # check_for_king=1 if it is the king the checker to check
    #pass_kill= heuristic value in case of passive killing
    #killed= heuristic value in case of killed in this state
    h=0
    l_neig = M[i, j - 1]
    r_neig = M[i, j + 1]
    u_neig = M[i - 1, j]
    d_neig = M[i + 1, j]

    left_obst,lij, right_obst,rij, up_obst,uij, down_obst,dij = first_obstacles(i, j, M)

    #  diagonal neighbours 1 (position i-1,j-1 wrt the  checker) obstacles:
    id1, jd1 = i - 1, j - 1
    left_obst_dn1,ldij, right_obst_dn1,rdij, up_obst_dn1,uidj, down_obst_dn1,ddij = first_obstacles(id1, jd1, M)

    # diagonal neighbours 2 (position i+1,j+1 wrt the checker) obstacles:
    id2, jd2 = i + 1, j + 1
    left_obst_dn2,ldij2, right_obst_dn2,rdij2, up_obst_dn2,udij2,down_obst_dn2,ddij2 = first_obstacles(id2, jd2, M)

    # a neighbour on the left:
    h += passive_active_killing(l_neig, r_neig, right_obst, id2, jd2, down_obst_dn2, up_obst_dn2, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed, opponent_value,king_value)

    #a neig on the right:
    h += passive_active_killing(r_neig, l_neig, left_obst, id1, jd1, down_obst_dn1, up_obst_dn1, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed, opponent_value,king_value)

    # neigh up:
    h += passive_active_killing(u_neig, d_neig, down_obst, id2, jd2, left_obst_dn2, right_obst_dn2, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed,opponent_value,king_value)

    #neig down:
    h += passive_active_killing(d_neig, u_neig, up_obst, id1, jd1, left_obst_dn1, right_obst_dn1, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed,opponent_value,king_value)
    return h


################
def check_killed_king(i, j, M, castle_value, empty_camps_value, full_camps_value, opponent_value, pass_kill,killed,king_value):
    # opponent value must be black_value if you are white and viceversa.
    # attention: it doesn't work if the checker is in the border of the chessboard (you should put more check conditions
    # to avoid error in the indexing of the matrix to include that case)
    # check_for_king=1 if it is the king the checker to check
    #pass_kill= heuristic value in case of passive killing
    #killed= heuristic value in case of killed in this state
    l_neig = M[i, j - 1]
    r_neig = M[i, j + 1]
    u_neig = M[i - 1, j]
    d_neig = M[i + 1, j]

    left_obst,lij, right_obst,rij, up_obst,uij, down_obst,dij = first_obstacles(i, j, M)

    #  diagonal neighbours 1 (position i-1,j-1 wrt the  checker) obstacles:
    id1, jd1 = i - 1, j - 1
    left_obst_dn1,ldij, right_obst_dn1,rdij, up_obst_dn1,uidj, down_obst_dn1,ddij = first_obstacles(id1, jd1, M)

    # diagonal neighbours 2 (position i+1,j+1 wrt the checker) obstacles:
    id2, jd2 = i + 1, j + 1
    left_obst_dn2,ldij2, right_obst_dn2,rdij2, up_obst_dn2,udij2,down_obst_dn2,ddij2 = first_obstacles(id2, jd2, M)

    # a neighbour on the left:
    h_horiz = passive_active_killing(l_neig, r_neig, right_obst, id2, jd2, down_obst_dn2, up_obst_dn2, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed, opponent_value,king_value)

    #a neig on the right:
    h_horiz= passive_active_killing(r_neig, l_neig, left_obst, id1, jd1, down_obst_dn1, up_obst_dn1, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed, opponent_value,king_value)

    # neigh up:
    h_vert= passive_active_killing(u_neig, d_neig, down_obst, id2, jd2, left_obst_dn2, right_obst_dn2, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed,opponent_value,king_value)

    #neig down:
    h_vert= passive_active_killing(d_neig, u_neig, up_obst, id1, jd1, left_obst_dn1, right_obst_dn1, full_camps_value,
                           empty_camps_value, castle_value, M, pass_kill, killed,opponent_value,king_value)

    if h_horiz>=killed and h_vert>=killed and ( (i==4 and j==4) or (i==4 and j==3) or (i==4 and j==5) or (i==3 and j==4) or (i==5 and j==4) ):
        return killed  #if king in the castle or close to the castle it must be sorrounded horizontally AND vertically

    if h_horiz>=killed or h_vert>=killed and not( (i==4 and j==4) or (i==4 and j==3) or (i==4 and j==5) or (i==3 and j==4) or (i==5 and j==4) ):
        return killed

    return 0

#########################################

def passive_active_killing(neig1, neig2, obst2, id, jd, dn_ob1,dn_ob2,full_camps_value, empty_camps_value, castle_value,
                           M,pass_kill, killed,opponent_value,king_value):
    #returns the value of the heuristic after checking if it is going to be sorrounded.
    # neig1 is the neighbour in the direction 1 which is supposed to be an opponent value.
    #obst 2 the first obstacle along the direction 2.
    #id and jd the indexes of the diagonal neig. needed.
    #dn_obx is the first obstacle of the diagonal element along the direction x
    h=0
    if neig1 == opponent_value or neig1 == empty_camps_value or neig1 == full_camps_value or neig1 == castle_value or neig1==(castle_value+king_value):
        if neig2 == opponent_value or neig2== empty_camps_value or neig2== full_camps_value or neig2 == castle_value or neig2==(castle_value +king_value):
            h += pass_kill  # the checker will be killed in this state
            #print('passive killing', str(h))
        # check if is possible that in the next move it will be sourrended

        if neig2 == 0 and (
                obst2 == opponent_value or obst2 == full_camps_value or dn_ob1 == opponent_value or \
                dn_ob1 == full_camps_value or dn_ob2 == opponent_value or dn_ob2 == full_camps_value or \
                M[id, jd] == opponent_value or M[id, jd] == full_camps_value):
            h -= killed
    return h


def protection(k_obst,i,j,oij,M,white_value,black_value,full_camps_value,protection_king=10,white_not_protecting=10):
    left_obst,xy, right_obst,xy, up_obst,xy, down_obst,xy = first_obstacles(i, j, M)
    h=0
    if oij[0]==i and oij[1]==j and k_obst == white_value :
        if left_obst == black_value or left_obst == full_camps_value or \
            right_obst == black_value or right_obst == full_camps_value or \
            up_obst == black_value or up_obst == full_camps_value or \
            down_obst == black_value or down_obst == full_camps_value:
           h=+protection_king
        else:
           h=-white_not_protecting
    return h




#################à
#######
#
def kill_opponent(i,j,M,M_tiles,black_value,white_value,castle_value,full_camps_value,empty_camps_value,king_value,kill_opponent=6):
    h=0
    if (j-2) >= 0:
        if M[i, j - 1] == black_value and (
                M[i, j - 2] == white_value or M_tiles[i, j-2] == castle_value or M[i, j-2] == full_camps_value\
                or M[i, j - 2] == empty_camps_value or M_tiles[i, j-2] == castle_value or M[i, j-2] == king_value):
            h += kill_opponent
    if (j+2) < M.shape[1]:
        if M[i, j + 1] == black_value and (
                M[i, j + 2] == white_value or M_tiles[i, j + 2] == castle_value or M[i, j + 2] == full_camps_value \
                or M[i, j + 2] == empty_camps_value or M_tiles[i, j + 2] == castle_value or M[i, j + 2] == king_value):
            h += kill_opponent
    if (i - 2) >= 0:
        if M[i- 1, j] == black_value and (
                M[i- 2, j] == white_value or M_tiles[i- 2, j] == castle_value or M[i- 2, j] == full_camps_value \
                or M[i- 2, j] == empty_camps_value or M_tiles[i- 2, j] == castle_value or M[i- 2, j] == king_value):
            h += kill_opponent
    if (i + 2) < M.shape[0]:
        if M[i+ 1, j ] == black_value and (
                M[i+ 2, j] == white_value or M_tiles[i+ 2, j] == castle_value or M[i+ 2, j] == full_camps_value \
                or M[i+ 2, j] == empty_camps_value or M_tiles[i+ 2, j] == castle_value or M[i + 2, j] == king_value):
            h += kill_opponent
    return h

