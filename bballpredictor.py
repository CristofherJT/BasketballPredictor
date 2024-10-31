#Data manipulation library
import pandas as pd

#Will download nba_api to device
import os
#os.system(f"{os.sys.executable} -m pip install nba_api")

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


#Function will get player data over multiple seasons
def get_player_data(player_id, seasons):
    all_data = []

    for season in seasons:
        game_logs = playergamelog.PlayerGameLog(player_id = player_id, season = season)
        game_data_df = game_logs.get_data_frames()[0]
        #Drops unnecessary data
        game_data_df.drop(['Player_ID','Game_ID','GAME_DATE','VIDEO_AVAILABLE'], axis = 1, inplace=True)
        all_data.append(game_data_df)

    combine_data = pd.concat(all_data, ignore_index = True)

    return combine_data

player_list = players.get_active_players()

playerIn = input('Name a current NBA player: ')

player = [player for player in player_list if player['full_name'] == playerIn][0]
playerID = player['id']
seasons = ['2021-22', '2022-23', '2023-24', '2024-25']

print(get_player_data(playerID, seasons))