import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    data = data[data['Series code'].isin(['NY.GDP.MKTP.CD','EN.ATM.CO2E.KT'])]
    data.set_index(['Country code','Series code'],inplace=True)
    data = data.iloc[:,4:].replace('..',np.nan).fillna(method='ffill',axis=1).fillna(method='bfill',axis=1).fillna(value=0).sum(axis=1)
    ret = data.unstack('Series code')
    ret = (ret-ret.min())/(ret.max()-ret.min())
    ret.rename(columns={'EN.ATM.CO2E.KT':'CO2-SUM','NY.GDP.MKTP.CD':'GDP-SUM'},inplace=True)
    labels = [list(ret.index).index(i) for i in ['USA','CHN','FRA','RUS','GBR']]
    ret.columns.name=None
    ret.index.name=None

    fig = plt.subplot()
    plt.xlabel('Countries')
    plt.ylabel('Values')
    ret.plot(kind='line',title='GDP-CO2',xticks=labels,ax=fig)
    plt.show()
    return fig,[np.round(i,3).tolist() for i in ret.loc['CHN'].values]

if __name__ == '__main__':
   print( co2_gpd_plot())
    
