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

input_file = "./unprocesseddata/lichess_db_standard_rated_2014-09.pgn"
output_file = "1000-1200EloRapidGamesTrainingSet1000.pgn"
pgn = open(input_file, "r")
processed_pgn = open(output_file, "w")
game = chess.pgn.read_game(pgn)
while(game):
    if (not('?' in game.headers["WhiteElo"]) and not('?' in game.headers["BlackElo"])):
        if ((int(game.headers["WhiteElo"]) > 999) and (int(game.headers["WhiteElo"]) < 1201))\
            and ((int(game.headers["BlackElo"]) > 999) and (int(game.headers["BlackElo"]) < 1201))\
                and game.headers["TimeControl"] == "600+0" or game.headers["TimeControl"] == "600+5":
                i+=1
                print(game, file = processed_pgn, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if i >= 999:
        break
processed_pgn.close()



output_file2 = "1000-1200EloRapidGamesTestSet500.pgn"
processed_pgn2 = open(output_file2, "w")
game = chess.pgn.read_game(pgn)
while(game):

    if (not('?' in game.headers["WhiteElo"]) and not('?' in game.headers["BlackElo"])):
        if ((int(game.headers["WhiteElo"]) > 999) and (int(game.headers["WhiteElo"]) < 1201))\
            and ((int(game.headers["BlackElo"]) > 999) and (int(game.headers["BlackElo"]) < 1201))\
                and game.headers["TimeControl"] == "600+0" or game.headers["TimeControl"] == "600+5":
                j+=1
                print(game, file = processed_pgn2, end = "\n\n")
            
    game = chess.pgn.read_game(pgn)
    if j >= 499:
        break
processed_pgn2.close()


pgn.close()