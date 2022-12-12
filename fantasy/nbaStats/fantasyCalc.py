import pandas as pd

writer = pd.ExcelWriter('fullfantasySeason.xlsx', engine='xlsxwriter')
file = pd.read_excel("fullSeason.xlsx", sheet_name=None)
for name, df in file.items():
    fantasyPTS = []
    for index, row in df.iterrows():
        fp = row['PTS'] + row["REB"] * 1.2 + row['AST'] * 1.5 + row['STL'] * 2 + row['BLK'] * 2 - row['TOV']
        fantasyPTS.append(round(fp,1))
    df['fantasy_points'] = fantasyPTS
    df.drop(df.columns[0], axis=1, inplace=True)
    print(df)
    df.to_excel(writer, sheet_name=name)

writer.close()