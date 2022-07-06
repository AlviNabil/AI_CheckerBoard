from asyncio.windows_events import NULL
from multiprocessing.connection import wait
import pygame
from .constant import RED, SQUARE_SIZE, WHITE, BLUE, CROWN, ROWS
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.pulse = 0
        self.end = 0
    def update(self):

        self.board.draw(self.win)
        
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init() 

    def select(self, row, col):
        
        self.pulse = 0
        
        if self.selected:
            result  = self._move(row, col)
            if not result: 
                self.selected = None
                self.select(row, col)
        else:
            self.valid_moves = []
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            # print("=====",self.valid_moves)
            if len(self.valid_moves) == 0:
                # print("yes")
                if self.board.red_left<=3: 
                    self.end = 1
                        
            return True
        return False



    def winner(self):
        return self.board.winner()

    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # print(self.selected, piece, self.selected==piece, type(self.selected), type(piece))
        if self.selected   and (row, col) in self.valid_moves:
            # print("hello0")
            if piece==0 or piece.color == self.selected.color:
                # print(piece,"========", self.selected, "=========", self.valid_moves)
                # print("heloo1")
                if piece==0:
                    self.board.move(self.selected, row, col)
                else:
                    # print(piece,"========", self.selected, "=========", self.valid_moves)
                    # print(row,"============",col)
                    if self.selected.row == ROWS-1 or self.selected.row==0:
                        self.selected.king = piece.king = True
                    self.selected.king, piece.king = piece.king, self.selected.king
                # for moves in self.valid_moves:
                #     print(moves, "|||||||||||||||||||||||||||",self.valid_moves[moves])    
                skipped = self.valid_moves[(row, col)]
                # for skip in skipped:
                #     print(skip.row, skip.col)
                if skipped:
                    self.board.remove(skipped)
                self.change_turn()




           
            
            
        else:
            # print("heloo3")
            return False
        return True
    
    
    def draw_valid_moves(self, moves):
        if self.pulse == 0:
            for move in moves:
                row, col  = move
                piece = self.board.get_piece(row, col)
                if piece != 0:
                    if piece.color == self.selected.color:
                        pygame.draw.circle(self.win, WHITE, (col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2), 15 )
                        self.win.blit(CROWN, (piece.x - CROWN.get_width()//2, piece.y - CROWN.get_height()//2))
                        self.pulse = 1
                else:

                    pygame.draw.circle(self.win, BLUE, (col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2), 15 )
                    self.pulse = 1
                
        else:
            for move in moves:
                row, col  = move
                piece = self.board.get_piece(row, col)
                if piece != 0:
                    if piece.color == self.selected.color:
                        pygame.draw.circle(self.win, WHITE, (col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2), 15 )
                        pygame.draw.circle(self.win, piece.color, (piece.x, piece.y), piece.radius)
                        self.pulse = 0
                else:

                    pygame.draw.circle(self.win, RED, (col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2), 15 )
                    self.pulse = 0


                  


    def change_turn(self):
        self.valid_moves = []
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED



    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board 
        self.change_turn()