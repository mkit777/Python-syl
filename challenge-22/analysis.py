import json
import pandas as pd

def analysis(file, user_id):
    times = 0
    minutes=0
    with open(file) as f:
        df = pd.read_json(f)
        times = df[df['user_id']==user_id].shape[0]
        minutes = df.loc[df['user_id']==user_id,'minutes'].sum()
    return times,minutes
