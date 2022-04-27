# -*- coding: utf-8 -*-
"""
Created on Thu May  6 18:48:25 2021

@author: Desmond
"""

import chess
import chess.pgn
import os

i = 0
j= 0

input_file = "./unprocesseddata/chess_com_games_2022-04-24.pgn"
output_file = "guillo-krapidgamestrain190.pgn"
pgn = open(input_file, "r")
processed_pgn = open(output_file, "w")
game = chess.pgn.read_game(pgn)
while(game):
    # if (not('?' in game.headers["WhiteElo"]) and not('?' in game.headers["BlackElo"])):
        # if ((int(game.headers["WhiteElo"]) > 1399) and (int(game.headers["WhiteElo"]) < 1701))\
        #     and ((int(game.headers["BlackElo"]) > 1399) and (int(game.headers["BlackElo"]) < 1701))\
        #         and game.headers["TimeControl"] == "600+0" or game.headers["TimeControl"] == "600+5":
    i+=1
    print(game, file = processed_pgn, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if i >= 189:
        break
processed_pgn.close()



output_file2 = "guillo-krapidgamestest48.pgn"
processed_pgn2 = open(output_file2, "w")
game = chess.pgn.read_game(pgn)
while(game):

    # if (not('?' in game.headers["WhiteElo"]) and not('?' in game.headers["BlackElo"])):
        # if ((int(game.headers["WhiteElo"]) > 1300) and (int(game.headers["WhiteElo"]) < 1701))\
        #     and ((int(game.headers["BlackElo"]) > 1300) and (int(game.headers["BlackElo"]) < 1701))\
        #         and game.headers["TimeControl"] == "600+0" or game.headers["TimeControl"] == "600+5":
    j+=1
    print(game, file = processed_pgn2, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if j >= 47:
        break
processed_pgn2.close()


pgn.close()