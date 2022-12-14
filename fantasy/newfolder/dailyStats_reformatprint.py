from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
import datetime



# def get_player_id(fullName):
#     """Returns the id for a given player when given their full name."""
#     player_dict = players.get_players()
#     data = [player for player in player_dict if player['full_name'] == fullName][0]
#     id = data["id"]
#     return(id)

def get_player_gamelog(fullName, season='2022'):
    """returns a players complete gamelog for the season"""
    df = pd.read_excel('playerGamelog.xlsx', sheet_name=fullName)
    return(df)

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
    df = pd.read_excel('dailyGamelog.xlsx', sheet_name=date)
    # gamelog = leaguegamelog.LeagueGameLog(season=season)
    # df = pd.DataFrame((gamelog.get_data_frames())[0])
    return(df)

def get_roster(team_id='', teamName='', season='2022'):
    if team_id == '':
        team_id = get_team_id(teamName)
    df = commonteamroster.CommonTeamRoster(season=season, team_id=team_id).get_data_frames()
    df = df[0]
    rosterDict = {}
    for i in range(len(df)):
        rosterDict[df["PLAYER"][i]] = df["PLAYER_ID"][i]
    return(rosterDict)


class Team():
    def __init__(self, roster, strdate, date):
        self.roster = roster
        self.date = date
        self.strdate = strdate
        self.gamelog = {}
        self.av_fpoints = {}
        for player in self.roster:
            self.gamelog[player] = get_player_gamelog(player)
        for name, df in self.gamelog.items():
            self.add_fantasy_row(df)
            self.av_fpoints[name] = self.average_fpoints(df)
        self.fantasy_points_by_date()
        self.check_if_injured()
            
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
    
    def fantasy_points_by_date(self):
        self.fptsatdate = {}
        for name, df in self.gamelog.items():
            dfDate = df[df['GAME_DATE'] == self.strdate]
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
        print('-'*65)
        total = 0
        totalav = 0
        totaldiff = 0
        for name in self.roster:
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
        print('-'*65)
        print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format('TOTALS', total, totalav, totaldiff))
        print('-'*65)
        print()
        print()
        
    def calculate_fantasy_points(self, df, row=0):
        fantasyPts = df['PTS'][row] + df['AST'][row]*1.5 + df['REB'][row]*1.2 + df['STL'][row]*2 + df['BLK'][row]*2 + df['FG3M'][row]*0.5 - df['TOV'][row]
        return(fantasyPts)

    def check_if_injured(self):
        gamelog = get_gamelog(self.date)
        for team in gamelog['TEAM_ID']:
            rosterTeam = get_roster(team_id=team)
            for player in self.roster:
                if player in rosterTeam.keys():
                    if self.fptsatdate[player] == 'DNP':
                        self.fptsatdate[player] = 'INJURED'
        return(self)
    
class Week():
    def __init__(self, roster, dates, stringDates):
        self.days = {}
        self.strDates = stringDates
        self.roster = roster
        for i in range(7):
            self.days[stringDates[i]] = Team(roster, stringDates[i], dates[i])
            
    def print_results(self):
        """Prints teams results for today compared with the expected(average)"""
        print('{0:^20}|{1:^15}|{2:^15}|{3:^15}|{4:^15}|{5:^15}|{6:^15}|{7:^15}|{8:^15}|{9:^15}'.format('NAME', 'AVEREAGE', self.strDates[0], self.strDates[1], self.strDates[2], self.strDates[3], self.strDates[4], self.strDates[5], self.strDates[6], 'DIFFERENCE'))
        print('-'*155)
        dailyTotal = {}
        for day in self.strDates:
            dailyTotal[day] = 0
        for name in self.roster:
            print('{0:20}'.format(name), end='|')
            for day in self.strDates:
                print('{15:0}'.format(self.days[day].fptsatdate[name]), end='|')
                print()
                dailyTotal[day] += self.days[day].fptsatdate[name]
            
            
        # for name in self.roster:
        #     today = self.fptsatdate[name]
        #     average = self.av_fpoints[name]
        #     if today != 'DNP' and today != 'INJURED':
        #         difference = today-average
        #         difference = round(difference, 2)
        #         total += today
        #         totalav += average
        #         totaldiff += difference
        #         if difference > 0:
        #             difference = '+' + str(difference)
        #     else:
        #         difference = '-'
        #     print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format(name, today, average, difference))
        # total = round(total,1)
        # totalav = round(totalav,2)
        # totaldiff = round(totaldiff,2)
        # if totaldiff > 0:
        #             totaldiff = '+' + str(totaldiff)
        # print('-'*65)
        # print('{0:^20}|{1:^15}|{2:^15}|{3:^15}'.format('TOTALS', total, totalav, totaldiff))
        # print('-'*65)
        # print()
        # print()
        

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
    weekString = [ # will need to find a way to get these strings
        "DEC 19, 2022",
        "DEC 20, 2022",
        "DEC 21, 2022",
        "DEC 22, 2022",
        "DEC 23, 2022",
        "DEC 24, 2022",
        "DEC 25, 2022"
    ]
    weekDates = [
        "2022-12-19",
        "2022-12-20",
        "2022-12-21",
        "2022-12-22",
        "2022-12-23",
        "2022-12-24",
        "2022-12-25"
    ]
    
    week = Week(myTeamRoster, weekDates, weekString)
    week.print_results()