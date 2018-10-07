"""running this file starts a game of StarFight and loads in savegame.txt"""

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


#initialize a gameboard with some random input and load in the savegame.txt straight away
gameboard = Gameboard(['Kristof', 'The Evil Enemy'], [RED, BLUE])
gameboard.buttons[0].want_maintenance = False
gameboard.buttons[-1].command()
#start pygame window:
#gameboard.start()
gameboard.buttons[-1].reload_game()

