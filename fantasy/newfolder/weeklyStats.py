from dailyStats import *

if __name__ == "__main__":
    weekString = [
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
    weeklyStats = []
    for i in range(7):
        x = Team(myTeamRoster, weekString[i], weekDates[i])
        print(x)
        # weeklyStats[weekString[i]].print_results()
        
    # today, yesterday, todayString, yesterdayString = get_dates()
    # myTeam = Team(myTeamRoster, 'DEC 30, 2022', '2022-12-30')
    # myTeam.print_results()
    # myroster = myTeam.roster
