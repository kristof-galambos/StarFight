
from ship import Star_destroyer, Fighter, Transport
import gameboard as g

import pygame


class My_button(pygame.sprite.Sprite):
    def __init__(self, master, ID, position, image_filename):
        pygame.sprite.Sprite.__init__(self)
        self.master = master #this will be a Gameboard instance
        self.ID = ID
        self.position = position
        self.image_filename = image_filename

        self.image = pygame.image.load(self.image_filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]




class New_round_button(My_button):
    SPACE_FACTORY_PRICE = [4000, 10]
    STAR_DESTROYER_BASE_PRICE = 4000
    FIGHTER_BASE_PRICE = 2000
    TRANSPORT_BASE_PRICE = 1000
    maintenance_percentage = 1./8
    price_inflation_percentage = 0.1
    star_destroyer_maintenance = int(STAR_DESTROYER_BASE_PRICE * maintenance_percentage)
    fighter_maintenance = int(FIGHTER_BASE_PRICE * maintenance_percentage)
    transport_maintenance = int(TRANSPORT_BASE_PRICE * maintenance_percentage)
    
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        self.calculate_prices()
        
        
    def command(self):
        self.master.messages = ['NEW ROUND!']
        print('\nNEW ROUND!')
        self.calculate_prices()
        print('\nPRICES:')
        self.master.messages.append('PRICES: ')
        print('STAR DESTROYER:', self.price_star_destroyer)
        self.master.messages.append('STAR DESTROYER: ' + str(self.price_star_destroyer))
        print('FIGHTER:', self.price_fighter)
        self.master.messages.append('FIGHTER: ' + str(self.price_fighter))
        print('TRANSPORT:', self.price_transport)
        self.master.messages.append('TRANSPORT: ' + str(self.price_transport))
        print('SPACE FACTORY:', self.SPACE_FACTORY_PRICE[0], 'money, ', self.SPACE_FACTORY_PRICE[1], 'crystals')
        self.master.messages.append('SPACE FACTORY: ' + str(self.SPACE_FACTORY_PRICE[0]) + 'money,' + str(self.SPACE_FACTORY_PRICE[1]) + 'crystals')
        self.master.messages.append('PLAYERS:')
        for player in self.master.players:
            player.update_total_income()
            player.add_total_income()
            if self.want_maintenance:
                player.subtract_maintenance()
            print('\n'+player.name)
            self.master.messages.append(player.name)
            print('money:', player.money)
            print('crystals:', player.crystals)
            self.master.messages.append('money: ' + str(player.money) + ', crystals: ' + str(player.crystals))
            print('money income:', player.money_income)
            print('crystal income:', player.crystal_income)
            if self.want_maintenance:
                player.print_maintenance()
            print('controlled planets:', len(player.planets))
            print('ships:', len(player.ships))
            for ship in player.ships:
                ship.already_travelled = False
            
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\button_click.wav'))
        
        
    def calculate_prices(self):
        star_destroyers_no = 0
        fighters_no = 0
        transports_no = 0
        for player in self.master.players:
            for ship in player.ships:
                if ship.ship_type == 'star destroyer':
                    star_destroyers_no +=1
                elif ship.ship_type == 'fighter':
                    fighters_no +=1
                elif ship.ship_type == 'transport':
                    transports_no +=1
                else:
                    print('Unknown ship type in calculate_prices method of New_round_button!!!')
        self.price_star_destroyer = int(self.STAR_DESTROYER_BASE_PRICE*(1+star_destroyers_no * self.price_inflation_percentage))
        self.price_fighter = int(self.FIGHTER_BASE_PRICE*(1+fighters_no * self.price_inflation_percentage))
        self.price_transport = int(self.TRANSPORT_BASE_PRICE*(1+transports_no * self.price_inflation_percentage))
                    
                
                

