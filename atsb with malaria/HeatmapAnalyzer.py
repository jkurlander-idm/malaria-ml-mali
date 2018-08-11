import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from simtools.SetupParser import SetupParser
from scipy import interpolate
import os
import time
mpl.rcParams['pdf.fonttype'] = 42
if not SetupParser.initialized:
    SetupParser.init('HPC')

userpath = 'C:\\Users\\jkurlander'

wdir = os.path.join(userpath, 'Dropbox (IDM)', 'Malaria Team Folder/projects/atsb')
plotdir = os.path.join(wdir, 'sim_plots')
datadir = os.path.join(wdir, 'sim_data')

class HeatmapAnalyzer(BaseAnalyzer):
    def __init__(self):
        super(HeatmapAnalyzer, self).__init__()
        self.channel = 'Blood Smear Parasite Prevalence'
        self.filenames = ['output/InsetChart.json']

    def select_simulation_data(self, data, simulation):
        channeldata = data[self.filenames[0]]['Channels'][self.channel]['Data'][-578:-213]
        channelOtherData = data[self.filenames[0]]['Channels'][self.channel]['Data'][-943:-578]
        simdata = pd.DataFrame({self.channel: channeldata,
                                'pre-prevalence': channelOtherData,
                                'time': list(range(len(channeldata)))})

        for tag in ['killing', 'x_Temporary_Larval_Habitat']:
           simdata[tag] = simulation.tags[tag]
        return simdata

    def finalize(self, all_data):
        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)


        sns.set_style('white', {'axes.linewidth': 0.5})
        fig = plt.figure()
        ax = fig.gca()
        
        sdf = df.groupby(['killing', 'x_Temporary_Larval_Habitat'])[self.channel].agg(np.mean).reset_index()
        sdf['Log_x_Temp'] = np.log10(sdf['x_Temporary_Larval_Habitat'])

        sdf2 = df.groupby(['killing', 'x_Temporary_Larval_Habitat'])['pre-prevalence'].agg(np.mean).reset_index()

        ax.set_xlabel('Killing rate')
        ax.set_ylabel('Initial Prevalence')
        x = np.linspace(0, 0.25, 100)
        y = np.linspace(min(sdf2['pre-prevalence']), max(sdf2['pre-prevalence']), 100)     #np.arange(min(sdf['Log_x_Temp']), max(sdf['Log_x_Temp'])+(sdf['Log_x_Temp'][3]-sdf['Log_x_Temp'][2]), (sdf['Log_x_Temp'][3]-sdf['Log_x_Temp'][2]))
        xx, yy = np.meshgrid(x, y)
        inter = interpolate.Rbf(sdf['killing'],
                        sdf2['pre-prevalence'],
                        sdf[self.channel])
        zz = inter(xx,yy)
        cmap = 'rainbow_r'
        #plt.imshow(zz, cmap = plt.get_cmap(cmap, 10))
        c = plt.contour(xx, yy, zz,cmap=plt.get_cmap((cmap)), vmin=0, vmax=1)
        plt.clabel(c, inline = 1, fontsize = 8, fmt = '%.2f')
        palette = sns.color_palette(cmap, 100)
        ax.scatter(sdf['killing'], sdf2['pre-prevalence'], 20, color=[palette[int(x*100)] for x in sdf[self.channel].values], alpha=0.5)
        #plt.savefig(os.path.join(plotdir, '123myplot123.pdf'), format='PDF')
        plt.title('ATSB Infection Reduction Heatmap')
        plt.show()
        plt.close('all')








if __name__ == '__main__' :

    expid = '4ee73ebf-d59c-e811-a2c0-c4346bcb7275'
    am = AnalyzeManager(expid,
                        analyzers=HeatmapAnalyzer())
    am.analyze()
