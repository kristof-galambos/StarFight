"""running this file starts a game of StarFight"""

#first check whether pygame is installed, and if not, it gets installed
#DELETE THIS PART if you don't want to waste time and you have pygame installed
from pygame_installer2 import install
install()


from gameboard import Gameboard


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

number_of_players = eval(input('Enter number of players (max 4): '))
want_maint = input('Do you want ship maintenance (yes/no)? ')
input_player_names = []
for i in range(number_of_players):
    input_player_names.append(input('Enter the name of player '+str(i+1)+': '))
    

if number_of_players == 2:
    gameboard = Gameboard(['Kristof', 'The Evil Enemy'], [RED, BLUE])
elif number_of_players == 3:
    gameboard = Gameboard(input_player_names, [RED, BLUE, YELLOW])
elif number_of_players == 4:
    gameboard = Gameboard(input_player_names, [RED, BLUE, YELLOW, PURPLE])
else:
    gameboard = Gameboard(input_player_names, [RED, BLUE, YELLOW, PURPLE, CYAN])
    
gameboard.buttons[0].want_maintenance = False
if want_maint == 'yes':
    gameboard.buttons[0].want_maintenance = True
    
#start pygame window:
gameboard.start()

if gameboard.want_to_reload:
    gameboard.buttons[-1].reload_game() #WARNING! only works if the Load_game_button is the last button added!



