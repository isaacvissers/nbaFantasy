from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import datetime

def get_gamelog(date, season='2022'):
    gamelog = leaguegamelog.LeagueGameLog(season=season)
    df = pd.DataFrame((gamelog.get_data_frames())[0])
    df.drop('SEASON_ID', axis=1, inplace=True)
    df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    dfdate = df[df["GAME_DATE"] == date]
    return(dfdate)

def excel_write(writer, df, sheetname=''):
    if sheetname != '':
        df.to_excel(writer, sheet_name=sheetname)
    else:
        df.to_excel(writer)

def get_week():
    startDate = datetime.datetime.today()
    while startDate.weekday() != 6:
        startDate = startDate - datetime.timedelta(1)
    week = []
    for i in range(7):
        day = startDate + datetime.timedelta(i)
        dayf = day.strftime('%Y-%m-%d')
        week.append(dayf)
    return(week)

if __name__ == '__main__':
    weekDates = [
        "2022-12-19",
        "2022-12-20",
        "2022-12-21",
        "2022-12-22",
        "2022-12-23",
        "2022-12-24",
        "2022-12-25"
    ]
    week = get_week() # will return the fantasy week that includes the current day
    writer = pd.ExcelWriter('dailyGamelog.xlsx', engine='xlsxwriter')
    
    for i in range(7):
        df = get_gamelog(weekDates[i])
        print(df)
        excel_write(writer, df, weekDates[i])
    writer.save()