from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import datetime
player_dict = players.get_players()

# Use ternary operator or write function 
# Names are case sensitive

def get_player_id(fullName):
    player_dict = players.get_players()
    data = [player for player in player_dict if player['full_name'] == fullName][0]
    id = data["id"]
    return(id)

def get_player_gamelog(id, season='2022'):
    gamelog = playergamelog.PlayerGameLog(player_id=id, season = season)
    dfgamelog = gamelog.get_data_frames()
    return(dfgamelog[0])

def get_team_id(fullName):
    team_dict = teams.get_teams()
    team = [x for x in team_dict if x['full_name'] == fullName][0]
    team_id = team['id']
    return(team_id)

def get_dates():
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return(today, yesterday)

def get_gamelog(date, season='2022'):
    gamelog = leaguegamelog.LeagueGameLog(season=season)
    df = pd.DataFrame((gamelog.get_data_frames())[0])
    dfdate = df[df["GAME_DATE"] == str(date)]
    return(dfdate)

# def get_allplayers():
#     df = pd.DataFrame(players.get_players())
#     df.drop(df[(df['is_active'] == False)].index, inplace=True)
#     df.drop('is_active', axis=1, inplace=True)
#     return(df)

def get_roster(team_id, season='2022'):
    df = commonteamroster.CommonTeamRoster(season = season, team_id = team_id).get_data_frames()
    df = df[0]
    rosterDict = {}
    for i in range(len(df)):
        rosterDict[df["PLAYER"][i]] = df["PLAYER_ID"][i]
    return(rosterDict)
    

if __name__ == "__main__":
    roster = get_roster(get_team_id('Toronto Raptors'))
    for name, playerid in roster.items():
        print(name)
        print(get_player_gamelog(playerid))