from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd


def get_team_id(fullName):
    team_dict = teams.get_teams()
    team = [x for x in team_dict if x['full_name'] == fullName][0]
    team_id = team['id']
    return(team_id)


def get_roster(team_id='', teamName='', season='2022'):
    if team_id == '':
        team_id = get_team_id(teamName)
    df = commonteamroster.CommonTeamRoster(season=season, team_id=team_id).get_data_frames()
    df = df[0]
    rosterDict = {}
    for i in range(len(df)):
        rosterDict[df["PLAYER"][i]] = df["PLAYER_ID"][i]
    return(rosterDict)


def excel_write(writer, df, sheetname=''):
    if sheetname != '':
        df.to_excel(writer, sheet_name=sheetname)
    else:
        df.to_excel(writer)
        
        
if __name__ == "__main__":
    writer = pd.ExcelWriter('teamRosters.xlsx', engine='xlsxwriter')
    team_list = teams.get_teams()
    for i in range(30):
        team = team_list[i]['full_name']
        id = team_list[i]['id']
        dict = get_roster(id)
        df = pd.DataFrame.from_dict(dict)
        excel_write(writer, df, team)
        writer.save()
        