from copy import deepcopy
from pickle import TRUE
from turtle import pos
import pygame
from checkers.constant import RED, WHITE, ROWS


def minimax(position, depth, max_player, game):
    if depth==0 or position.winner()!=None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        # print("best",best_move)
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        # print("best",best_move)
        return minEval, best_move



def simulate_move(piece, move, board, game, skip):
    # print("----->2",piece)
    
    anp =  board.get_piece(move[0],move[1])
   

    if anp==0:
        board.move(piece, move[0], move[1])
    else:
        
        if piece.row == ROWS-1 or piece.row==0:
            piece.king = anp.king = True
        piece.king, anp.king = anp.king, piece.king



   
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    all_piece = board.get_all_pieces(color)
    # for piece in all_piece:
    #     print(piece, piece.color)
    for piece in all_piece:
        valid_moves = board.get_valid_moves(piece)
        # print("######",valid_moves,"-------------", piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            # print("===========> row colo",piece.row, piece.col)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
           
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win,(0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(300)