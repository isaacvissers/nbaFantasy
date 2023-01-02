from nba_api.stats.endpoints import playernextngames

x = playernextngames.PlayerNextNGames(player_id=1630173, number_of_games=5).get_data_frames()[0]
print(x)
print(x.columns)