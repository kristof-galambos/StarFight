

from ship import Star_destroyer, Fighter, Transport

import pygame


class Player():
    def __init__(self, name, colour, master):
        self.name = name
        self.colour = colour
        self.master = master #will be a Gameboard instance
        self.planets = []
        self.ships = []
        self.money = 0
        self.crystals = 0
        self.money_income = 0
        self.crystal_income = 0
        
    
    def update_total_income(self):
        money_income = 0
        crystal_income = 0
        for planet in self.planets:
            money_income += planet.money_income
            crystal_income += planet.crystal_income
        self.money_income = money_income
        self.crystal_income = crystal_income
    
    
    def add_total_income(self):
        self.money += self.money_income
        self.crystals += self.crystal_income
        
        
    def subtract_maintenance(self):
        """uses maintenance prices from New_round_button in buttons.py
        subtracts from self.money, called by New_round_button"""
        maintenance_cost = 0
        for ship in self.ships:
            if ship.ship_type == 'star destroyer':
                maintenance_cost += self.master.buttons[0].star_destroyer_maintenance
            elif ship.ship_type == 'fighter':
                maintenance_cost += self.master.buttons[0].fighter_maintenance
            elif ship.ship_type == 'transport':
                maintenance_cost += self.master.buttons[0].transport_maintenance
        self.money -= maintenance_cost

        
    def print_maintenance(self):
        """uses maintenance prices from New_round_button in buttons.py
        prints mainteneance, called by New_round_button"""
        maintenance_cost = 0
        for ship in self.ships:
            if ship.ship_type == 'star destroyer':
                maintenance_cost += self.master.buttons[0].star_destroyer_maintenance
            elif ship.ship_type == 'fighter':
                maintenance_cost += self.master.buttons[0].fighter_maintenance
            elif ship.ship_type == 'transport':
                maintenance_cost += self.master.buttons[0].transport_maintenance
        print('ship maintenance:', maintenance_cost)
        

    def build_space_factory(self, planet):
        if not planet.has_space_factory:
            success = self.decrease_funds(self.master.buttons[0].SPACE_FACTORY_PRICE[0], self.master.buttons[0].SPACE_FACTORY_PRICE[1])
            if success:
                planet.has_space_factory = True
                print('\n', self.name, 'has built a space factory on '+planet.name+'!')
                print('remaining:', '\nmoney:', self.money, '\ncrystals:', self.crystals)
            else:
                print('\n', self.name, 'has insufficient funds to build a space factory on '+planet.name+'!')
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
        else:
            print('\n'+self.name, 'already has a space factory on', planet.name+'!')
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
    
            
    def buy_star_destroyer(self, planet):
        success = self.decrease_funds(self.master.buttons[0].price_star_destroyer, 0)
        if success:
            new_ship = Star_destroyer([planet.position[0], planet.position[1]], self)
            self.master.add_ship_to_player(new_ship, self)
            print('\n', self.name, 'has bought a star destroyer on '+planet.name+'!')
            print('remaining:' '\nmoney:', self.money, '\ncrystals:', self.crystals)
        else:
            print('\n', self.name, 'has insufficient funds to buy a star destroyer on '+planet.name+'!')
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
    

    def buy_fighter(self, planet):
        success = self.decrease_funds(self.master.buttons[0].price_fighter, 0)
        if success:
            new_ship = Fighter([planet.position[0], planet.position[1]], self)
            self.master.add_ship_to_player(new_ship, self)
            print('\n', self.name, 'has bought a fighter on '+planet.name+'!')
            print('remaining:' '\nmoney:', self.money, '\ncrystals:', self.crystals)
        else:
            print('\n', self.name, 'has insufficient funds to buy a fighter on '+planet.name+'!')
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
    
        
    def buy_transport(self, planet):
        success = self.decrease_funds(self.master.buttons[0].price_transport, 0)
        if success:
            new_ship = Transport([planet.position[0], planet.position[1]], self)
            self.master.add_ship_to_player(new_ship, self)
            print('\n', self.name, 'has bought a transport on '+planet.name+'!')
            print('remaining:' '\nmoney:', self.money, '\ncrystals:', self.crystals)
        else:
            print('\n', self.name, 'has insufficient funds to buy a transport on '+planet.name+'!')
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
    
            
    def decrease_funds(self, sub_money, sub_crystals):
        if self.money - sub_money >= 0 and self.crystals - sub_crystals >= 0:
            self.money -= sub_money
            self.crystals -= sub_crystals
            return True #True stands for success
        else:
            return False #False stands for insufficient money
        
        
        

