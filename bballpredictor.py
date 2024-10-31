#Data manipulation library
import pandas as pd

#Will download nba_api to device
import os
#os.system(f"{os.sys.executable} -m pip install nba_api")

from nba_api.stats.endpoints import playergamelog, leaguedashteamstats, teamdashptshots
from nba_api.stats.static import players, teams


#Function will get player data over multiple seasons
def get_player_data(player_id, seasons):
    all_data = []

    for season in seasons:
        game_logs = playergamelog.PlayerGameLog(player_id = player_id, season = season).get_data_frames()[0]
        #Drops unnecessary data
        game_logs.drop(['Player_ID','Game_ID','GAME_DATE','VIDEO_AVAILABLE'], axis = 1, inplace=True)
        all_data.append(game_logs)

    combine_data = pd.concat(all_data, ignore_index = True)

    return combine_data

def get_team_defensive_data(seasons):
    team_defense_data = []

    for season in seasons:
        defense_logs = leaguedashteamstats.LeagueDashTeamStats(team_id = team_id, season = season, measure_type_detailed_defense = 'Defense').get_data_frames()[0]
        team_defense_data.append(defense_logs)

    combined_defense_data = pd.concat(team_defense_data, ignore_index = True)

    return combined_defense_data


seasons = ['2021-22', '2022-23', '2023-24', '2024-25']
player_list = players.get_active_players()

playerIn = input('Name a current NBA player by their full name: ')
teamIn = input('What team is the player playing against?: ')

#Will look through active roster in search of the input
player = [player for player in player_list if player['full_name'] == playerIn][0]
playerID = player['id']

team = teams.find_teams_by_full_name('teamIn')
print(team)

print(get_team_defensive_data(seasons))