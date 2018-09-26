
import pygame

BLACK = (0, 0, 0)

pygame.init()
#pygame.mixer.init()

screen = pygame.display.set_mode((300,200))
clock = pygame.time.Clock()

want_to_end = False
while not want_to_end:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            want_to_end = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\ship_click.wav'))
            if event.key == pygame.K_d:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('sounds\\planet_click.wav'))
            if event.key == pygame.K_f:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('sounds\\captured.wav'))
            if event.key == pygame.K_g:
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('sounds\\explosion.mp3'))
            if event.key == pygame.K_h:
                pygame.mixer.music.load('music\\karaste_broder.mp3')
                pygame.mixer.music.play()
            if event.key == pygame.K_j:
                pygame.mixer.music.stop()
                
    screen.fill(BLACK)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()