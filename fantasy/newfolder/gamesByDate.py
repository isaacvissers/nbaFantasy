from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import time

def get_gamelog(dates, season='2022'):
    gamelog = leaguegamelog.LeagueGameLog(season=season)
    df = pd.DataFrame((gamelog.get_data_frames())[0])
    df.drop('SEASON_ID', axis=1, inplace=True)
    df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    dfdate = df[df["GAME_DATE"] in dates]
    return(dfdate)

def excel_write(df, filename, sheetname=''):
    writer = pd.ExcelWriter(filename+'.xlsx', engine='xlsxwriter')
    if sheetname != '':
        df.to_excel(writer, sheet_name=sheetname)
        writer.save()
        writer.close()
    else:
        df.to_excel(writer)
        writer.save()
        writer.close()

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
    df = {}

    df = get_gamelog(weekDates)
    print(df)
    # for i in range(7):
    #     excel_write(df, "dailyGamelog", weekDates[i])