import main_black as b
import main_white as w

player=input('White or Black? ')
T=input('Set the timeout time in seconds ')
server=input('server IP address ')
if player=='White':
    w.main_white(T,server)
elif player=='Black':
    b.main_black(T,server)
else:
    raise Exception('player not correct; please write White or Black')