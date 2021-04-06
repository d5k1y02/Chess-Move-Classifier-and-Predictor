# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:00:53 2021

@author: Desmond Yancey
"""

"""This is a classification algorithm for chess moves. Given a position in array format, 
it will determine if a chosen move meets a variety of criteria.
notation is as follows: k = king, q = queen, n = knight, b = bishop,r = rook and p = pawn"""



    
"""converts chess fen format to an array in the format board[coord1][coord2] = (piece, color)"""    

from collections import Counter

def fen_to_array():
    
    board = [[('e', 'e') for i in range(8)] for j in range(8)] #board[coord1][coord2] = (piece, color)
    return board

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
        pos = position[in_piece[0]+i][in_piece[1]-i]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0]+i,in_piece[1]-i,pos[0],pos[1]))
            break
        
    for i in range(min((8-in_piece[0]), in_piece[1])): #down-left
        pos = position[in_piece[0]-i][in_piece[1]-i]
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
        if in_piece[1] <= 6:
            pos = position[in_piece[0]-1][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[1] >= 1:
            pos = position[in_piece[0]-1][in_piece[1]-1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]-1,in_piece[1]-1,pos[0],pos[1]))
                
    if color == 'b': #if color is black, look downward
        if in_piece[1] <= 6:
            pos = position[in_piece[0]+1][in_piece[1]+1]
            if  pos != ('e','e'):
                piece_list.append((in_piece[0]+1,in_piece[1]+1,pos[0],pos[1]))
        if in_piece[1] >= 1:
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
    if in_piece[1] >= 1: #right
        pos = position[in_piece[0]][in_piece[1]+1]
        if  pos != ('e','e'):
            piece_list.append((in_piece[0],in_piece[1]+1,pos[0],pos[1]))
    if in_piece[1] <= 6: #left
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
            pieces_seen = pawn_vision(position, piece)
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
            pieces_seen.extend(pawn_vision(position, piece))
        
        elif piece[2] == 'k':
            pieces_seen.extend(king_vision(position, piece))
            
            need to delete friendly pieces
            
        pre_move_counter = Counter(pieces_seen)  
        
        position[move[2]][move[3]] = position[move[0]][move[1]] #make the move
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
            pieces_seen.extend(pawn_vision(position, piece))
        
        elif piece[2] == 'k':
            pieces_seen.extend(king_vision(position, piece))
                
        post_move_counter = Counter(pieces_seen) 
    
    diff = post_move_counter - pre_move_counter
    if diff != Counter():
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
    temp_list = pawn_vision(position, input_piece)
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
    attacked_list = []
    for i in range(8):
        for j in range(8):
            if is_piece_attacked(position, move, (i, j, position[i][j][0])):
                attacked_list.append((i, j, position[i][j][0]))
    pieces_seen = []
    p = (move[2], move[3], position[move[0], move[1]][0])
    if p[2] == 'q':
        pieces_seen = diag_vision(position, p) + straight_vision(position, p)
    elif p[2] == 'r':
        pieces_seen.extend(straight_vision(position, p))
    
    elif p[2] == 'n':
        pieces_seen.extend(knight_vision(position, p))
     
    elif p[2] == 'b':
        pieces_seen.extend(diag_vision(position, p))
        
    elif p[2] == 'p':
        pieces_seen.extend(pawn_vision(position, p))
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

def is_promotion(position, move): #does move promote a pawn

    color = position[move[0]][move[1]][1] #color of player whose turn it is
    opp_color = 'w'
    if color == 'w':
        opp_color = 'b'
    if position[move[0]][move[1]][0] == 'p':
        
        if color == 'w': #if color is white, look upward
            if in_piece[0] == 1:
                return True
                    
        elif color == 'b': #if color is black, look downward
            if in_piece[0] == 6:
                return True
               

""" accepts a position in the array format created by fen_to_array and a move tuple 
(pos1l,pos1n,pos2l,pos2n) and returns a dictionary of classifications that apply to that move"""
def move_classifier(position, move):
    
    criteria = {}                 #define criteria-this may grow as needed
    criteria["DEVELOPE"].append(is_developing(position, move))
    criteria["CHECK"].append(is_check(position, move))
    criteria["ATTACK"].append(is_attack(position, move))
    criteria["CAPTURE"].append(is_capture(position, move))
    criteria["DEFEND"].append(is_defense(position, move))
    criteria["RETREAT"].append(is_retreat(position, move))
    criteria["PROMOTE"].append(is_promotion(position, move))
    
    return criteria

