import pandas as pd
def quarter_volume():
    data = pd.read_csv('apple.csv',header=0)
    date = pd.to_datetime(data['Date'])
    data.index=date
    data.drop('Date',axis='columns')
    second_volume = data.resample('Q').sum().sort_values('Volume',axis='index',ascending=False).iloc[1,-1]
    return second_volume

if __name__ == '__main__':
    print(quarter_volume())