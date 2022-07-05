import pygame, sys
from button import Button
import pygame
from checkers.constant import SQUARE_SIZE, WHITE, WIDTH, HEIGHT,RED, ORANGE
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("American Draughts")



def get_row_col_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col




pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("American Draughts")

BG =   pygame.transform.scale(pygame.image.load("assets/Background.png"), (WIDTH,HEIGHT)) 



def get_font(size): #
    return pygame.font.Font("assets/font.ttf", size)

    
def options(flag):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    
    while(run):
        clock.tick(FPS)
        
        
        
        if(flag==1):
            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(),3, WHITE, game)
                game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:   
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                game.select(row,col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                
        
        game.update()
        pygame.time.delay(250)


    pygame.quit()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        
        PLAY_WITH_HUMAN = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(WIDTH/2, HEIGHT*1/3), 
                            text_input="PLAY_WITH_HUMAN", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        PLAY_WITH_AI = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(WIDTH/2, HEIGHT*1/3+125), 
                            text_input="PLAY_WITH_AI", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WIDTH/2, HEIGHT*1/3+250), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_WITH_HUMAN,PLAY_WITH_AI, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if PLAY_WITH_HUMAN.checkForInput(MENU_MOUSE_POS):
                    flag = 0
                    options(flag)
                if PLAY_WITH_AI.checkForInput(MENU_MOUSE_POS):
                    flag = 1
                    options(flag)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()































# def main():
#    



# main()