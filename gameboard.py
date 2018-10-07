
from planet import Planet
from player import Player
from buttons import New_round_button, Build_space_factory_button, Buy_star_destroyer_button, Buy_fighter_button, Buy_transport_button, Save_and_quit_button, Load_game_button

import pygame
import openpyxl
import numpy.random as npr


class Gameboard():
    FULL_SCREEN_MODE = False
    def __init__(self, player_names, player_colours):
        self.initialise_pygame()
        
        self.background_image = 'images\\gameboard_background2_final.jpg'
        self.planets = [] #planets stored here and in Player as well
        self.players = []
        self.TILE_SIZE = 70
        for i in range(len(player_names)):
            self.players.append(Player(player_names[i], player_colours[i], self))
        self.buttons = []
        self.messages = ['Game started!', 'brief output info will appear here', 'more details will be printed to the console']

        self.attacker = None
        self.defender = None
        self.want_to_keep_playing = True
        self.songs = None
        self.want_music = True
        self.SONG_END = None
        self.songs = ['music\\my_kingdom.mp3', 'music\\my_kingdom.mp3', 'music\\my_kingdom.mp3', 'music\\l_autunno.mp3', 'music\\main_theme.mp3', 'music\\for_honour_and_glory.mp3', \
                      'music\\main_theme.mp3', 'music\\kings_court.mp3', 'music\\the_stage_is_set.mp3', 'music\\ride_forth_victoriously.mp3', 'music\\ride_forth_victoriously.mp3', \
                      'music\\Two_Steps_From_Hell_Star_Sky.mp3', 'music\\Two_Steps_From_Hell_United_We_Stand_Divided_We_Fall.mp3', \
                      'music\\Two_Steps_from_Hell_Heart_Of_Courage.mp3'] # 'music\\piano_concerto_no_1000.mp3', 'music\\grat_fader_berg.mp3', 'music\\Two_Steps_From_Hell_Victory.mp3', 'music\\Two_Steps_From_Hell_Blackheart.mp3', 'music\\Two_Steps_From_Hell_Merchant_Prince_Reprised_Version_.mp3'
        self.want_to_reload = False #used by load game button
        
        self.initialise_planets()
        self.initialise_buttons()

        
    def initialise_pygame(self):
        pygame.init()
        WIDTH = 1350
        HEIGHT = 700
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Fight for the galaxy! ;-)')
        self.clock = pygame.time.Clock()
        self.all_sprites_list1 = pygame.sprite.Group()
        self.all_ship_sprites = pygame.sprite.Group()
        
        
    def initialise_planets(self):
        #read in planets
        self.read_in_planets()
        #add stuff to the players
        for i, planet in enumerate(self.planets):
            self.add_planet_to_player(planet, self.players[i%len(self.players)])

        
    def read_in_planets(self):
        """reads in the planets from an excel file named planets_in.xlsx
        stores the planets in self.planets"""
        book = openpyxl.load_workbook('planets_in.xlsx')
        sheet = book.active
        names = []
        positions = []
        money_incomes = []
        crystal_incomes = []
        image_filenames = []
        for row in sheet.iter_rows('B4:G37'):
            if row[0].value==None or row[0].value=='':
                break
            names.append(row[0].value)
            positions.append([row[1].value*self.TILE_SIZE, row[2].value*self.TILE_SIZE])
            money_incomes.append(row[3].value)
            crystal_incomes.append(row[4].value)
            image_filenames.append(row[5].value)
        for i in range(len(names)):
            self.planets.append(Planet(names[i], positions[i], money_incomes[i], crystal_incomes[i], image_filenames[i]))
            
            
    def add_planet_to_player(self, planet, player):
        """in the beginning of the game, allocates the planets from self.planets to the players"""
        if planet in self.planets and planet not in player.planets:
            player.planets.append(planet)
            planet.owner = player
            planet.set_owner_colour()
            
    
    def add_ship_to_player(self, ship, player):
        """used by the buy_star_destroyer, etc. methods of player"""
        player.ships.append(ship)
        ship.set_owner_colour()
        self.all_ship_sprites.add(ship)
        
        
    def ship_moved_check_collisions(self, ship):
        """called by the event_handling every time just after a ship moves
        calls who_did_the_ship_meet to get its return info. in the case of enemy objects meeting, sets attacker and defenders attributes and sets want_to_quit_pygame True"""
        while ship.slightly_down>0:
            ship.travel_slightly_up()   
        met_enemy, met_friend = self.who_did_the_ship_meet(ship.position, ship)
        want_to_move_slightly_down = False
        if met_enemy != None:
