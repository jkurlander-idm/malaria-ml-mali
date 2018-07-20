import os
import json
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from plotting.colors import load_color_palette
mpl.rcParams['pdf.fonttype'] = 42


rootdir = 'D:/Dropbox (IDM)'
datadir = os.path.join(rootdir, 'Malaria Team Folder/data/Novel VC/ATSB/phase 2 data/merged_2018_07')
plotdir = os.path.join(rootdir, 'Malaria Team Folder/projects/atsb/data_exploration_plots')

hlc_fname = os.path.join(datadir, 'HLC_raw_all_dates.csv')

atsb_start = datetime.date(2017, 6, 1)
intervention_villages = ['Krekelo', 'Sirakele', 'Trekourou', 'Farabale', 'Kignele', 'Tiko', 'Sambadani']


def add_date_column() :

    df = pd.read_csv(hlc_fname)

    import calendar

    cal = {v: k for k,v in enumerate(calendar.month_abbr)}
    df['date'] = df.apply(lambda x : datetime.date(x['Year'], cal[x['Month'][:3]], 1), axis=1)
    df.to_csv(hlc_fname, index=False)

def load_df() :

    df = pd.read_csv(hlc_fname)
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_hlc_by_site() :

    df = load_df()

    palette = load_color_palette()

    fig = plt.figure('HLC vector counts', figsize=(16,10))
    axes = [fig.add_subplot(4, 4, x + 1) for x in range(14)]
    fig.subplots_adjust(left=0.05, right=0.97, top=0.95, bottom=0.05)
    linestyles = ['-o', '--o']
    for locindex, (location, ldf) in enumerate(df.groupby('Position')) :
        grouped = ldf.groupby(['Study Sites', 'date'])
        sdf = grouped['mosquito ID'].agg(len).reset_index()
        sdf.rename(columns={'mosquito ID' : 'vector count'}, inplace=True)
        sdf.sort_values(by=['Study Sites', 'date'], inplace=True)

        for s, (site, ssdf) in enumerate(sdf.groupby('Study Sites')) :
            ax = axes[s]
            ax.plot(ssdf['date'], ssdf['vector count'], linestyles[locindex], color=palette[s],
                    label=location if s == 0 else '')
            ax.set_title(site)
            ax.set_xlim(np.min(df['date']), np.max(df['date']))
            if s < 10 :
                ax.set_xticklabels([])
            else :
                ax.set_xticklabels(['Jun \'16', '', '', 'Dec \'16', '', '', 'Jun \'17', '', '', 'Dec \'17', ''])
            if s == 0 and locindex > 0 :
                ax.legend()
            if s%4 == 0 :
                ax.set_ylabel('mosquito count')
            if locindex == 1 and site in intervention_villages :
                ymin, ymax = ax.get_ylim()
                ax.fill_between([atsb_start, np.max(df['date'])], [ymin,ymin], [ymax, ymax],
                                color='k', alpha=0.25, linewidth=0)
                ax.set_ylim(ymin, ymax)
    plt.savefig(os.path.join(plotdir, 'HLC_by_site.png'))
    plt.savefig(os.path.join(plotdir, 'HLC_by_site.pdf'), format='PDF')
    plt.show()

if __name__ == '__main__' :

    plot_hlc_by_site()