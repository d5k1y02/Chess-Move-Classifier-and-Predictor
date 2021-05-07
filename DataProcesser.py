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

input_file = "./unprocesseddata/lichess_db_standard_rated_2021-04.pgn"
output_file = "1000-1200EloGamesTrainingSet10000.pgn"
pgn = open(input_file, "r")
processed_pgn = open(output_file, "w")
game = chess.pgn.read_game(pgn)
while(game):

    if ((int(game.headers["WhiteElo"]) > 999) and (int(game.headers["WhiteElo"]) < 1201))\
        and ((int(game.headers["BlackElo"]) > 999) and (int(game.headers["BlackElo"]) < 1201))\
            and game.headers["Event"] != "Rated Bullet game":
            i+=1
            print(game, file = processed_pgn, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if i >= 9999:
        break
processed_pgn.close()



output_file2 = "1000-1200EloGamesTestSet5000.pgn"
processed_pgn2 = open(output_file2, "w")
game = chess.pgn.read_game(pgn)
while(game):

    if ((int(game.headers["WhiteElo"]) > 999) and (int(game.headers["WhiteElo"]) < 1201))\
        and ((int(game.headers["BlackElo"]) > 999) and (int(game.headers["BlackElo"]) < 1201))\
            and game.headers["Event"] != "Rated Bullet game":
            j+=1
            print(game, file = processed_pgn2, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if j >= 2999:
        break
processed_pgn2.close()


pgn.close()