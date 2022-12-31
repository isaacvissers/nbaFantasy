from nba_api.stats.endpoints import leaguegamelog
import pandas as pd

def get_gamelog(date, season='2022'):
    gamelog = leaguegamelog.LeagueGameLog(season=season)
    df = pd.DataFrame((gamelog.get_data_frames())[0])
    df.drop('SEASON_ID', axis=1, inplace=True)
    df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
    dfdate = df[df["GAME_DATE"] == str(date)]
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
    date = '2022-12-30'
    df = get_gamelog(date)
    excel_write(df, "dailyGamelog", date)
