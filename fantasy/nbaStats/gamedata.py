from nba_api.stats.endpoints import leaguegamelog
import nba_api.stats.endpoints as nba
import pandas as pd
import datetime


today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)

gamelog = leaguegamelog.LeagueGameLog(season='2022')
df = pd.DataFrame((gamelog.get_data_frames())[0])
dftoday = df[df["GAME_DATE"] == str(today)]
dfyesterday = df[df["GAME_DATE"] == str(yesterday)]
print(dftoday)
dftoday.to_excel("today.xlsx")
dfyesterday.to_excel("yesterday.xlsx")

for id in dfyesterday["GAME_ID"]:
    print(id)
    
x = leaguegamelog.LeagueGameLog
print(x)