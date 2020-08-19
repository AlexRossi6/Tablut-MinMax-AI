import functions_black as bl
import copy


def utility( state, start, r, c, illegal_moves, black_win = 1000, black_loose = 1000,black_checker_death=5,white_checker_death=4,strategic_position=3,move_strategic_position=2,black_near_king=4):


    #r and c are the indexes of the action



        k_ind=[]

        for i in range(9):
            for j in range(9):

                if state[i][j]=='K':
                    k_ind=[i,j]
                    break
        '''board used to check the camps'''
        board=copy.deepcopy(state)
        for i in range(9):
            for j in range(9):
                if [i, j] in illegal_moves:
                    board[i][j]=1
        h=0

        '''if king is in the throne return 1 if it is surrounded by 4 black checkers'''
        if k_ind == [4, 4] and state[4][3] == 'B' and state[4][5] == 'B' and state[3][4] == 'B' and state[5][4] == 'B':


            return black_win
        #'''if king is outside the throne and it is surrounded by two black checkers (or by one if king adjacent to a camp) return 1'''
        if k_ind not in [[4,3],[4,5],[3,4],[5,4],[4,4]] and [k_ind[0]+1,k_ind[1]]==[r,c] and (state[k_ind[0] - 1][k_ind[1]] == 'B' or k_ind in [[1,3], [2,4], [1,5], [5,1], [5, 7]]):
            return black_win
        elif k_ind not in [[4,3],[4,5],[3,4],[5,4],[4,4]] and [k_ind[0]-1,k_ind[1]]==[r,c] and (state[k_ind[0]+1][k_ind[1]]=='B' or k_ind in [[3,1],[7,3],[6,4],[7,5],[3,7]]):
            return black_win
        elif k_ind not in [[4,3],[4,5],[3,4],[5,4],[4,4]] and [k_ind[0],k_ind[1]-1]==[r,c] and (state[k_ind[0]][k_ind[1]+1] =='B' or k_ind in [[1,3],[3,7],[4,6],[5,7],[7,3]]):
            return black_win
        elif k_ind not in [[4,3],[4,5],[3,4],[5,4],[4,4]] and [k_ind[0],k_ind[1]+1]==[r,c] and (state[k_ind[0]][k_ind[1]-1]=='B' or k_ind in [[1,5],[3,1],[4,2],[5,1],[7,5]]):
            return black_win
        elif bl.king_3(state,k_ind):
            return black_win



        elif board[k_ind[0]][0:k_ind[1]] == [0 for i in range(0, k_ind[1])] or board[k_ind[0]][(k_ind[1]+1):9] == [0 for i in range((k_ind[1]+1), 9)] or [board[i][k_ind[1]] for i in range(0,k_ind[0])]==[0 for i in range(0,k_ind[0])] or [board[i][k_ind[1]] for i in range(k_ind[0]+1,9)]==[0 for i in range(k_ind[0]+1,9)]:

            h += -1500



        state_2 = copy.deepcopy(state)
        if bl.white_checker_death(state, r, c, illegal_moves):

            h += white_checker_death
            state_2=bl.apply_whitedeath(state_2,r,c)

        if bl.king_win_2(state_2,k_ind,illegal_moves):
            h += -black_loose

        if bl.black_checker_death(state_2, illegal_moves):

            h += -black_checker_death




        if start not in [[2,2],[6,6],[2,6],[6,2]] and [r,c] in [[2,2],[6,6],[2,6],[6,2]]:
            h+= strategic_position
        if start in [[2,2],[6,6],[2,6],[6,2]] and [r,c] not in [[2,2],[6,6],[2,6],[6,2]]:
            h+= -move_strategic_position
        if k_ind in [[r+1,c],[r,c+1],[r-1,c],[r,c-1]] and not bl.black_checker_death(state_2, illegal_moves):
            h+= black_near_king



        return h



