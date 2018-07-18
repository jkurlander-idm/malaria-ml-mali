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

hlc_fname = os.path.join(datadir, 'HLC_raw_all_dates.csv')


def add_date_column(df, hlc_fname) :

    import calendar

    cal = {v: k for k,v in enumerate(calendar.month_abbr)}
    df['date'] = df.apply(lambda x : datetime.date(x['Year'], cal[x['Month'][:3]], 1), axis=1)
    df.to_csv(hlc_fname, index=False)


if __name__ == '__main__' :

    df = pd.read_csv(hlc_fname)

    for location, ldf in df.groupby('Position') :
        grouped = ldf.groupby(['Study Sites', 'date'])
        sdf = grouped['mosquito ID'].agg(len).reset_index()
        sdf.rename(columns={'mosquito ID' : 'vector count'}, inplace=True)
