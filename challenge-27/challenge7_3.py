import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def climate_plot():
    df_gt = pd.read_excel('GlobalTemperature.xlsx')
    df_ghg = pd.read_excel('ClimateChange.xlsx', sheetname='Data')

    df_ghg = df_ghg[df_ghg['Series code'].isin(
        ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE'])]

    df_ghg_fill = df_ghg.iloc[:, 6:].replace('..', np.nan).fillna(
        method='ffill', axis=1).fillna(method='bfill', axis=1).dropna(axis=0)
    df_ghg_clean = df_ghg_fill.sum(axis=0)

    df_ghg_clean.index = pd.PeriodIndex(
        df_ghg_clean.index, freq='A')
    df_ghg_clean = df_ghg_clean['1990':'2010']

    df_gt.index = pd.to_datetime(df_gt['Date'])
    df_gt_A = df_gt['1990':'2010'].resample('A').mean()
    df_gt_A.index = df_gt_A.index.to_period(freq='A')

    df_merge = pd.concat([df_ghg_clean, df_gt_A['1990':'2010']], axis=1)
    df_merge = (df_merge-df_merge.min())/(df_merge.max()-df_merge.min())
    df_merge.rename(columns={0:'Data'},inplace=True)
    df_merge = df_merge.reindex(columns=['Data','Land Average Temperature','Land And Ocean Average Temperature'])

    df_gt_Q = df_gt.resample('Q').mean()
    df_gt_Q.index = df_gt_Q.index.to_period(freq='Q')
    df_gt_Q = df_gt_Q.reindex(columns=['Land Average Temperature','Land And Ocean Average Temperature'])


    fig, ax = plt.subplots(2, 2)
    df_merge.plot(kind='line', ax=ax[0, 0])
    ax[0, 0].set_xlabel('Years')
    ax[0, 0].set_ylabel('Values')
    
    df_merge.plot(kind='bar', ax=ax[0, 1])
    ax[0, 1].set_xlabel('Years')
    ax[0, 1].set_ylabel('Values')
    
    df_gt_Q.plot(kind='area', ax=ax[1, 0])
    ax[1, 0].set_xlabel('Quarters')
    ax[1, 0].set_ylabel('Values')
    
    df_gt_Q.plot(kind='kde', ax=ax[1, 1])
    ax[1, 1].set_xlabel('Values')
    ax[1, 1].set_ylabel('Values')
    return fig

if __name__=='__main__':
    climate_plot()

