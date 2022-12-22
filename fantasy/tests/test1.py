from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import datetime


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

def get_team_id(fullName):
    team_dict = teams.get_teams()
    team = [x for x in team_dict if x['full_name'] == fullName][0]
    team_id = team['id']
    return(team_id)

def get_dates():
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterdayString = yesterday.strftime('%b').upper() + ' ' +  str(yesterday.day) + ', ' + str(yesterday.year)
    todayString = today.strftime('%b').upper() + ' ' +  str(today.day) + ', ' + str(today.year)
    return(today, yesterday, todayString, yesterdayString)

def get_gamelog(date, season='2022'):
    gamelog = leaguegamelog.LeagueGameLog(season=season)
    df = pd.DataFrame((gamelog.get_data_frames())[0])
    df.drop('SEASON_ID', axis=1, inplace=True)
    df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    dfdate = df[df["GAME_DATE"] == str(date)]
    return(dfdate)

def get_roster(team_id='', teamName='', season='2022'):
    if team_id == '':
        team_id = get_team_id(teamName)
    df = commonteamroster.CommonTeamRoster(season = season, team_id = team_id).get_data_frames()
    df = df[0]
    rosterDict = {}
    for i in range(len(df)):
        rosterDict[df["PLAYER"][i]] = df["PLAYER_ID"][i]
    return(rosterDict)

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
 


class Team():
    def __init__(self, roster, date):
        self.roster = roster
        self.date = date
        self.gamelog = {}
        self.av_fpoints = {}
        for player in self.roster:
            self.gamelog[player] = get_player_gamelog(player)
        for name, df in self.gamelog.items():
            self.add_fantasy_row(df)
            self.av_fpoints[name] = self.average_fpoints(df)
        self.fantasy_points_by_date(date)
        # self.check_if_injured(self)
            
    def printfn(self):
        for name, df in self.gamelog.items():
            print(name)
            print(df)
        print(self.av_fpoints)
        print(self.fptsatdate)
            
    def average_fpoints(self, df):
        fpoints = sum(df['FPTS']) / len(df)
        fpoints = round(fpoints, 2)
        return(fpoints)
    
    def add_fantasy_row(self,df):
        fpts = []
        for i in range(len(df)):
            fpts.append(self.calculate_fantasy_points(df, i))
        df["FPTS"] = fpts
        return(df)
    
    def fantasy_points_by_date(self, date):
        self.fptsatdate = {}
        for name, df in self.gamelog.items():
            dfDate = df[df['GAME_DATE'] == date]
            if 'FPTS' in dfDate:
                try:
                    x = (float(dfDate['FPTS']))
                    x = round(x,1)
                except TypeError:
                    x = ('DNP')
            else:
                x = (False)
            self.fptsatdate[name] = x
        return(self)
    
    def print_results(self):
        """Prints teams results for today compared with the expected(average)"""
        print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format('NAME', 'TODAY', 'AVEREAGE', 'DIFFERENCE'))
        total = 0
        totalav = 0
        totaldiff = 0
        for name in myTeam.roster:
            today = self.fptsatdate[name]
            average = self.av_fpoints[name]
            if today != 'DNP' and today != 'INJURED':
                difference = today-average
                difference = round(difference, 2)
                total += today
                totalav += average
                totaldiff += difference
                if difference > 0:
                    difference = '+' + str(difference)
            else:
                difference = '-'
            print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format(name, today, average, difference))
        total = round(total,1)
        totalav = round(totalav,2)
        totaldiff = round(totaldiff,2)
        if totaldiff > 0:
                    totaldiff = '+' + str(totaldiff)
        print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format('TOTALS', total, totalav, totaldiff))
        
    def calculate_fantasy_points(self, df, row=0):
        fantasyPts = df['PTS'][row] + df['AST'][row]*1.5 + df['REB'][row]*1.2 + df['STL'][row]*2 + df['BLK'][row]*2 + df['FG3M'][row]*0.5 - df['TOV'][row]
        return(fantasyPts)

    def check_if_injured(self):
        gamelog = get_gamelog(yesterday)
        for team in gamelog['TEAM_NAME']:
            roster = get_roster(teamName = team)
            for player in myroster:
                if player in roster & self.fptsatdate[player] == 'DNP':
                    self.fptsatdate[player] = 'INJURED'

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
    
    today, yesterday, todayString, yesterdayString = get_dates()
    myTeam = Team(myTeamRoster, yesterdayString)

    # myTeam.printfn()
    myTeam.print_results()
    myroster = myTeam.roster
    # print(myTeam.roster)
    # league_roster = {}
    # teamlist = []
    # for team in teams.get_teams():
    #     teamlist.append(team['full_name'])
    # for team in teamlist:
    #     league_roster[team] = get_roster(teamName=team)
    # print(league_roster)
        
    
    # # Need to add 
    # myTeamGamelog = {}
    # for player in myTeam:
    #     myTeamGamelog[player] = get_player_gamelog(player)
    # print(myTeamGamelog)
    
    
    
    
    
    
    # today, yesterday, todayString, yesterdayString = get_dates()
    # todaysGames = get_gamelog(yesterday)
    # print(todaysGames)
    # for team_id in todaysGames["TEAM_ID"]:
    #     roster = get_roster(team_id=team_id)
    #     for name, playerid in roster.items():
    #         print(name)
    #         df = get_player_gamelog(name)
    #         print(df)
    #         add_fantasy_row(df)
    #         print(df)
    #         x = fantasy_points_by_date(df,yesterdayString)
    #         print(x)
    #         quit()
            
            
            
            
            # yesterdayString = yesterday.strftime('%b').upper() + ' ' +  str(yesterday.day) + ', ' + str(yesterday.year)
            # yesterdayStats = df[df["GAME_DATE"] == yesterdayString]
            # # exit()
            # if df["GAME_DATE"][0] == yesterdayString:
            #     df1 = df[df['GAME_DATE'] == str(yesterdayString)]
            #     print(calculate_fantasy_points(df1))
            #     print(df1)
            #     exit()