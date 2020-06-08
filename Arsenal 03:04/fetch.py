import pandas as pd
import json
import glob
from flatten_json import flatten

# competition id has been defined as 2 for Arsenal's 2003/04 season
COMP_ID = 2
MATCH_PATH = f'/Users/sidthakur08/Github/open-data/data/matches/{COMP_ID}'

# creating a list of file inside the directory
files = [f for f in glob.glob(MATCH_PATH+'/*',recursive=True)]

# iterating and loading in data from the directory and flattening it
for file in files:
    with open(file,'rb') as f:
        data = json.load(f)
flatten_data = [flatten(data[i]) for i in range(len(data))]

# list of all the column names and choosing what to drop
col = ['match_id', 'match_week','match_date', 'kick_off','home_team_home_team_id', 'home_team_home_team_name', 
       'home_team_home_team_gender', 'home_team_home_team_group', 'home_team_country_id', 
       'home_team_country_name', 'away_team_away_team_id', 'away_team_away_team_name', 
       'away_team_away_team_gender', 'away_team_away_team_group', 'away_team_country_id', 
       'away_team_country_name', 'home_score', 'away_score', 'match_status', 'last_updated', 
       'metadata_data_version', 'metadata_shot_fidelity_version', 'metadata_xy_fidelity_version', 
       'competition_stage_id', 'competition_stage_name', 'referee_id', 'referee_name']
drop_col = ['kick_off','home_team_home_team_gender','home_team_home_team_group',
            'home_team_country_id','home_team_country_name','away_team_away_team_gender',
            'away_team_away_team_group','away_team_country_id','away_team_country_name',
            'match_status','last_updated','metadata_data_version','metadata_shot_fidelity_version',
            'metadata_xy_fidelity_version','competition_stage_id','competition_stage_name',
            'referee_id','referee_name']

# creating dataframe
df = pd.DataFrame(flatten_data,columns=col)
df = df.drop(columns=drop_col)

# sorting by game weeks
df = df.sort_values(by=['match_week']).reset_index(drop=True)
df.to_csv('matches.csv',index=False)

# making a list of ids and their respective gameweeks
MATCH_ID = list(df['match_id'].values)
MATCH_WEEK = list(df['match_week'].values)
EVENT_PATH = f'/Users/sidthakur08/Github/open-data/data/events'

# converting json files of events (for each game) to csv
for m_id,m_wk in zip(MATCH_ID,MATCH_WEEK):
    print("Getting match id "+str(m_id))
    with open(EVENT_PATH+f'/{m_id}.json','rb') as event:
        event_json = json.load(event)
    flatten_event = [flatten(event_json[i]) for i in range(len(event_json))]
    dataframe = pd.DataFrame(flatten_event)
    dataframe.to_csv(f'{m_wk}.csv',index=False)
