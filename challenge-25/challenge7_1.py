#! -*-coding:utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
def co2():
    data = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    country = pd.read_excel("ClimateChange.xlsx", sheetname='Country')
    data.set_index('Country code', inplace=True)
    data = data[data['Series code'] == 'EN.ATM.CO2E.KT'].iloc[:,5:]
    data.replace('..', np.nan, inplace=True)
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    data = data.dropna(how='all')
    data = data.sum(axis=1)

    data_merge = pd.concat([data, country.set_index('Country code')], axis=1)
    data_merge.rename(columns = {0: 'Sum emissions'}, inplace=True)
    result = data_merge.groupby('Income group')['Sum emissions'].apply(lambda g: Series([g.sum(), data_merge.loc[g.idxmax(), 'Country name'], g.max(), data_merge.loc[g.idxmin(), 'Country name'],g.min()], index=['Sum emissions', 'Highest emission country', 'Highest emissions', 'Lowest emission country', 'Lowest emissions'])).unstack(1)
    return result.sort_index()


if __name__ == '__main__':
    print(co2())
