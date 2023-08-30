import pandas as pd
from unidecode import unidecode

url = 'https://raw.githubusercontent.com/theFPLkiwi/theFPLkiwi/main/ID_Dictionary.csv'
df = pd.read_csv(url, encoding='latin-1', skipinitialspace=True)
df = df.iloc[:, [0,7,10,11,12,13,14]]
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
df.columns = ['name','ffs_name', 'code', 'id', 'fpl_name', 'pos', 'team']
df['name'] = df['name'].apply(unidecode)
df['ffs_name'] = df['ffs_name'].apply(unidecode)

def get_fpl_id(name):
    columns_to_check = ['fpl_name', 'name', 'ffs_name']
    
    for column in columns_to_check:
        try:
            filter_condition = df[column].str.lower() == name.lower()
            id = int(df[filter_condition]['id'].values[0])
            pos = df[filter_condition]['pos'].values[0]
            team = df[filter_condition]['team'].values[0]
            name = df[filter_condition][column].values[0]
            return id, pos, team, name
        except IndexError:
            pass
        
    return None