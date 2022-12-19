from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import datetime


def get_player_id(fullName):
    player_dict = players.get_players()
    data = [player for player in player_dict if player['full_name'] == fullName][0]
    id = data["id"]
    return(id)

def get_player_gamelog(id, season='2022'):
    gamelog = playergamelog.PlayerGameLog(player_id=id, season = season)
    df = gamelog.get_data_frames()
    df1 = df[0]
    df1.drop('SEASON_ID', axis=1, inplace=True)
    df1.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    return(df1)

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
    df.drop('SEASON_ID', axis=1, inplace=True)
    df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    dfdate = df[df["GAME_DATE"] == str(date)]
    return(dfdate)

def get_roster(team_id, season='2022'):
    df = commonteamroster.CommonTeamRoster(season = season, team_id = team_id).get_data_frames()
    df = df[0]
    rosterDict = {}
    for i in range(len(df)):
        rosterDict[df["PLAYER"][i]] = df["PLAYER_ID"][i]
    return(rosterDict)

def calculate_fantasy_points(df, row=0):
    fantasyPts = df['PTS'][row] + df['AST'][row]*1.5 + df['REB'][row]*1.2 + df['STL'][row]*2 + df['BLK'][row]*2 + df['FG3M'][row]*0.5 - df['TOV'][row]
    return(fantasyPts)

def excel_write(df, filename, sheetname=''):
    writer = pd.ExcelWriter(filename+'.xlsx', engine='xlsxwriter')
    if sheetname != '':
        df.to_excel(writer, sheet_name = sheetname)
        writer.save()
        writer.close()
    else:
        df.to_excel(writer)
        writer.save()
        writer.close()
        
def add_fantasy_row(df):
    fpts = []
    for i in range(len(df)):
        fpts.append(calculate_fantasy_points(df, i))
    df["FPTS"] = fpts
    return(df)
        

if __name__ == "__main__":
    today, yesterday = get_dates()
    todaysGames = get_gamelog(yesterday)
    print(todaysGames)
    for teamid in todaysGames["TEAM_ID"]:
        roster = get_roster(teamid)
        for name, playerid in roster.items():
            print(name)
            df = get_player_gamelog(playerid)
            print(df)
            add_fantasy_row(df)
            print(df)
            quit()
            # yesterdayString = yesterday.strftime('%b').upper() + ' ' +  str(yesterday.day) + ', ' + str(yesterday.year)
            # yesterdayStats = df[df["GAME_DATE"] == yesterdayString]
            # # exit()
            # if df["GAME_DATE"][0] == yesterdayString:
            #     df1 = df[df['GAME_DATE'] == str(yesterdayString)]
            #     print(calculate_fantasy_points(df1))
            #     print(df1)
            #     exit()