#            print '\nMet enemy!'
            print('\nBeginning battle!')
            
            same_type = False
            try:
                if ship.ship_type == met_enemy.ship_type:
                    same_type = True
            except:
                pass
            
            if same_type:
                randomNumber = npr.randint(2)
                attackSuccessful = False
                if randomNumber == 0:
                    attackSuccessful = True
                if attackSuccessful:
                    met_enemy.owner.ships.remove(met_enemy)
                    print('\nAttacker won! Defender ship destroyed.')
                    met_enemy.kill()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
                else:
                    ship.owner.ships.remove(ship)
                    print('\nDefender won! Attacker ship destroyed.')
                    ship.kill()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
            else:
                if isinstance(met_enemy, Planet):
                    ship.owner.planets.append(met_enemy)
                    met_enemy.owner.planets.remove(met_enemy)
                    met_enemy.owner = ship.owner
                    met_enemy.set_owner_colour()
                    print('\nAttacking ship captured planet!')    
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\captured.wav'))              
                elif ship.ship_type == 'star destroyer':
                    met_enemy.owner.ships.remove(met_enemy) #destroy enemy ship
                    print('\nThe attacking star destroyer destroyed the defending ship!')
                    met_enemy.kill()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
                elif ship.ship_type == 'fighter':
                    if met_enemy.ship_type == 'transport':
                        met_enemy.owner.ships.remove(met_enemy)
                        print('\nThe attacking fighter destroyed the defending transport!')
                        met_enemy.kill()
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
                    elif met_enemy.ship_type == 'star destroyer':
                        ship.owner.ships.remove(ship)
                        print('\nThe defending star destroyer destroyed the attacking fighter!')
                        ship.kill()
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
                    else:
                        print('logic error!!!')
                elif ship.ship_type == 'transport':
                    ship.owner.ships.remove(ship)
                    print('\nThe defending ship destroyed the attacking transport!')
                    ship.kill()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\explosion.wav'))
                else:
                    print('logic error 2!!!')
                        
        if met_friend != None:
