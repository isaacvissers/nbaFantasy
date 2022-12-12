from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import datetime
today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)

gamelog = leaguegamelog.LeagueGameLog(season='2022')
df = pd.DataFrame((gamelog.get_data_frames())[0])
print(df)
dftoday = df.loc[df["GAME_DATE"] == today, ]
print(dftoday)
df.to_excel("gamelog.xlsx")