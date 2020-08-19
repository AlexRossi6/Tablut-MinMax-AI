import numpy as np
def conv_matrix(M_white_conv):

    #print('Matrix to convert:\n',M_white_conv)
    M_black_conv=np.zeros((9,9),dtype='object')

    for i in range(9):
        for j in range(9):
            if M_white_conv[i,j]==1:
                M_black_conv[i,j]='B'
            if M_white_conv[i,j]==10:
                M_black_conv[i,j]='W'
            if M_white_conv[i,j]==8:
                M_black_conv[i,j]='K'
            if M_white_conv[i,j]==0:
                M_black_conv[i,j]=0

    #print('Matrix coverted black:\n', M_black_conv)



    return M_black_conv