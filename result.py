from useful_functions import apply_action

def result(M,M_converted,king_indexes,black_value,white_value,castle_value,empty_camps_value,full_camps_value,king_value,move,turn):

    #print('M before action:\n',M)
    #print('M_converted before action:\n',M_converted)
    M,M_converted = apply_action(M, M_converted, move)
    #print('M after action:\n', M)
    #print('M_converted after action:\n', M_converted)


    dim1,dim2=M.shape
    # the killing it's necessary active, so I have to check only the neighbourhood of the last checker moved:
    moved_i,moved_j= move[1]
    left_ok=False
    right_ok=False
    up_ok=False
    down_ok=False


    if moved_j-2>=0:
         li,lj=moved_i, moved_j - 1
         l_neig = M[li, lj-1]  # left neig of the left neigh
         left_ok=True

    if moved_j+2<dim2:
        ri,rj=moved_i, moved_j + 1
        r_neig = M[ri, rj+1]
        right_ok=True

    if moved_i-2>=0:
        ui,uj=moved_i - 1, moved_j
        u_neig = M[ui- 1, uj ]
        up_ok=True

    if moved_i+2<dim1:
       di,dj=moved_i + 1, moved_j
       d_neig = M[di+ 1, dj ]
       down_ok=True





    #check if king is closed to the castle:
    ik = king_indexes[0][0]
    jk = king_indexes[0][1]
    if [ik,jk]==[3,4] or [ik,jk]==[5,4] or [ik,jk]==[4,3] or [ik,jk]==[4,5]:
        king_close_castle = True
    else:
        king_close_castle = False

    #sum of the neighbourhood of the king:
    sum_neig_k = sum_neig(M,ik, jk,dim1,dim2)


    if turn == 'WHITE':
            if left_ok:
                M,M_converted=check_neig(M, M_converted, li, lj, l_neig, black_value, white_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
            if right_ok:
                M,M_converted=check_neig(M, M_converted, ri, rj, r_neig, black_value, white_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
            if up_ok:
                M,M_converted=check_neig(M, M_converted, ui, uj, u_neig, black_value, white_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
            if down_ok:
                M,M_converted=check_neig(M, M_converted, di, dj, d_neig, black_value, white_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)

    if turn == 'BLACK':
        if left_ok and (l_neig==white_value or (l_neig==king_value and (not(king_close_castle)))):
            M,M_converted=check_neig(M, M_converted, li, lj, l_neig, white_value, black_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
        if right_ok and (r_neig==white_value or (r_neig==king_value and (not(king_close_castle)))):
            M,M_converted=check_neig(M, M_converted, ri, rj, r_neig, white_value, black_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
        if up_ok and(u_neig==white_value or (u_neig==king_value and (not(king_close_castle)))):
            M,M_converted=check_neig(M, M_converted, ui, uj, u_neig, white_value, black_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)
        if down_ok and (d_neig==white_value or (d_neig==king_value and (not(king_close_castle)))):
            M,M_converted=check_neig(M, M_converted, di, dj, d_neig, white_value, black_value, castle_value, empty_camps_value,
                       full_camps_value,king_value)

        if left_ok and(l_neig==king_value and king_close_castle):
            if  (black_value*3+white_value) >= sum_neig_k >=black_value*3:
                M[li, lj] -= M_converted[li, lj]
                M_converted[li, lj]=0

        if right_ok and (r_neig==king_value and king_close_castle):
            if  (black_value*3+white_value) >= sum_neig_k >=black_value*3:
                M[ri, rj] -= M_converted[ri, rj]
                M_converted[ri, rj]=0

        if up_ok and (u_neig==king_value and king_close_castle):
            if  (black_value*3+white_value) >= sum_neig_k >=black_value*3:
                M[ui, uj] -= M_converted[ui, uj]
                M_converted[ui, uj] = 0

        if down_ok and (d_neig==king_value and king_close_castle):
            if  (black_value*3+white_value) >= sum_neig_k >=black_value*3:
                M[di, dj] -= M_converted[di, dj]
                M_converted[di, dj] = 0


        if left_ok and (l_neig==castle_value+king_value and sum_neig_k==black_value*4):
            M[li, lj] -= M_converted[li, lj]
            M_converted[li, lj] = 0

        if right_ok and (r_neig==castle_value+king_value and sum_neig_k==black_value*4):
            M[ri, rj] -= M_converted[ri, rj]
            M_converted[ri, rj] = 0

        if up_ok and (u_neig==castle_value+king_value and sum_neig_k==black_value*4):
            M[ui, uj] -= M_converted[ui, uj]
            M_converted[ui, uj] = 0

        if down_ok and (d_neig==castle_value+king_value and sum_neig_k==black_value*4):
            M[di, dj] -= M_converted[di, dj]
            M_converted[di, dj] = 0

   # print('M after eliminating killed action:\n', M)
    #print('M_converted after eliminating killed action:\n', M_converted)
    return M,M_converted













def check_neig(M,M_converted,xi,xj,x_neig,opposite_value,mate_value,castle_value,empty_camps_value,full_camps_value,king_value):
        if M[xi, xj] == opposite_value and (x_neig == mate_value or x_neig == castle_value or x_neig==(castle_value + king_value) or x_neig==full_camps_value or
            x_neig==empty_camps_value):
            M[xi,xj] -= M_converted[xi,xj]
            M_converted[xi, xj] = 0
        return M,M_converted




def sum_neig(M,i,j,dim1,dim2):
    s=0
    if i-1>=0:
        s+=M[i-1,j]
    if i+1<dim2:
        s+=M[i+1,j]
    if j-1>=0:
        s+=M[i,j-1]
    if j+1<dim1:
        s+=M[i,j+1]
    return s