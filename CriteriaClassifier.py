# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:00:53 2021

@author: Desmond Yancey
"""

"""This is a classification algorithm for chess moves. Given a position in array format, 
it will determine if a chosen move meets a variety of criteria.
notation is as follows: k = king, q = queen, n = knight, b = bishop,r = rook and p = pawn"""



    
    
import chess.pgn
import copy
from collections import Counter


def is_developing(position, move): #improve position of piece CURRENTLY TRUE IF PIECE MOVED IS NOT A PAWN OR KING
    if position[move[0]][move[1]][0] == 'r' or position[move[0]][move[1]][0] == 'q'\
    or position[move[0]][move[1]][0] == 'n' or position[move[0]][move[1]][0] == 'b':
        return True
    return False

"""(board, piece) Take a board position and a piece to move and return any pieces the input can see diagonally"""
def diag_vision(position,in_piece):
    piece_list = [] #list of pieces the input contacts on diagonals
    
    for i in range(min(in_piece[0], (8-in_piece[1]))): #up-right
        pos = position[in_piece[0]-i][in_piece[1]+i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-i,in_piece[1]+i,pos[0],pos[1]))
            break
        
    for i in range(min((8-in_piece[0]), (8-in_piece[1]))): #down-right
        pos = position[in_piece[0]+i][in_piece[1]+i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+i,in_piece[1]+i,pos[0],pos[1]))
            break
        
    for i in range(min(in_piece[0], in_piece[1])): #up-left
        pos = position[in_piece[0]-i][in_piece[1]-i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+i,in_piece[1]-i,pos[0],pos[1]))
            break
        
    for i in range(min((8-in_piece[0]), in_piece[1])): #down-left
        pos = position[in_piece[0]+i][in_piece[1]-i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-i,in_piece[1]-i,pos[0],pos[1]))
            break
        
    return piece_list

"""(board, piece) Take a board position and a piece to move and return any pieces 
the input can see through a rank or file"""
def straight_vision(position,in_piece):
    piece_list = [] #list of pieces the input contacts on ranks and files
    
    for i in range(in_piece[0]): #up
        pos = position[in_piece[0]-i][in_piece[1]]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-i,in_piece[1],pos[0],pos[1]))
            break
        
    for i in range(8-in_piece[0]): #down
        pos = position[in_piece[0]+i][in_piece[1]]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+i,in_piece[1],pos[0],pos[1]))
            break
        
    for i in range(in_piece[1]): #left
        pos = position[in_piece[0]][in_piece[1]-i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0],in_piece[1]-i,pos[0],pos[1]))
            break
        
    for i in range(8-in_piece[1]): #right
        pos = position[in_piece[0]][in_piece[1]+i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0],in_piece[1]+i,pos[0],pos[1]))
            break
        
    return piece_list

"""(board, piece) Take a board position and a piece to move and return any pieces 
the input can see through an L-shape"""
def knight_vision(position,in_piece):
    piece_list = [] #list of pieces the input contacts on L-shape
    if in_piece[0] <=5: #down
        if in_piece[1] <= 6:
            pos = position[in_piece[0]+2][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+2,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[1] >= 1:
            pos = position[in_piece[0]+2][in_piece[1]-1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+2,in_piece[1]-1,pos[0],pos[1]))
                
    if in_piece[0] >=2: #up
        if in_piece[1] <= 6:
            pos = position[in_piece[0]-2][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-2,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[1] >= 1:
            pos = position[in_piece[0]-2][in_piece[1]-1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-2,in_piece[1]-1,pos[0],pos[1]))
                
    if in_piece[1] >=2: #left
        if in_piece[0] <= 6:
            pos = position[in_piece[0]+1][in_piece[1]-2]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+1,in_piece[1]-2,pos[0],pos[1]))
        if in_piece[0] >= 1:
            pos = position[in_piece[0]-1][in_piece[1]-2]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]-2,pos[0],pos[1]))
    
    if in_piece[1] <= 5: #right
        if in_piece[0] <= 6:
            pos = position[in_piece[0]+1][in_piece[1]+2]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+1,in_piece[1]+2,pos[0],pos[1]))
        if in_piece[0] >= 1:
            pos = position[in_piece[0]-1][in_piece[1]+2]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]+2,pos[0],pos[1]))
        
    return piece_list

"""(board, piece, color) Take a board position and a piece to move and return any pieces 
the input can see 1 square diagonally in front of it. Front or behind is determined by color"""
def pawn_vision(position, in_piece, color):
    piece_list = [] #list of pieces the input contacts on 1-sqaure forward diagonal
    
    if color == 'w': #if color is white, look upward
        if in_piece[0] >= 1 and in_piece[1] <= 6:
            pos = position[in_piece[0]-1][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[0] >= 1 and in_piece[1] >= 1:
            pos = position[in_piece[0]-1][in_piece[1]-1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]-1,pos[0],pos[1]))
                
    if color == 'b': #if color is black, look downward
        if in_piece[0] <= 6 and in_piece[1] <= 6:
            pos = position[in_piece[0]+1][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+1,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[0] <= 6 and in_piece[1] >= 1:
            pos = position[in_piece[0]+1][in_piece[1]-1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+1,in_piece[1]-1,pos[0],pos[1]))
                
    return piece_list

"""(board, piece, color) """
def king_vision(position, in_piece):
    piece_list = [] #list of pieces the input contacts on 1-sqaure forward diagonal
    #check diagonals
    if (in_piece[0] >= 1) and (in_piece[1] <= 6): #up-right
        pos = position[in_piece[0]-1][in_piece[1]+1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-1,in_piece[1]+1,pos[0],pos[1]))
    if (in_piece[0] >= 1) and (in_piece[1] >= 1): #up-left
        pos = position[in_piece[0]-1][in_piece[1]-1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-1,in_piece[1]-1,pos[0],pos[1]))     
    if (in_piece[0] <= 6) and (in_piece[1] <= 6): #down-right
        pos = position[in_piece[0]+1][in_piece[1]+1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+1,in_piece[1]+1,pos[0],pos[1]))
    if (in_piece[0] <= 6) and (in_piece[1] >= 1): #down-left
        pos = position[in_piece[0]+1][in_piece[1]-1]
        if  pos != ('e','e'): 
            piece_list.append((in_piece[0]+1,in_piece[1]-1,pos[0],pos[1]))
        
    #check ranks and files   
    if in_piece[0] >= 1: #up
        pos = position[in_piece[0]-1][in_piece[1]]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]-1,in_piece[1],pos[0],pos[1]))
    if in_piece[0] <= 6: #down
        pos = position[in_piece[0]+1][in_piece[1]]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+1,in_piece[1],pos[0],pos[1]))     
    if in_piece[1] <= 6: #right
        pos = position[in_piece[0]][in_piece[1]+1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0],in_piece[1]+1,pos[0],pos[1]))
    if in_piece[1] >= 1: #left
        pos = position[in_piece[0]][in_piece[1]-1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0],in_piece[1]-1,pos[0],pos[1]))
            
    return piece_list

"""(position, move) Take a chess postion and a move and determine if that move result in a check"""
def is_check(position, move): #is move a check
    color = position[move[0]][move[1]][1] #color of player whose turn it is
    opp_color = 'w'
    if color == 'w':
        opp_color = 'b'
    
    piece_list = [] #(pos1,pos2,piece)
    
    for i in range(8):
        for j in range(8):
            if position[i][j][1] == color:
                piece_list.append((i, j, position[i][j][0])) #add every friendly piece to the list
                            
    for piece in piece_list:
        if piece[2] == 'q':
            pieces_seen = diag_vision(position, piece) + straight_vision(position, piece)
            for p in pieces_seen:
                if(p[2] == 'k' and p[3] == opp_color):
                    return True
        elif piece[2] == 'r':
            pieces_seen = straight_vision(position, piece)
            for p in pieces_seen:
                if(p[2] == 'k' and p[3] == opp_color):
                    return True
        elif piece[2] == 'n':
            pieces_seen = knight_vision(position, piece)
            for p in pieces_seen:
                if(p[2] == 'k' and p[3] == opp_color):
                    return True
        elif piece[2] == 'b':
            pieces_seen = diag_vision(position, piece)
            for p in pieces_seen:
                if(p[2] == 'k' and p[3] == opp_color):
                    return True
        elif piece[2] == 'p':
            pieces_seen = pawn_vision(position, piece, color)
            for p in pieces_seen:
                if(p[2] == 'k' and p[3] == opp_color):
                    return True
   
    return False
"""(position, move) Take a chess postion and a move and determine if that move creates an attack"""
def is_attack(position, move): #does move attack a piece

    
    color = position[move[0]][move[1]][1] #color of player whose turn it is
    opp_color = 'w'
    if color == 'w':
        opp_color = 'b'
    
    piece_list = [] #(pos1,pos2,piece)
    
    for i in range(8):
        for j in range(8):
            if position[i][j][1] == color:
                piece_list.append((i, j, position[i][j][0])) #add every friendly piece to the list
    pieces_seen = []           
    for piece in piece_list:
        if piece[2] == 'q':
            pieces_seen = diag_vision(position, piece) + straight_vision(position, piece)
            
        elif piece[2] == 'r':
            pieces_seen.extend(straight_vision(position, piece))
        
        elif piece[2] == 'n':
            pieces_seen.extend(knight_vision(position, piece))
         
        elif piece[2] == 'b':
            pieces_seen.extend(diag_vision(position, piece))
            
        elif piece[2] == 'p':
            pieces_seen.extend(pawn_vision(position, piece, color))
        
        elif piece[2] == 'k':
            pieces_seen.extend(king_vision(position, piece))
            
    for p in pieces_seen:
        if position[p[0]][p[1]][1] == color:
            pieces_seen.remove(p)
        
    pre_move_counter = Counter(pieces_seen)  
        
    position[move[2]][move[3]] = position[move[0]][move[1]] #make the move FIX FOR CASTLING
    position[move[0]][move[1]] = ('e','e')
        
    for piece in piece_list:
        if piece[2] == 'q':
            pieces_seen = diag_vision(position, piece) + straight_vision(position, piece)
            
        elif piece[2] == 'r':
            pieces_seen.extend(straight_vision(position, piece))
        
        elif piece[2] == 'n':
            pieces_seen.extend(knight_vision(position, piece))
         
        elif piece[2] == 'b':
            pieces_seen.extend(diag_vision(position, piece))
            
        elif piece[2] == 'p':
            pieces_seen.extend(pawn_vision(position, piece, color))
        
        elif piece[2] == 'k':
            pieces_seen.extend(king_vision(position, piece))
        
    for p in pieces_seen:
        if position[p[0]][p[1]][1] == color:
            pieces_seen.remove(p)
                    
                
    post_move_counter = Counter(pieces_seen) 
    
    diff = post_move_counter - pre_move_counter
    if diff != Counter():
        return True
                
    return False
def is_move_attacking(board, move):
    
    if board.is_capture(move):
        return False
    board_copy = copy.deepcopy(board)
    board_copy.push(move)
    p_list = board.piece_map()
    ep_list = []
        
        
    for sq, s in p_list.items():
        if board.turn:
            if s.symbol().islower():
                ep_list.append((sq, s))
        else:
            if s.symbol().isupper():
                ep_list.append((sq, s))
    
    p_list2 = board_copy.piece_map()
    ep_list2 = []
    
    for sq, s in p_list2.items():
        if board.turn:
            if s.symbol().islower():
                ep_list2.append((sq, s))
        else:
            if s.symbol().isupper():
                ep_list2.append((sq, s))
                
    attackers_list = []     
    attackers_list_after_move = []      
    for n, s in ep_list:
        attackers_list.append(len(board.attackers(board.turn, n)))
        
    for n, s in ep_list2:
        attackers_list_after_move.append(len(board_copy.attackers(board.turn, n)))
        
    for i in range(len(attackers_list)):
        if attackers_list_after_move[i] > attackers_list[i]:
            return True
    return False

def is_capture(position, move): #is move a capture

    if position[move[2]][move[3]] != ('e', 'e'):
        return True
    return False


def is_piece_attacked(position, move, input_piece): #determine if the input piece is attacked
    color = position[move[0]][move[1]][1] #color of player whose turn it is
    opp_color = 'w'
    if color == 'w':
        opp_color = 'b'
    temp_list = straight_vision(position, input_piece)
    for p in temp_list:
        if p[3] == opp_color and (p[2] ==  'r' or p[2] == 'q'):
            return True
    temp_list = diag_vision(position, input_piece)
    for p in temp_list:
        if p[3] == opp_color and (p[2] ==  'b' or p[2] == 'q'):
            return True
    temp_list = knight_vision(position, input_piece)
    for p in temp_list:
        if p[3] == opp_color and (p[2] ==  'n'):
            return True
    if(color == 'w'):
        if(input_piece[0] != 0):
            temp_list = pawn_vision(position, input_piece, color)
    if(color == 'b'):
        if(input_piece[0] != 7):
            temp_list = pawn_vision(position, input_piece, color)
    for p in temp_list:
        if p[3] == opp_color and (p[2] ==  'p'):
            return True
    temp_list = king_vision(position, input_piece)
    for p in temp_list:
        if p[3] == opp_color and (p[2] ==  'k'):
            return True

    return False

def is_defense(position, move): #does move defend a piece or pawn under attack

    #first list all attacked pieces and pawns on your side
    color = position[move[0]][move[1]][1] #color of player whose turn it is
    attacked_list = []
    for i in range(8):
        for j in range(8):
            if is_piece_attacked(position, move, (i, j, position[i][j][0])):
                attacked_list.append((i, j, position[i][j][0]))
    pieces_seen = []
    p = (move[2], move[3], position[move[0]][move[1]][0])
    if p[2] == 'q':
        pieces_seen = diag_vision(position, p) + straight_vision(position, p)
    elif p[2] == 'r':
        pieces_seen.extend(straight_vision(position, p))
    
    elif p[2] == 'n':
        pieces_seen.extend(knight_vision(position, p))
     
    elif p[2] == 'b':
        pieces_seen.extend(diag_vision(position, p))
        
    elif p[2] == 'p':
        pieces_seen.extend(pawn_vision(position, p, color))
    else:
        pieces_seen.extend(king_vision(position, p))
        
    for piece in attacked_list:
        if piece in pieces_seen:
            return True
    return False

def is_retreat(position, move): #does move retreat an attacked piece
    if is_piece_attacked(position, move, (move[0], move[1], position[move[0]][move[1]][0])):
        return True
    return False

def is_pawnpush(position, move):
    if position[move[0]][move[1]][0] == 'p':
        return True
    return False

def is_kingmove(position, move):
    if position[move[0]][move[1]][0] == 'k':
        return True
    return False

""" accepts a position in the array format created by fen_to_array and a move tuple 
(pos1l,pos1n,pos2l,pos2n) and returns a dictionary of classifications that apply to that move"""
def move_classifier(position,board, move, move_original):
    criteria = {}                 #define criteria-this may grow as needed
    positiond = copy.deepcopy(position) #not memory efficient, but doesn't work otherwise
    positionc = copy.deepcopy(position)
    positionc2 = copy.deepcopy(position)
    positiond2 = copy.deepcopy(position)
    positionr = copy.deepcopy(position)
    criteria["DEVELOPE"] = (is_developing(positiond, move))
    criteria["CHECK"] = (board.gives_check(move_original))
    criteria["ATTACK"] = (is_move_attacking(board, move_original))
    criteria["CAPTURE"] = (is_capture(positionc2, move))
    criteria["DEFEND"] = (is_defense(positiond2, move))
    criteria["RETREAT"] = (is_retreat(positionr, move))
    criteria["PAWNPUSH"] = (is_pawnpush(position, move))
    criteria["KINGMOVE"] = (is_kingmove(position, move))
    
    return criteria

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
        criteria = {}
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
                criteria = move_classifier(position,board,move_t, move)
                board.push(move)
                directory = ""
                labelname = ""
                move_class = 0
                if criteria["CAPTURE"]:
                    directory = "chessdataset/test/CAPTURE/"
                    labelname = "CAPTURE/"
                    move_class = 0
                elif criteria["CHECK"]:
                    directory = "chessdataset/test/CHECK/"
                    labelname = "CHECK/"
                    move_class = 1
                elif criteria["ATTACK"]:
                    directory = "chessdataset/test/ATTACK/"
                    labelname = "ATTACK/"
                    move_class = 2
                elif criteria["DEFEND"]:
                    directory = "chessdataset/test/DEFEND/"
                    labelname = "DEFEND/"
                    move_class = 3
                elif criteria["RETREAT"]:
                    directory = "chessdataset/test/RETREAT/"
                    labelname = "RETREAT/"
                    move_class = 4
                elif criteria["PAWNPUSH"]:
                    directory = "chessdataset/test/PAWNPUSH/"
                    labelname = "PAWNPUSH/"
                    move_class = 5
                elif criteria["KINGMOVE"]:
                    directory = "chessdataset/test/KINGMOVE/"
                    labelname = "KINGMOVE/"
                    move_class = 6
                else:
                    directory = "chessdataset/test/DEVELOPE/"
                    labelname = "DEVELOPE/"
                    move_class = 7
                
                filename = directory + "position"+ str(i) +".txt"
                labelname = labelname + "position"+ str(i) + ".txt"
                pos_file = open(filename, "w+")
                print(filename + ',', move_class, file = labels)
                for r in position:
                    print(r, file = pos_file)
                # print(criteria)
                pos_file.close()
            game = chess.pgn.read_game(pgn)
    else:
        criteria = {}
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
                criteria = move_classifier(position,board,move_t, move)
                board.push(move)
                directory = ""
                labelname = ""
                move_class = 0
                if criteria["CAPTURE"]:
                    directory = "chessdataset/train/CAPTURE/"
                    labelname = "CAPTURE/"
                    move_class = 0
                elif criteria["CHECK"]:
                    directory = "chessdataset/train/CHECK/"
                    labelname = "CHECK/"
                    move_class = 1
                elif criteria["ATTACK"]:
                    directory = "chessdataset/train/ATTACK/"
                    labelname = "ATTACK/"
                    move_class = 2
                elif criteria["DEFEND"]:
                    directory = "chessdataset/train/DEFEND/"
                    labelname = "DEFEND/"
                    move_class = 3
                elif criteria["RETREAT"]:
                    directory = "chessdataset/train/RETREAT/"
                    labelname = "RETREAT/"
                    move_class = 4
                elif criteria["PAWNPUSH"]:
                    directory = "chessdataset/train/PAWNPUSH/"
                    labelname = "PAWNPUSH/"
                    move_class = 5
                elif criteria["KINGMOVE"]:
                    directory = "chessdataset/train/KINGMOVE/"
                    labelname = "KINGMOVE/"
                    move_class = 6
                else:
                    directory = "chessdataset/train/DEVELOPE/"
                    labelname = "DEVELOPE/"
                    move_class = 7
                
                filename = directory + "position"+ str(i) +".txt"
                labelname = labelname + "position"+ str(i) + ".txt"
                pos_file = open(filename, "w+")
                print(filename + ',', move_class, file = labels)
                for r in position:
                    print(r, file = pos_file)
                # print(criteria)
                pos_file.close()
            game = chess.pgn.read_game(pgn)
    return True
    

l_csv_train = "chess_labels_train.csv"
l_csv_test = "chess_labels_test.csv"
create_classify_file("chess_com_games_2021-04-24.pgn", l_csv_train)    
create_classify_file("chess_com_games_2021-04-24.pgn", l_csv_test, True)  
    
