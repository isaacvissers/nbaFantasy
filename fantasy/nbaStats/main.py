from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
playerDict = players.get_players()
# print(playerDict)
df = pd.DataFrame(playerDict)
rm = []
df.drop(df[(df['is_active'] == False)].index, inplace=True)
df.drop('is_active', axis=1, inplace=True)
# df.to_excel("players.xlsx")

# print(df["full_name"][df.index][22])
writer = pd.ExcelWriter('nbaStats/fullSeason.xlsx', engine='xlsxwriter')
count = 0
names = []
for index in df.index:
    id = df["id"][df.index][index]
    names.append(df["full_name"][df.index][index])
    gamelog = playergamelog.PlayerGameLog(player_id=id, season='2022')
    dfGameLog = gamelog.get_data_frames()
    df1 = pd.DataFrame(dfGameLog[0])

    df1.drop('SEASON_ID', axis=1, inplace=True)
    df1.drop('VIDEO_AVAILABLE', axis=1, inplace=True)

    df1.to_excel(writer, sheet_name=df["full_name"][df.index][index].strip())

    count += 1
    if count >= 10:
        writer.close()
        exit()





# siakam = [player for player in playerDict if player['full_name'] == 'Pascal Siakam'][0]
# siakamId = siakam['id']

# gamelog = playergamelog.PlayerGameLog(player_id=siakamId, season='2022')
# siakam22 = gamelog.get_data_frames()
# df = pd.DataFrame(siakam22[0])
# df.to_excel("siakamStats.xlsx")