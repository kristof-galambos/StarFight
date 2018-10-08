
import pygame



class Ship(pygame.sprite.Sprite):
    def __init__(self, ship_type, image_filename, owner, position):
        pygame.sprite.Sprite.__init__(self)
        self.ship_type = ship_type
        self.image_filename = image_filename
        
        self.owner = owner
        self.position = position
        self.selected = False
        self.already_travelled = False
        self.slightly_down = 0 #how much has it travelled slightly down to get out of the way of other planets/ships?
        

        self.image = pygame.image.load(self.image_filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]


    def travel_left(self):
        self.position[0] -= self.owner.master.TILE_SIZE
        self.rect.x -= self.owner.master.TILE_SIZE
        self.click()
        self.already_travelled = True
    def travel_right(self):
        self.position[0] += self.owner.master.TILE_SIZE
        self.rect.x += self.owner.master.TILE_SIZE
        self.click()
        self.already_travelled = True
    def travel_up(self):
        self.position[1] -= self.owner.master.TILE_SIZE
        self.rect.y -= self.owner.master.TILE_SIZE
        self.click()
        self.already_travelled = True
    def travel_down(self):
        self.position[1] += self.owner.master.TILE_SIZE
        self.rect.y += self.owner.master.TILE_SIZE
        self.click()
        self.already_travelled = True
        
    def travel_slightly_down(self):
        self.position[1] += self.owner.master.TILE_SIZE/4
        self.rect.y += self.owner.master.TILE_SIZE/4
        self.slightly_down +=1
    def travel_slightly_up(self):
        self.position[1] -= self.owner.master.TILE_SIZE/4
        self.rect.y -= self.owner.master.TILE_SIZE/4
        self.slightly_down -=1
    
    
    def click(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\ship_click.wav'))
#        YELLOW = (255, 255, 0)
#        width = 100 #self.image_width
#        height = 100 #self.image_height
        if self.selected:
            self.selected = False
            try:
                if self.owner.master.messages[0][0:5] in ['use t', 'The s']: #remove only specific messages
                    self.owner.master.messages = []
            except:
                pass
            self.image = pygame.image.load(self.image_filename).convert_alpha()
        else:
            self.selected = True
            self.owner.master.messages = ['use the up, down, left and right arrow keys', 'to move your ship', 'or click again to deselect']
            try:
                self.image = pygame.image.load(self.image_filename[:-4]+'_selected.jpg').convert_alpha()
            except:
                self.image = pygame.image.load(self.image_filename[:-4]+'_selected.png').convert_alpha()
#            pygame.draw.rect(self.image, YELLOW, [0, 0, width, height])
        self.set_owner_colour()


    def set_owner_colour(self):
        pygame.draw.rect(self.image, self.owner.colour, [0, 0, 10, 10])



class Star_destroyer(Ship):
    def __init__(self, position, owner):
        Ship.__init__(self, 'star destroyer', 'images\\battleship_final.jpg', owner, position)
        
        
class Fighter(Ship):
    def __init__(self, position, owner):
        Ship.__init__(self, 'fighter', 'images\\fighter_final.jpg', owner, position)
        
        
class Transport(Ship):
    def __init__(self, position, owner):
        Ship.__init__(self, 'transport', 'images\\transport_final.jpg', owner, position)
        
        
        
        