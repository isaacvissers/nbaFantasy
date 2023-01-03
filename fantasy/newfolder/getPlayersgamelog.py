from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd


def get_player_id(fullName):
    """Returns the id for a given player when given their full name."""
    player_dict = players.get_players()
    data = [player for player in player_dict if player['full_name'] == fullName][0]
    id = data["id"]
    return(id)


def get_player_gamelog(fullName, season='2022'):
    """returns a players complete gamelog for the season"""
    id = get_player_id(fullName)
    gamelog = playergamelog.PlayerGameLog(player_id=id, season = season)
    df = gamelog.get_data_frames()
    df1 = df[0]
    df1.drop('SEASON_ID', axis=1, inplace=True)
    df1.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    return(df1)


def excel_write(writer, df, sheetname=''):
    if sheetname != '':
        df.to_excel(writer, sheet_name=sheetname)
    else:
        df.to_excel(writer)


if __name__ == "__main__":
        myTeamRoster = [
        'Kevin Porter Jr.',
        'Jalen Brunson',
        'Jayson Tatum',
        'Pascal Siakam',
        'Ivica Zubac',
        'Terry Rozier',
        'John Collins',
        'Deandre Ayton',
        'Jordan Clarkson',
        'Jamal Murray',
        'D\'Angelo Russell',
        'Andrew Nembhard',
        'Jakob Poeltl',
        'RJ Barrett'
        ]
        writer = pd.ExcelWriter('playerGamelog.xlsx', engine='xlsxwriter')
        for name in myTeamRoster:
            df = get_player_gamelog(name)
            excel_write(writer, df, name)
        writer.save()
        