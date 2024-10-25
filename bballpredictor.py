#Data manipulation library
import pandas as pd
#Lets us create and work with arrays of data
import numpy as np

#Will download nba_api to device
import os
#os.system(f"{os.sys.executable} -m pip install nba_api")

from nba_api.stats.endpoints import playergamelog, commonallplayers
from nba_api.stats.static import players

all_players = commonallplayers.CommonAllPlayers()
players_df = all_players.get_data_frames()[0]

#Function will get player data over multiple seasons
def get_player_data(player_id, seasons):
    all_data = []

    for season in seasons:
        game_logs = playergamelog.PlayerGameLog(player_id = player_id, season = season)
        game_data_df = game_logs.get_data_frames()[0]
        #Drops unnecessary data
        game_data_df.drop(['Game_ID','VIDEO_AVAILABLE'], axis = 1, inplace=True)
        all_data.append(game_data_df)

    combine_data = pd.concat(all_data, ignore_index = True)

    return combine_data

playerID = '2544'
seasons = ['2021-22', '2022-23', '2023-24']

print(get_player_data(playerID, seasons))