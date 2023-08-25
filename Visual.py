import requests
import pandas as pd
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar

def get_player_json(id):
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        elements = data.get('elements', [])
        player = next((element for element in elements if element['id'] == id), None)
        if player:
            return player
        else:
            print("No player with this ID")
    else:
        print("Failed to retrieve data from the API.")

new_column_names = ['Name', 'Goals', 'Assists', 'Points', 'Minutes', 'xG', 'xA', 'Bonus', 'BPS', 'Threat', 'Starts']

def get_player_data(player_id):
    data = get_player_json(player_id)  # Replace with your actual function call
    new_column_names = [
        'web_name',
        'goals_scored',
        'assists',
        'total_points',
        'minutes',
        'expected_goals',
        'expected_assists',
        'bonus',
        'bps',
        'threat',
        'starts'
    ]
    df = pd.DataFrame(data, index=[0])
    df = df[new_column_names]
    df.columns = new_column_names
    return df

def visualise(p1, p2):
    player_ids = [p1[0], p2[0]]
    positions = [p1[1], p2[1]]
    teams = [p1[2], p2[2]]
    names = [p1[3], p2[3]]
    # Fetch player data and concatenate
    dfs = [get_player_data(player_id) for player_id in player_ids]
    df = pd.concat(dfs, ignore_index=True)
    df.columns = new_column_names
    #get parameters
    params = list(df.columns)
    params = params[1:]
    #add ranges to list of tuple pairs
    ranges = []
    a_values = []
    b_values = []

    for x in params:
        a = float(min(df[params][x]))
        a = a - (a*.25)
        
        b = float(max(df[params][x]))
        b = b + (b*.25)
        
        ranges.append((a,b))
        
    for x in range(len(df['Name'])):
        if df['Name'][x] == names[0]:
            a_values = df.iloc[x].values.tolist()
        if df['Name'][x] == names[1]:
            b_values = df.iloc[x].values.tolist()
            
    a_values = a_values[1:]
    b_values = b_values[1:]

    values = [a_values,b_values]
    # Convert float strings to float values
    tuple_pair = [
        [float(value) if isinstance(value, str) and '.' in value else value for value in row]
        for row in values
    ]

    #title 

    title = dict(
        title_name=df['Name'][0],
        title_color = 'red',
        subtitle_name = teams[0],
        subtitle_color = 'red',
        title_name_2=df['Name'][1],
        title_color_2 = 'blue',
        subtitle_name_2 = teams[1],
        subtitle_color_2 = 'blue',
        title_fontsize = 18,
        subtitle_fontsize=15
    )

    endnote = 'Oakley rules'

    #instantiate radar chart class
    radar = Radar()

    fig,ax = radar.plot_radar(ranges=ranges,params=params,values=tuple_pair,
                            radar_color=['#B6282F', '#344D94'],
                            alphas=[.75,.6],title=title,endnote=endnote,
                            compare=True)
    fig.savefig(f"{names[0]}vs{names[1]}.png", dpi=300, bbox_inches='tight')
    return True