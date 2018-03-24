import pandas as pd
from matplotlib import pyplot as plt

def data_plot():
    data = pd.read_json('user_study.json')
    data_uid = data.groupby('user_id').sum().head(100)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')

    ax.plot(data_uid.index,data_uid.minutes)
    plt.show()
    return ax

if __name__ == '__main__':
    data_plot()
