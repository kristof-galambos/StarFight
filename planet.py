

import pygame



class Planet(pygame.sprite.Sprite):
    PRINT_WHEN_CLICKED = True
    def __init__(self, name, position, money_income, crystal_income, image_filename):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.position = position
        self.money_income = money_income
        self.crystal_income = crystal_income
        self.image_filename = image_filename
        
        self.has_space_factory = False
        self.selected = False
        self.owner = None #will be set by add_planets_to_players method of gameboard and used by set_owner.colour method
        
        try:
            self.image = pygame.image.load(self.image_filename).convert_alpha()
        except:
            self.image = pygame.image.load(self.image_filename[:-4]+'.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]



    def click(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\planet_click.wav'))
#        YELLOW = (255, 255, 0)
#        width = 100 #self.image_width
#        height = 100 #self.image_height
        if self.selected:
            self.selected = False
            try:
                if self.owner.master.messages[0][0:5] in ['selec']: #remove only specific messages
                    self.owner.master.messages = []
            except:
                pass
            try:
                self.image = pygame.image.load(self.image_filename).convert_alpha()
            except:
                self.image = pygame.image.load(self.image_filename[:-4]+'.png').convert_alpha()
        else:
            if self.PRINT_WHEN_CLICKED:
                print('selected planet: '+self.name+' ('+str(self.money_income)+') owned by '+self.owner.name)
                self.owner.master.messages = ['selected planet: '+self.name+' (producing '+str(self.money_income)+' money', 'per round) owned by '+self.owner.name]
                if self.has_space_factory:
                    self.owner.master.messages.append('Has a space factory! You can build ships here')
            self.selected = True
            try:
                self.image = pygame.image.load(self.image_filename[:-4]+'_selected.jpg').convert_alpha()
            except:
                self.image = pygame.image.load(self.image_filename[:-4]+'_selected.png').convert_alpha()
#            pygame.draw.rect(self.image, YELLOW, [0, 0, width, height])
        self.set_owner_colour()


    def set_owner_colour(self):
        pygame.draw.rect(self.image, self.owner.colour, [0, 0, 10, 10])
        
        
    def draw_space_factory(self):
        GREEN = (0,255,0)
        pygame.draw.rect(self.image, GREEN, [self.owner.master.TILE_SIZE-10, self.owner.master.TILE_SIZE-10, 10, 10])

        
        
