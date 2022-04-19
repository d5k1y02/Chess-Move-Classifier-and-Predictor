# -*- coding: utf-8 -*-
"""
@author: Desmond Yancey
"""

"""This is a classification algorithm for chess moves. Given a position in array format, 
it will determine if a chosen move meets a variety of criteria.
notation is as follows: k = king, q = queen, n = knight, b = bishop,r = rook and p = pawn"""



    
    
import chess.pgn
import copy
from collections import Counter

def is_pawn_move(position, move): 
    if position[move[0]][move[1]][0] == 'p':
        return True
    return False

def is_rook_move(position, move): 
    if position[move[0]][move[1]][0] == 'r':
        return True
    return False

def is_knight_move(position, move): 
    if position[move[0]][move[1]][0] == 'n':
        return True
    return False

def is_bishop_move(position, move): 
    if position[move[0]][move[1]][0] == 'b':
        return True
    return False

def is_queen_move(position, move): 
    if position[move[0]][move[1]][0] == 'q':
        return True
    return False

def is_king_move(position, move): 
    if position[move[0]][move[1]][0] == 'k':
        return True
    return False

def determine_source_quadrant(move, quadrant): 
    if quadrant == "BOTLEFT":
        if(move[0] < 4 and move[1] < 4):
            return True
        else:
            return False
    
    if quadrant == "BOTRIGHT":
        if(move[0] < 4 and move[1] >= 4):
            return True
        else:
            return False
    
    if quadrant == "TOPLEFT":
        if(move[0] >= 4 and move[1] < 4):
            return True
        else:
            return False

    if quadrant == "TOPLEFT":
        if(move[0] >= 4 and move[1] >= 4):
            return True
        else:
            return False


def determine_dest_quadrant(move, quadrant): 
    if quadrant == "BOTLEFT":
        if(move[2] < 4 and move[3] < 4):
            return True
        else:
            return False
    
    if quadrant == "BOTRIGHT":
        if(move[2] < 4 and move[3] >= 4):
            return True
        else:
            return False
    
    if quadrant == "TOPLEFT":
        if(move[2] >= 4 and move[3] < 4):
            return True
        else:
            return False

    if quadrant == "TOPLEFT":
        if(move[2] >= 4 and move[3] >= 4):
            return True
        else:
            return False



""" accepts a position in the array format created by fen_to_array and a move tuple 
(pos1l,pos1n,pos2l,pos2n) and returns a dictionary of classifications that apply to that move"""
def move_classifier(position,board, move, move_original):
    piece_class = {}                 #dictionary used to hold which piece type was moved
    source_class = {}                #hold source quadrant
    dest_class = {}                  #hold destination quadrant
    piece_class["PAWN"] = is_pawn_move(position, move)
    piece_class["ROOK"] = is_rook_move(position, move)
    piece_class["KNIGHT"] = is_knight_move(position, move)
    piece_class["BISHOP"] = is_bishop_move(position, move)
    piece_class["QUEEN"] = is_queen_move(position, move)
    piece_class["KING"] = is_king_move(position, move)
    source_class["BOTLEFT"] = determine_source_quadrant(move, "BOTLEFT")
    source_class["BOTRIGHT"] = determine_source_quadrant(move, "BOTRIGHT")
    source_class["TOPLEFT"] = determine_source_quadrant(move, "TOPLEFT")
    source_class["TOPRIGHT"] = determine_source_quadrant(move, "TOPRIGHT")
    dest_class["BOTLEFT"] = determine_dest_quadrant(move, "BOTLEFT")
    dest_class["BOTRIGHT"] = determine_dest_quadrant(move, "BOTRIGHT")
    dest_class["TOPLEFT"] = determine_dest_quadrant(move, "TOPLEFT")
    dest_class["TOPRIGHT"] = determine_dest_quadrant(move, "TOPRIGHT")
    
    return piece_class

"""converts chess fen format to an array in the format board[coord1][coord2] = (piece, color)"""
def fen_to_array(input_fen):
    
    position = [[('e', 'e') for i in range(8)] for j in range(8)] #board[coord1][coord2] = (piece, color)
    fen = input_fen.replace('/', ',')
    fen = fen.replace(' ', ',')
    ranks = fen.split(',')
    k = 0
    for i in range(8):
        for j in ranks[i]:
            if not(j.isdigit()):
                if j.islower():
                    position[i][k] = (j, 'b')
                    k+=1
                else:
                    position[i][k] = (j.lower(), 'w')
                    k+=1
            else:
                k+=int(j)
        k = 0
    return position

