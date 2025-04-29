import os
import subprocess

def install(package):
    try:
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")

try:
    import nba_api
except ImportError:
    install("nba_api")

try:
    import pandas
except ImportError:
    install("pandas")

try:
    import sklearn
except ImportError:
    install("scikit-learn")

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
        #Will filter for the specific team
        filtered_logs = game_logs[game_logs['MATCHUP'].str.contains(teamABR, case=False)].copy()

        all_data.append(filtered_logs)

    #Combines the data into one dataframe
    combine_data = pd.concat(all_data, ignore_index = True)

    return combine_data

seasons = ['2021-22', '2022-23', '2023-24', '2024-25']
inUse = True

while inUse:
    playerIn = input('Name a current NBA player by their full name: ')
    teamIn = input('What team is the player playing against: ')

    #Will search for players by their full name
    player = players.find_players_by_full_name(playerIn)[0]
    playerID = player['id']

    #Will search for teams by the full name
    team = teams.find_teams_by_full_name(teamIn)[0]
    teamID = team['id']
    teamABR = team['abbreviation']

    #Calls the functions to get the data
    player_data = get_player_data(playerID, seasons)

    features = ['MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT']

    #Assigns X and y to the appropriate data sets
    X = player_data[features]
    y = player_data['PTS']

    #Trains the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    model = RandomForestRegressor(n_estimators=35, random_state=42)    
    model.fit(X_train, y_train)
    point_prediction = model.predict(X_test)

    print(f"I predict that {playerIn} will score {point_prediction[0]:.0f} points against the {teamIn} tonight.")
    
    userCho = input('Would you like to predict another player? (y/n): ')

    if userCho.lower() == 'n':
        inUse = False
        print('Thanks for using the program!')
