
import pygame

from .piece import Piece 
from .constant import BLACK, ROWS, RED, SQUARE_SIZE, COLUMNS, WHITE

class Board:
    def __init__(self):
        self.board = []
       
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                 pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return (self.white_left - self.red_left) + (self.white_kings * 0.5 - self.red_kings * 0.5)


    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color ==color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
       

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS-1 or row==0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings +=1
            else: 
                self.red_kings +=1
            
        
    def get_piece(self, row, col):
        
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col%2 == ((row+1))%2:
                    if(row<3):
                        self.board[row].append(Piece(row, col, WHITE))
                    elif (row>4):
                        self.board[row].append(Piece(row, col, RED))
                    else: 
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece!=0:
                    piece.draw(win)


    def remove(self, pieces):
        
        for piece in pieces:
            
            self.board[piece.row][piece.col] = 0
            if piece != 0 :
                if piece.color == RED:
                    self.red_left -=1
                else:
                    self.white_left -=1

    def winner(self):
        if self.red_left<=0:
            return WHITE
        elif self.white_left<=0:
            return RED
        return None



    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col-1
        right = piece.col+1
        row = piece.row

        if piece.color == RED:
            moves.update(self._traverse_left(piece,row-1, max(row-3,-1),-1, piece.color, left))
            moves.update(self._traverse_right(piece,row-1, max(row-3,-1),-1, piece.color, right))
        if piece.color == WHITE :
            moves.update(self._traverse_left(piece,row+1, min(row+3, ROWS),1, piece.color, left))
            moves.update(self._traverse_right(piece,row+1, min(row+3,ROWS),1, piece.color, right))
        if piece.king:
            moves.update(self._traverse_left(piece,row-1, max(row-3,-1),-1, piece.color, left))
            moves.update(self._traverse_right(piece,row-1, max(row-3,-1),-1, piece.color, right))
            moves.update(self._traverse_left(piece,row+1, min(row+3, ROWS),1, piece.color, left))
            moves.update(self._traverse_right(piece,row+1, min(row+3,ROWS),1, piece.color, right))



            for (roww, coll) in moves:
                # print(roww, coll)
                if len(moves[(roww, coll)])>0 :
                    # print("=====>", moves[(roww, coll)][0], type(moves[(roww, coll)][0]))
                
                    if moves[(roww, coll)][0].color == piece.color:
                        
                        if (roww+1,coll+1) in moves:
                            moves[(roww, coll)] = moves[(roww+1,coll+1)]
                        elif (roww+1,coll-1) in moves:
                            moves[(roww, coll)] = moves[(roww+1,coll-1)]
                        elif (roww-1,coll+1) in moves:
                            moves[(roww, coll)] = moves[(roww-1,coll+1)]
                        elif (roww-1,coll-1) in moves:
                            moves[(roww, coll)] = moves[(roww-1,coll-1)]

        return moves

    def _traverse_left(self, piece,start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left<0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break     
                elif skipped:
                    moves[(r,left)] = last+skipped
                else:
                    moves[(r,left)] = last
                if last:
                    if step ==-1:
                        row = max(r-3, -1)    
                    else:
                        row = min(r+3,ROWS)
                    moves.update(self._traverse_left(piece,r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(piece,r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color==color:
                if piece.king:
                    moves[(r,left)] = [current]
                    break
                else:
                    break
            else:
                last = [current]
            
            left-=1
        return moves

    def _traverse_right(self,piece, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right>=COLUMNS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break     
                elif skipped:
                    moves[(r,right)] = last+skipped
                else:
                    moves[(r,right)] = last
                if last:
                    if step ==-1:
                        row = max(r-3, -1)    
                    else:
                        row = min(r+3,ROWS)
                    moves.update(self._traverse_left(piece,r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(piece,r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color==color:
                if piece.king:
                    moves[(r,right)] = [current]
                    break
                else:
                    break
            else:
                last = [current]
            
            right+=1    
        return moves