def create_classify_file(input_file, label_csv, is_testset = False):
    if(is_testset):
        piece_class = {}
        position = [[('e', 'e') for i in range(8)] for j in range(8)]
        pgn = open(input_file)
        labels = open(label_csv, "a")
        i = 0
        game = chess.pgn.read_game(pgn)
        while(game):
            # Iterate through all moves and play them on a board.
            board = game.board()
            for move in game.mainline_moves():
                move_t = (7-chess.square_rank(move.from_square), chess.square_file(move.from_square),\
                    7-chess.square_rank(move.to_square), chess.square_file(move.to_square) )
                position = fen_to_array(board.fen())
                i+=1
                piece_class = move_classifier(position,board,move_t, move)
                board.push(move)
                directory = ""
                labelname = ""
                move_class = 0
                if piece_class["PAWN"]:
                    directory = "chessdataset/test/PAWN/"
                    labelname = "PAWN/"
                    move_class = 0
                elif piece_class["ROOK"]:
                    directory = "chessdataset/test/ROOK/"
                    labelname = "ROOK/"
                    move_class = 1
                elif piece_class["KNIGHT"]:
                    directory = "chessdataset/test/KNIGHT/"
                    labelname = "KNIGHT/"
                    move_class = 2
                elif piece_class["BISHOP"]:
                    directory = "chessdataset/test/BISHOP/"
                    labelname = "BISHOP/"
                    move_class = 3
                elif piece_class["QUEEN"]:
                    directory = "chessdataset/test/QUEEN/"
                    labelname = "QUEEN/"
                    move_class = 4
                elif piece_class["KING"]:
                    directory = "chessdataset/test/KING/"
                    labelname = "KING/"
                    move_class = 5
                else:
                    print("error, piece class has invalid value")
                
                filename = directory + "position"+ str(i) +".txt"
                labelname = labelname + "position"+ str(i) + ".txt"
                pos_file = open(filename, "w+")
                print(filename + ',', move_class, file = labels)
                for r in position:
                    print(r, file = pos_file)
                # print(piece_class)
                pos_file.close()
            game = chess.pgn.read_game(pgn)
    else:
        piece_class = {}
        position = [[('e', 'e') for i in range(8)] for j in range(8)]
        pgn = open(input_file)
        labels = open(label_csv, "a")
        i = 0
        game = chess.pgn.read_game(pgn)
        while(game):
            # Iterate through all moves and play them on a board.
            board = game.board()
            for move in game.mainline_moves():
                move_t = (7-chess.square_rank(move.from_square), chess.square_file(move.from_square),\
                    7-chess.square_rank(move.to_square), chess.square_file(move.to_square) )
                position = fen_to_array(board.fen())
                i+=1;
                piece_class = move_classifier(position,board,move_t, move)
                board.push(move)
                directory = ""
                labelname = ""
                move_class = 0
                if piece_class["PAWN"]:
                    directory = "chessdataset/train/PAWN/"
                    labelname = "PAWN/"
                    move_class = 0
                elif piece_class["ROOK"]:
                    directory = "chessdataset/train/ROOK/"
                    labelname = "ROOK/"
                    move_class = 1
                elif piece_class["KNIGHT"]:
                    directory = "chessdataset/train/KNIGHT/"
                    labelname = "KNIGHT/"
                    move_class = 2
                elif piece_class["BISHOP"]:
                    directory = "chessdataset/train/BISHOP/"
                    labelname = "BISHOP/"
                    move_class = 3
                elif piece_class["QUEEN"]:
                    directory = "chessdataset/train/QUEEN/"
                    labelname = "QUEEN/"
                    move_class = 4
                elif piece_class["KING"]:
                    directory = "chessdataset/train/KING/"
                    labelname = "KING/"
                    move_class = 5
                else:
                    print("error, piece class has invalid value")
                
                filename = directory + "position"+ str(i) +".txt"
                labelname = labelname + "position"+ str(i) + ".txt"
                pos_file = open(filename, "w+")
                print(filename + ',', move_class, file = labels)
                for r in position:
                    print(r, file = pos_file)
                # print(piece_class)
                pos_file.close()
            game = chess.pgn.read_game(pgn)
    return True
    

l_csv_train = "chess_labels_train.csv"
l_csv_test = "chess_labels_test.csv"
create_classify_file("chess_com_games_2021-04-24.pgn", l_csv_train)    
create_classify_file("chess_com_games_2021-04-24.pgn", l_csv_test, True)  
    
