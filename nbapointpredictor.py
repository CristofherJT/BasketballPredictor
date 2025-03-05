import os
#Will download needed libraries
#os.system(f"{os.sys.executable} -m pip install nba_api")
#os.system(f"{os.sys.executable} -m pip install scikit-learn")
#os.system(f"{os.sys.executable} -m pip install pandas")

#Data manipulation library
import pandas as pd

from nba_api.stats.endpoints import playergamelog, leaguedashteamstats
from nba_api.stats.static import players, teams
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

#Function will get player data over multiple seasons
def get_player_data(player_id, seasons):
    all_data = []

    for season in seasons:
        game_logs = playergamelog.PlayerGameLog(player_id = player_id, season = season).get_data_frames()[0]
        all_data.append(game_logs)

    #Combines the data into one dataframe
    combine_data = pd.concat(all_data, ignore_index = True)

    return combine_data

#Function will get team defense stats
def get_team_data(seasons):
    team_defense_data = []

    for season in seasons:
        defense_logs = leaguedashteamstats.LeagueDashTeamStats(season = season, measure_type_detailed_defense = 'Defense').get_data_frames()[0]
        defense_logs.drop(['TEAM_NAME','GP','W','L','W_PCT'], axis = 1, inplace=True)
        team_defense_data.append(defense_logs)

    #Combines the data into one dataframe
    combined_defense_data = pd.concat(team_defense_data, ignore_index = True)

    return combined_defense_data


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

#Calls the functions to get the data
player_data = get_player_data(playerID, seasons)
combined_defense_data = get_team_data(seasons)

#Filters for the specific team data
#team_defensive_stats = combined_defense_data[combined_defense_data['TEAM_ID'] == teamID]
#Merges all relevant data for the model
#all_data = player_data.merge(team_defensive_stats)

features = ['MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT']

#Assigns X and y to the appropriate data sets
X = player_data[features]
y = player_data['PTS']

#Trains the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)    
model.fit(X_train, y_train)
point_prediction = model.predict(X_test)

print(f"I predict that {playerIn} will score {point_prediction[0]:.0f} points against the {teamIn} tonight.")