#            print '\nMet friend!'
            if not isinstance(met_friend, Planet):
                want_to_move_slightly_down = True
        if want_to_move_slightly_down:
            ship.travel_slightly_down()
                
        
    def who_did_the_ship_meet(self, new_pos, the_ship):
        """arguments: the ship that moved, the new_pos where it moved
        returns: enemy object met and friendly object met"""
        met_enemy = None
        met_friend = None
        for player in self.players:
            for planet in player.planets:
                if planet.position == new_pos:
                    if player is the_ship.owner:
                        met_friend = planet
                    else:
                        met_enemy = planet
            for ship in player.ships:
                if ship.position == new_pos:
                    if ship.owner is the_ship.owner:
                        if not ship is the_ship:
                            met_friend = ship
                    else:
                        met_enemy = ship
        return met_enemy, met_friend
        
        
    def initialise_buttons(self):
        """called in the init method"""
        if self.FULL_SCREEN_MODE:
            new_round_button = New_round_button(self, 1, [1130, 10], 'images\\new_round_button_final.jpg')
            build_space_factory_button = Build_space_factory_button(self, 2, [1130, 60], 'images\\build_space_factory_button_final.jpg')
            buy_star_destroyer_button = Buy_star_destroyer_button(self, 3, [1130, 110], 'images\\buy_star_destroyer_button_final.jpg')
            buy_fighter_button = Buy_fighter_button(self, 4, [1130, 160], 'images\\buy_fighter_button_final.jpg')
            buy_transport_button = Buy_transport_button(self, 5, [1130, 210], 'images\\buy_transport_button_final.jpg')
        else:
            new_round_button = New_round_button(self, 1, [1130, 10], 'images\\new_round_button_full.jpg')
            build_space_factory_button = Build_space_factory_button(self, 2, [1130, 60], 'images\\build_space_factory_button_full.jpg')
            buy_star_destroyer_button = Buy_star_destroyer_button(self, 3, [1130, 110], 'images\\buy_star_destroyer_button_full.jpg')
            buy_fighter_button = Buy_fighter_button(self, 4, [1130, 160], 'images\\buy_fighter_button_full.jpg')
            buy_transport_button = Buy_transport_button(self, 5, [1130, 210], 'images\\buy_transport_button_full.jpg')
        save_and_quit_button = Save_and_quit_button(self, 6, [1130, 600], 'images\\save_and_quit_button_final.jpg')
        load_game_button = Load_game_button(self, 7, [1130, 650], 'images\\load_game_button_final.jpg')
        self.buttons.append(new_round_button) #WARNING! HAS TO BE THE FIRST BUTTON!
        self.buttons.append(build_space_factory_button)
        self.buttons.append(buy_star_destroyer_button)
        self.buttons.append(buy_fighter_button)
        self.buttons.append(buy_transport_button)
        self.buttons.append(save_and_quit_button)
        self.buttons.append(load_game_button) #WARNING! HAS TO BE THE LAST BUTTON!
        
            
    def start(self):
        
        #initialise background music
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
        if self.want_music:
            pygame.mixer.music.load(self.songs[npr.randint(len(self.songs))])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.2)
        
        #define colours
        BLACK = (0, 0, 0)
        GREEN = (0, 255, 0)
        
        #create background object and buttons
        background = Background(self.background_image, [0, 0])
        
        for button in self.buttons:
            self.all_sprites_list1.add(button)
        for player in self.players:
            for planet in player.planets:
                self.all_sprites_list1.add(planet)
            for ship in player.ships:
                self.all_sprites_list1.add(ship)
                
        while self.want_to_keep_playing:
            #EVENT HANDLING
            self.event_handling()
            
            #GAME LOGIC
            
            #functions for displaying text on the pygame window
            def text_objects(text, font):
                textSurface = font.render(text, True, GREEN)
                return textSurface, textSurface.get_rect()
            def message_display(text, lineNumber):
                largeText = pygame.font.Font('freesansbold.ttf', 12)
                TextSurf, TextRect = text_objects(text, largeText)
                TextRect.center = (1200, 300 + i*15)
                self.screen.blit(TextSurf, TextRect)
                            
            #GRAPHICS
            self.screen.fill(BLACK)
            self.screen.blit(background.image, background.rect)
            
            for i, msg in enumerate(self.messages):
                message_display(msg, i)
                
            self.all_sprites_list1.draw(self.screen)
            self.all_ship_sprites.draw(self.screen)
            for player in self.players:
                for planet in player.planets:
                    if planet.has_space_factory:
                        planet.draw_space_factory()
            
            pygame.display.flip()
            self.clock.tick(60)
              
        pygame.quit()
        
        
    def event_handling(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.want_to_keep_playing = False
            elif event.type == self.SONG_END:
                if self.want_music:
                    pygame.mixer.music.load(self.songs[npr.randint(len(self.songs))])
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(0.2)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x:
                    self.want_to_keep_playing = False
                if event.key==pygame.K_s:
                    if self.want_music:
                        self.want_music = False
                        pygame.mixer.music.stop()
                    else:
                        self.want_music = True
                        pygame.mixer.music.load(self.songs[npr.randint(len(self.songs))])
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_volume(0.2)
                if event.key==pygame.K_d:
                    if self.want_music:
                        pygame.mixer.music.load(self.songs[npr.randint(len(self.songs))])
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_volume(0.2)
                    
                if event.key==pygame.K_LEFT:
                    for player in self.players:
                        for ship in player.ships:
                            if ship.selected:
                                if not ship.already_travelled:
                                    ship.travel_left()
                                    self.ship_moved_check_collisions(ship)
                                else:
                                    print('\nThe selected ship has already travelled in this round!')
                                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
                if event.key==pygame.K_RIGHT:
                    for player in self.players:
                        for ship in player.ships:
                            if ship.selected:
                                if not ship.already_travelled:
                                    ship.travel_right()
                                    self.ship_moved_check_collisions(ship)
                                else:
                                    print('\nThe selected ship has already travelled in this round!')
                                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
                if event.key==pygame.K_UP:
                    for player in self.players:
                        for ship in player.ships:
                            if ship.selected:
                                if not ship.already_travelled:
                                    ship.travel_up()
                                    self.ship_moved_check_collisions(ship)
                                else:
                                    print('\nThe selected ship has already travelled in this round!')
                                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
                if event.key==pygame.K_DOWN:
                    for player in self.players:
                        for ship in player.ships:
                            if ship.selected:
                                if not ship.already_travelled:
                                    ship.travel_down()
                                    self.ship_moved_check_collisions(ship)
                                else:
                                    print('\nThe selected ship has already travelled in this round!')
                                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\error.wav'))
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                #check if the new round button has been clicked
                for button in self.buttons:
                    if button.position[0]<=mouse_pos[0] and mouse_pos[0]<=button.position[0]+140 and button.position[1]<=mouse_pos[1] and mouse_pos[1]<=button.position[1]+40:
                        button.command()
                #check if a planet or ship has been clicked
                for player in self.players:
                    wannaBreak = False #if a ship has been clicked, don't look for planets being clicked
                    for ship in player.ships:
                        if ship.position[0]<=mouse_pos[0] and mouse_pos[0]<=ship.position[0]+self.TILE_SIZE and ship.position[1]<=mouse_pos[1] and mouse_pos[1]<=ship.position[1]+self.TILE_SIZE:
                            ship.click()
                            wannaBreak = True
                    if wannaBreak:
                        break
                    for planet in player.planets:
                        if planet.position[0]<=mouse_pos[0] and mouse_pos[0]<=planet.position[0]+self.TILE_SIZE and planet.position[1]<=mouse_pos[1] and mouse_pos[1]<=planet.position[1]+self.TILE_SIZE:
                            planet.click()
        
                            
        
        
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
     
    


        
