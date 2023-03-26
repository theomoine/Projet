import pandas as pd
from datetime import datetime, timedelta

# Extrait une plage horaire spécifique des données de prix du bitcoin
df = pd.read_csv('data.csv')
df = df.loc[:, ['t', 'bitcoin']]
df["t"] = pd.to_datetime(df["t"], unit="s")
start_time = pd.Timestamp.now().replace(hour=16, minute=0, second=0, microsecond=0)
end_time = start_time + pd.Timedelta(days=1)
end_time = end_time.replace(hour=20)
df2 = df.set_index('t').between_time(start_time.time(), end_time.time()).reset_index()
df2.to_csv('rapport.csv', index=False)

