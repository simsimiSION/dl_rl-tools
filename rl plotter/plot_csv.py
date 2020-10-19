
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate

def get_csv_path(prefix_path):
    filenames = os.listdir(prefix_path)
    fullpaths = [prefix_path + filename for filename in filenames]

    return fullpaths


def read_csv(path_csv):
    try:
        csv_data = pd.read_csv(path_csv)
        value_data = np.array(csv_data['Value'].array)

        return value_data
    except:
        raise Exception("open csv {} error".format(path_csv))


def get_value_data(fullpaths, limit_step, weight=0.85):
    def smooth(data, weight=weight):
        smoothed = []
        last = data[0]
        for da in data:
            smooth_val = last * weight + (1 - weight) * da
            smoothed.append(smooth_val)
            last = smooth_val
        return smoothed

    value_data_len = [ len(read_csv(path_csv)) for path_csv in fullpaths]
    value_data_len.sort()
    value_data = [ read_csv(path_csv)[:min(value_data_len[0], int(limit_step))] for path_csv in fullpaths]

    # 曲线平滑
    value_data = [ smooth(ydata) for ydata in value_data]
    value_data = np.array(value_data)

    return value_data


def plot_value_data(value_data, name, color):
    _, length_t = value_data.shape
    print(length_t)
    xdata = np.arange(length_t) * 1e4

    min_line = np.min(value_data, axis=0) * 100
    max_line = np.max(value_data, axis=0) * 100
    plt.fill_between(xdata, min_line, max_line, where=max_line>min_line, facecolor=color, alpha=0.3)
    plt.plot(xdata, np.mean(value_data * 100, axis=0), label=name, linewidth=2.5,c=color)



def plot_main(prefix_path, limit_step, color):
    name = prefix_path.split('/')[-2]

    fullpaths = get_csv_path(prefix_path)
    value_data = get_value_data(fullpaths, limit_step)
    plot_value_data(value_data, name, color)

if __name__ == '__main__':
    limit_step = 800

    def formatnum(x, pos):
        return '$%.1f$x$10^{4}$' % (x / 10000)

    PATH_CSV_Q_MIX = '5m6m/qmix/'
    PATH_CSV_QTRAN_MIX = '5m6m/qtran/'
    PATH_CSV_VDN_MIX = '5m6m/vdn/'
    PATH_CSV_COMA_MIX = '5m6m/coma/'
    PATH_CSV_G2A_MIX = '5m6m/g2a/'
    
    plot_main(PATH_CSV_Q_MIX, limit_step, color='slategrey')
    plot_main(PATH_CSV_QTRAN_MIX, limit_step, color='m')
    plot_main(PATH_CSV_VDN_MIX, limit_step, color='c')
    plot_main(PATH_CSV_COMA_MIX, limit_step, color='r')
    plot_main(PATH_CSV_G2A_MIX, limit_step, color='y')

    ax = plt.gca()
    ax.xaxis.get_major_formatter().set_powerlimits((0,1))
    plt.xlabel('Time Steps')
    plt.ylabel('Test Win % ')
    plt.legend(loc='upper left')
    plt.grid(True, linewidth = "0.3")
    title_name = PATH_CSV_Q_MIX.split('/')[-3]
    plt.title(title_name)

    plt.savefig('15m17m.pdf', dpi=1200, format='pdf')
    plt.show()










