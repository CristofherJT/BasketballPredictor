#Data manipulation library
import pandas as pd

#Will download nba_api to device
import os
#os.system(f"{os.sys.executable} -m pip install nba_api")

from nba_api.stats.endpoints import playergamelog, leaguedashteamstats
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
        defense_logs = leaguedashteamstats.LeagueDashTeamStats(season = season, measure_type_detailed_defense = 'Defense').get_data_frames()[0]
        team_defense_data.append(defense_logs)

    combined_defense_data = pd.concat(team_defense_data, ignore_index = True)

    return combined_defense_data

def get_shot_defense_data(seasons):
    shot_defense_data = []

    for season in seasons:
        shot_defense_logs = 
        shot_defense_data.append(shot_defense_logs)

    combined_shot_data = pd.concat(shot_defense_data, ignore_index = True)

    return combined_shot_data

seasons = ['2021-22', '2022-23', '2023-24', '2024-25']
player_list = players.get_active_players()

playerIn = input('Name a current NBA player by their full name: ')
teamIn = input('What team is the player playing against: ')

#Will search for players by their full name
player = players.find_players_by_full_name(playerIn)[0]
playerID = player['id']

#Will search for teams by the full name
team = teams.find_teams_by_full_name(teamIn)[0]
teamID = team['id']

#Calls the function for the defensive data of all teams
combined_defense_data = get_team_defensive_data(seasons)

#Filters for the specific team's defensive data
team_defensive_stats = combined_defense_data[combined_defense_data['TEAM_ID'] == teamID]



