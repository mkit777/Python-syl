import pandas as pd
from sklearn.linear_model import LinearRegression


def Temperature():
    gt = pd.read_csv('GlobalSurfaceTemperature.csv')
    ghg = pd.read_csv('GreenhouseGas.csv')
    co2 = pd.read_csv('CO2ppm.csv')

    gt.index = pd.to_datetime(gt.Year, format='%Y')
    gt_clean = gt.reindex(columns=['Median', 'Upper', 'Lower'])

    ghg.index = pd.to_datetime(ghg.Year, format='%Y')
    ghg_clean = ghg.drop('Year', axis=1).dropna(axis=0)

    co2.index = pd.to_datetime(co2.Year, format='%Y')
    co2_clean = co2.drop('Year', axis=1)

    data_merge = pd.concat([co2_clean, ghg_clean, gt_clean], axis=1)
    feature = data_merge.iloc[:, :4].fillna(method='ffill').fillna(method='bfill')

    target_mid = data_merge.iloc[:, 4]
    target_up = data_merge.iloc[:, 5]
    target_low = data_merge.iloc[:, 6]

    feature_train = feature['1980':'2010']
    feature_test = feature['2011':'2017']

    target_train_mid = target_mid['1980':'2010']
    target_train_up = target_up['1980':'2010']
    target_train_low = target_low['1980':'2010']

    model_mid = LinearRegression()
    model_mid.fit(feature_train, target_train_mid)
    mid_ret = model_mid.predict(feature_test)

    model_up = LinearRegression()
    model_up.fit(feature_train, target_train_up)
    up_ret = model_mid.predict(feature_test)

    model_low = LinearRegression()
    model_low.fit(feature_train, target_train_low)
    low_ret = model_mid.predict(feature_test)

    return list(up_ret), list(mid_ret), list(low_ret)

if __name__ == '__main__':
    print(Temperature())