class Build_space_factory_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        where_to_buy = None
        who_buys = None
        many_planets_selected = False #we won't allow that to happen!
        
        for player in self.master.players:
            if many_planets_selected:
                break
            for planet in player.planets:
                if many_planets_selected:
                    break
                if planet.selected:
                    if where_to_buy != None:
                        many_planets_selected = True
                        break
                    else:
                        where_to_buy = planet
                        who_buys = player
        if many_planets_selected:
            print('\nMany planets selected! Please press this button again with only one planet selected!')
            self.master.messages = ['Many planets selected! Please press this button again with only one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
        if where_to_buy == None:
            print('\nNo planets selected! Please press this button again with one planet selected!')
            self.master.messages = ['No planets selected! Please press this button again with one planet selected!']
            return
            
        who_buys.build_space_factory(where_to_buy)
        where_to_buy.click()
        
       
        
        
class Buy_star_destroyer_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        where_to_buy = None
        who_buys = None
        many_planets_selected = False #we won't allow that to happen!
        
        for player in self.master.players:
            if many_planets_selected:
                break
            for planet in player.planets:
                if many_planets_selected:
                    break
                if planet.selected:
                    if where_to_buy != None:
                        many_planets_selected = True
                        break
                    else:
                        where_to_buy = planet
                        who_buys = player
        if many_planets_selected:
            print('\nMany planets selected! Please press this button again with only one planet selected!')
            self.master.messages = ['Many planets selected! Please press this button again with only one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
        if where_to_buy == None:
            print('\nNo planets selected! Please press this button again with one planet selected!')
            self.master.messages = ['No planets selected! Please press this button again with one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        if not where_to_buy.has_space_factory:
            print('\nYou need to build a space factory first!')
            self.master.messages = ['You need to build a space factory first!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        who_buys.buy_star_destroyer(where_to_buy)
        where_to_buy.click()
    
        
        
        
class Buy_fighter_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        where_to_buy = None
        who_buys = None
        many_planets_selected = False #we won't allow that to happen!
        
        for player in self.master.players:
            if many_planets_selected:
                break
            for planet in player.planets:
                if many_planets_selected:
                    break
                if planet.selected:
                    if where_to_buy != None:
                        many_planets_selected = True
                        break
                    else:
                        where_to_buy = planet
                        who_buys = player
        if many_planets_selected:
            print('\nMany planets selected! Please press this button again with only one planet selected!')
            self.master.messages = ['Many planets selected! Please press this button again with only one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
        if where_to_buy == None:
            print('\nNo planets selected! Please press this button again with one planet selected!')
            self.master.messages = ['No planets selected! Please press this button again with one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        if not where_to_buy.has_space_factory:
            print('\nYou need to build a space factory first!')
            self.master.messages = ['You need to build a space factory first!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        who_buys.buy_fighter(where_to_buy)
        where_to_buy.click()
        
        
        
        
class Buy_transport_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        where_to_buy = None
        who_buys = None
        many_planets_selected = False #we won't allow that to happen!
        
        for player in self.master.players:
            if many_planets_selected:
                break
            for planet in player.planets:
                if many_planets_selected:
                    break
                if planet.selected:
                    if where_to_buy != None:
                        many_planets_selected = True
                        break
                    else:
                        where_to_buy = planet
                        who_buys = player
        if many_planets_selected:
            print('\nMany planets selected! Please press this button again with only one planet selected!')
            self.master.messages = ['Many planets selected! Please press this button again with only one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
        if where_to_buy == None:
            print('\nNo planets selected! Please press this button again with one planet selected!')
            self.master.messages = ['No planets selected! Please press this button again with one planet selected!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        if not where_to_buy.has_space_factory:
            print('\nYou need to build a space factory first!')
            self.master.messages = ['You need to build a space factory first!']
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            return
            
        who_buys.buy_transport(where_to_buy)
        where_to_buy.click()
                
                
                

class Save_and_quit_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        f = open('savegame.txt', 'w')
        f.write('Number of players: '+str(len(self.master.players)))
        f.write('\nMaintenance: '+str(self.master.buttons[0].want_maintenance))
        for player in self.master.players:
            f.write('\n\nplayer: '+player.name)
            f.write('\nmoney: '+str(player.money))
            f.write('\ncrystals: '+str(player.crystals))
        f.write('\n\n\nAll planets:')
        for player in self.master.players:
            for planet in player.planets:
                f.write('\n\nplanet: '+planet.name)
                f.write('\np_owner_name: '+planet.owner.name)
                f.write('\nspace_factory: '+str(planet.has_space_factory))
        f.write('\n\n\nAll ships:')
        for player in self.master.players:
            for ship in player.ships:
                f.write('\n\nship: '+ship.ship_type)
                f.write('\ns_owner_name: '+ship.owner.name)
                f.write('\nposition: '+str(ship.position[0]/self.master.TILE_SIZE)+' '+str(ship.position[1]/self.master.TILE_SIZE))
                f.write('\nalready_travelled: '+str(ship.already_travelled))
        f.close()
        
        self.master.want_to_keep_playing = False
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\button_click.wav'))
        
        
        
        
class Load_game_button(My_button):
    def __init__(self, master, ID, position, image_filename):
        My_button.__init__(self, master, ID, position, image_filename)
        
    def command(self):
        f = open('savegame.txt', 'r')
        content = f.read().split('\n')
        
        self.saved_number_of_players = content[0][-1]
        self.saved_names = []
        self.saved_moneys = []
        self.saved_crystals = []
        self.saved_planet_names = []
        self.saved_planet_owner_names = []
        self.saved_planet_has_space_factories = []
        self.saved_ships = []
        self.saved_ship_owner_names = []
        self.saved_ship_positions = []
        self.saved_ship_already_travelled = []
        for i,linestring in enumerate(content):
            line = linestring.split(' ')
            if line[0]=='Maintenance:':
                self.saved_want_maintenance = self.str_to_bool(line[-1])
            if line[0]=='player:':
                self.saved_names.append(line[-1])
            elif line[0]=='money:':
                self.saved_moneys.append(int(line[-1]))
            elif line[0]=='crystals:':
                self.saved_crystals.append(int(line[-1]))
            elif line[0]=='planet:':
                self.saved_planet_names.append(' '.join(line[1:]))
            elif line[0]=='p_owner_name:':
                self.saved_planet_owner_names.append(line[-1])
            elif line[0]=='space_factory:':
                self.saved_planet_has_space_factories.append(self.str_to_bool(line[-1]))
            elif line[0]=='ship:':
                self.saved_ships.append(' '.join(line[1:]))
            elif line[0]=='s_owner_name:':
                self.saved_ship_owner_names.append(line[-1])
            elif line[0]=='position:':
                self.saved_ship_positions.append([int(x) for x in line[1:]])
            elif line[0]=='already_travelled:':
                self.saved_ship_already_travelled.append(self.str_to_bool(line[-1]))
#            else:
#                print 'logic error in Load game button command method!!!'
        f.close()
        
        self.master.want_to_keep_playing = False
        self.master.want_to_reload = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\button_click.wav'))
        
        
    def reload_game(self):
        
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        PURPLE = (255, 0, 255)
        CYAN = (0, 255, 255)

        #create gameboard with player names
        if self.saved_number_of_players == 2:
            gameboard = g.Gameboard(['Kristof', 'The Ugly Enemy'], [RED, BLUE])
            self.master = gameboard
        elif self.saved_number_of_players == 3:
            gameboard = g.Gameboard(self.saved_names, [RED, BLUE, YELLOW])
            self.master = gameboard
        elif self.saved_number_of_players == 4:
            gameboard = g.Gameboard(self.saved_names, [RED, BLUE, YELLOW, PURPLE])
            self.master = gameboard
        else:
            gameboard = g.Gameboard(self.saved_names, [RED, BLUE, YELLOW, PURPLE, CYAN])
            self.master = gameboard
            
        #adjust want_maintenance
        self.want_maintenance = False
        if self.saved_want_maintenance:
            self.master.buttons[0].want_maintenance = True

        #adjust moneys and crystals
        for i in range(len(self.saved_moneys)):
            gameboard.players[i].money = int(self.saved_moneys[i])
            gameboard.players[i].crystals = int(self.saved_crystals[i])
    
        #add planets to players - without initially removing evenly allocated planets from players
        for i in range(len(self.saved_planet_names)):
#            print '\n'+self.saved_planet_names[i]
#            print 'looking for owner name:', self.saved_planet_owner_names[i]
            for player in self.master.players:
                if self.saved_planet_owner_names[i]==player.name:
#                    print 'found owner:', player.name
                    k = 0
                    for j in range(len(self.master.planets)):
                        if self.master.planets[j-k].name==self.saved_planet_names[i]:
                            planet_to_be_added = self.master.planets[j-k]
#                            print 'found in self.master.planets:', self.master.planets[j-k].name
                            for other_player in self.master.players:
                                if self.master.planets[j-k] in other_player.planets:
                                    other_player.planets.remove(self.master.planets[j-k])
                                    k +=1
                            player.planets.append(planet_to_be_added)
#                            print 'planet', planet_to_be_added.name, 'added to player', player.name
                            
                            player.planets[-1].owner = player
                            player.planets[-1].set_owner_colour()
                            if self.saved_planet_has_space_factories[i]:
                                player.planets[-1].has_space_factory = True
                            break
                    break
                
        #add ships to players
        for i in range(len(self.saved_ships)):
            for player in self.master.players:
                if self.saved_ship_owner_names[i] == player.name:
                    if self.saved_ships[i] == 'star destroyer':
                        self.master.add_ship_to_player(Star_destroyer([self.master.TILE_SIZE*x for x in self.saved_ship_positions[i]], player), player)
                    elif self.saved_ships[i] == 'fighter':
                        self.master.add_ship_to_player(Fighter([self.master.TILE_SIZE*x for x in self.saved_ship_positions[i]], player), player)
                    elif self.saved_ships[i] == 'transport':
                        self.master.add_ship_to_player(Transport([self.master.TILE_SIZE*x for x in self.saved_ship_positions[i]], player), player)
                    else:
                        raise Exception('unknown ship type in reload_game method')
                    if self.saved_ship_already_travelled[i]:
                        player.ships[-1].already_travelled = True
                    break
        
        gameboard.start()
        
        
    def str_to_bool(self, s):
        if s == 'True':
             return True
        elif s == 'False':
             return False
        else:
             raise ValueError('Cannot covert {} to bool'.format(s))
        
             
             
        