import pandas as pd
import numpy as np
from nba_api.stats import endpoints

data = endpoints.LeagueLeaders()
df = data.league_leaders.get_data_frame()

df.to_excel("output.xlsx")