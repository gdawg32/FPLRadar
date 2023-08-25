import pandas as pd
from unidecode import unidecode

url = 'https://raw.githubusercontent.com/theFPLkiwi/theFPLkiwi/main/ID_Dictionary.csv'
df = pd.read_csv(url, encoding='latin-1', skipinitialspace=True)
df = df.iloc[:, 10:15]
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
df.columns = ['code', 'id', 'name', 'pos', 'team']
df['name'] = df['name'].apply(unidecode)

def get_fpl_id(name):
    try:
        id = int(df[df['name'].str.lower() == name.lower()]['id'].values[0])
        pos = df[df['name'].str.lower() == name.lower()]['pos'].values[0]
        team = df[df['name'].str.lower() == name.lower()]['team'].values[0]
        name = df[df['name'].str.lower() == name.lower()]['name'].values[0]
        return id, pos, team, name
    except IndexError:
        return None