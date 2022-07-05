import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLUMNS = 8,8

SQUARE_SIZE = WIDTH//COLUMNS


#rgb
RED = (255, 204, 000)
BLUE = (0,0, 255)
WHITE = (255, 128, 000)
BLACK = (40,40,40)
GRAY = (128, 128, 128)



YELLOW = (255, 204, 000)
ORANGE=(255, 128, 000)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown1.png'), (75,75))

START_IMG = pygame.transform.scale(pygame.image.load('assets/start.png'), (200,75))  


STOP_IMG =  pygame.transform.scale(pygame.image.load('assets/stop.png'), (200,75))   