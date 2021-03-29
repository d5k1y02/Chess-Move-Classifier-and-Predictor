# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:00:53 2021

@author: Desmond Yancey
"""

"""This is a classification algorithm for chess moves. Given a position in array format, 
it will determine if a chosen move meets a variety of criteria.
notation is as follows: k = king, q = queen, n = knight, b = bishop,r = rook and p = pawn"""



    
"""converts chess fen format to an array in the format board[coord1][coord2] = (piece, color)"""    
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
        
    return piece_list

def is_check(position, move): #is move a check

    position[move[2]][move[3]] = position[move[0]][move[1]] #make the move before checking if there are any checks
    position[move[0]][move[1]] = ('e','e')
    
    color = position[move[0]][move[1]][1] #color of player whose turn it is
    piece_list = [] #(pos1,pos2,piece)
    enemy_king_pos = (0,0)
    
    for i in range(8):
        for j in range(8):
            if position[i][j][1] == color:
                piece_list.append((i, j, position[i][j][0])) #add every friendly piece to the list
            else:
                if position[i][j][0] == 'k':
                    enemy_king_pos = (i,j)
    for piece in piece_list:
        if piece[2] == 'q':
            return True
        elif piece[2] == 'r':
            return True
        elif piece[2] == 'n':
            return True
        elif piece[2] == 'b':
            return True
        elif piece[2] == 'p':
            return True
    return False

def is_attack(position, move): #does move attack a piece
    return False

def is_capture(position, move): #is move a capture
    return False

def is_defense(position, move): #does move defend a piece or pawn under attack
    return False

def is_retreat(position, move): #does move retreat an attacked piece
    return False

def is_promotion(position, move): #does move retreat an attacked piece
    return False

""" accepts a position in the array format created by fen_to_array and a move tuple 
(pos1l,pos1n,pos2l,pos2n) and returns a dictionary of classifications that apply to that move"""
def move_classifier(position, move):
    
    criteria = {}                       #define criteria-this may grow as needed
    criteria["DEVELOPE"].append(is_developing(position, move))
    criteria["CHECK"].append(is_check(position, move))
    criteria["ATTACK"].append(is_attack(position, move))
    criteria["CAPTURE"].append(is_capture(position, move))
    criteria["DEFEND"].append(is_defense(position, move))
    criteria["RETREAT"].append(is_retreat(position, move))
    criteria["PROMOTE"].append(is_promotion(position, move))
    
    return criteria

