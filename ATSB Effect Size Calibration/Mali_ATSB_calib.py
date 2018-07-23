# Execute directly: 'python example_optimization.py'
# or via the calibtool.py script: 'calibtool run example_optimization.py'
import copy
import math
import random
import pandas as pd
import numpy as np
import os
from dtk.interventions.irs import add_IRS
from dtk.vector.species import update_species_param
from dtk.interventions.mosquito_release import add_mosquito_release
from dtk.interventions.itn_age_season import add_ITN_age_season

from malaria.reports.MalariaReport import add_habitat_report
from scipy.special import gammaln

from calibtool.CalibManager import CalibManager
from calibtool.algorithms.OptimTool import OptimTool
from calibtool.plotters.LikelihoodPlotter import LikelihoodPlotter
from calibtool.plotters.OptimToolPlotter import OptimToolPlotter
from calibtool.plotters.SiteDataPlotter import SiteDataPlotter
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.utils.reports.CustomReport import BaseVectorStatsReport
from malaria.reports.MalariaReport import add_filtered_report
from dtk.vector.species import set_larval_habitat
from simtools.SetupParser import SetupParser
from spline_functions import *
# from .spline_functions import get_spline_values_for_all_params, get_annual_representative_spline, \
#     get_representative_spline_multipiers
from dtk.interventions.novel_vector_control import add_ATSB

from ATSBEntoCalibSite import ATSBEntoCalibSite

# Which simtools.ini block to use for this calibration
SetupParser.default_block = 'HPC'

# Start from a base MALARIA_SIM config builder
# This config builder will be modify by the different sites defined below
cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')
update_species_param(cb, 'gambiae', 'Indoor_Feeding_Fraction', 0.5)
update_species_param(cb, 'funestus', 'Indoor_Feeding_Fraction', 0.9)
update_species_param(cb, 'funestus', 'Vector_Sugar_Feeding_Frequency', 'VECTOR_SUGAR_FEEDING_EVERY_DAY', overwrite=False)

datadir = 'C:\\Users\\jkurlander\\Dropbox (IDM)'

# List of sites we want to calibrate on
throwaway = 1
species  = 'funestus'
# reference_fname = 'combined_funestus_count.csv'
reference_fname = 'cluster_mosquito_counts_per_house_by_month.csv'
reference_spline = 'Multi_year_calibration_by_HFCA_180404/best_180409/Panjane_funestus.csv'
irs_fn = os.path.join(datadir,
                      'Malaria Team Folder/projects/Mozambique/entomology_calibration/cluster_all_irs_events_pyrethroid_2014.csv')
itn_fn = os.path.join(datadir,
                      'Malaria Team Folder/projects/Mozambique/entomology_calibration/cluster_all_itn_events.csv')


hfca = 'Kangaba'
sites = [ATSBEntoCalibSite(species, hfca=hfca, throwaway=throwaway,
                                      reference_fname = 'C:/Users/jkurlander/Dropbox (IDM)/Malaria Team Folder/projects/atsb/Reference_data/atsbAppliedData.csv'#os.path.join(datadir, 'Malaria Team Folder/projects/Mozambique/entomology_calibration/', reference_fname),
                               )
        ]


Class = "WaningEffectMapPiecewise"
expname = 'Mali ATSB Daily Sugarfeeding Seasonal'
max_iterations = 15
max_diff = 0.5
max_frac_diff = 0.05

# The default plotters used in an Optimization with OptimTool
# plotters = [LikelihoodPlotter(combine_sites=True),
plotters = [SiteDataPlotter(num_to_plot=20, combine_sites=True),
            OptimToolPlotter()  # OTP must be last because it calls gc.collect()
]


#############################################################################################################
ref = sites[0].analyzers[0].reference.copy()
duration = 1#int(max(ref.reset_index()['Month'])/12) + 1

params = [

      # {
      #     'Name': 'KillingProfile',
      #     'Dynamic': True,
      #     'Guess': 0.015,
      #     'Min': 0.0,
      #     'Max': 0.5,
      # },
      # {
      #      'Name': 'HalfLife',
      #      'Dynamic': False,
      #      'Guess': 36500,
      #      'Min': 1,
      #      'Max': 36500
      # },
      # {
      #     'Name': 'BoxDuration',
      #     'Dynamic': False,
      #     'Guess': 900,
      #     'Min': 1,
      #     'Max': 365
      # }
      {
         'Name': 'WetSeason',
          'Dynamic': True,
          'Guess': 0.010243,
          'Min': 0,
          'Max': 1
      },
      {
          'Name': 'DrySeason',
          'Dynamic': True,
          'Guess': 0.04922,
          'Min': 0,
          'Max': 1
      }

]

spline = get_spline_values(ref, species)
hardCodedGuesses = [0.001114407,	0.001019929,	0.001121028, 0.011774454, 	0.039971776, 	0.132583995, 	0.967888784, 	2.214546424, 	0.753793083, 0.336686848,	0.051583281, 0.024973167]
# for i, row in spline.iterrows() :
#     d = row.to_dict()
#     d['Name'] = '%s_%i' % (species, row['Month'])
#     d['Guess'] = hardCodedGuesses[i]
#     params.append(d)




def map_sample_to_model_input(cb, sample):


    tags = {}



    # Updating max habitat values
    #value = sample.pop('KillingProfile')
    #tags.update({'KillingProfile': value})
    dry = sample.pop('DrySeason')
    tags.update({'DrySeason': dry})
    wet = sample.pop('WetSeason')
    tags.update({'WetSeason': wet})
    #time = sample.pop('HalfLife')
    #tags.update({'HalfLife': time})
    #box = sample.pop('BoxDuration')
    #tags.update({'BoxDuration': box})
    add_ATSB(cb, start = 517, coverage = 1.0, kill_cfg = {'Species': 'funestus',
                              'Killing_Config': {"class": Class,
                                                 "Initial_Effect": 1.0,

                                                  #"Box_Duration": box,
                                                 #"Decay_Time_Constant": time,
                                                 "Durability_Map": {
                                                       "Times": [0, 30, 120],
                                                       "Values": [dry, wet, dry]
                                                   }
                                                 }},
                duration = 365)
     #for name,value in sample.items():
     #    print('UNUSED PARAMETER:'+name)
    # assert( len(sample) == 0 ) # All params used

    # For testing only, the duration should be handled by the site !! Please remove before running in prod!
    tags.update(cb.set_param("Simulation_Duration", (throwaway+duration)*365))
    tags.update(cb.set_param('Run_Number', 0))

    return tags


###################################################### INTERVENTIONS ##########################################################
# irs_fn = 'C:\Github\PS_dtk_tools\malaria-mz-magude\data\IRS_input_for_PS.csv'


# add_mosquito_release(cb, start_day=0, species=species, number=10, tsteps_btwn=30)

################################################################################################################################

cb.update_params({'Demographics_Filenames': ['single_node_no_malaria_demographics.json'],

                      'Base_Population_Scale_Factor': 1,

                      "Birth_Rate_Dependence": "FIXED_BIRTH_RATE",
                      "Climate_Model": 'CLIMATE_BY_DATA',

                      "Air_Temperature_Filename": 'Mozambique_Magude_30arcsec_air_temperature_daily.bin',
                      "Land_Temperature_Filename": 'Mozambique_Magude_30arcsec_air_temperature_daily.bin',
                      "Rainfall_Filename": 'Mozambique_Magude_30arcsec_rainfall_daily.bin',
                      "Relative_Humidity_Filename": 'Mozambique_Magude_30arcsec_relative_humidity_daily.bin',

                      "Death_Rate_Dependence": "NONDISEASE_MORTALITY_BY_AGE_AND_GENDER",
                      "Disable_IP_Whitelist": 1,

                      "Enable_Vital_Dynamics": 1,
                      "Enable_Birth": 1,
                      'Enable_Default_Reporting': 1,
                      'Enable_Demographics_Other': 1,
                      # 'Enable_Property_Output': 1,

                      'x_Temporary_Larval_Habitat': 1,
                      'logLevel_default': 'ERROR',

                      "Vector_Species_Names": [species]
                      })

# Just for fun, let the numerical derivative baseline scale with the number of dimensions
volume_fraction = 0.01   # desired fraction of N-sphere area to unit cube area for numerical derivative (automatic radius scaling with N)
num_params = len([p for p in params if p['Dynamic']])
#r = math.exp(1/float(num_params)*(math.log(volume_fraction) + gammaln(num_params/2.+1) - num_params/2.*math.log(math.pi)))
r = 0.05

optimtool = OptimTool(params,
    mu_r = r,           # <-- radius for numerical derivatve.  CAREFUL not to go too small with integer parameters
    sigma_r = r/10.,    # <-- stdev of radius
    center_repeats=1, # <-- Number of times to replicate the center (current guess).  Nice to compare intrinsic to extrinsic noise
    samples_per_iteration=500 # was 32  # 32 # <-- Samples per iteration, includes center repeats.  Actual number of sims run is this number times number of sites.
)


# cb.add_reports(BaseVectorStatsReport(type='ReportVectorStats', stratify_by_species=1))
add_filtered_report(cb, start=365*throwaway)

calib_manager = CalibManager(name=expname,    # <-- Please customize this name
                             config_builder=cb,
                             map_sample_to_model_input_fn=map_sample_to_model_input,
                             sites=sites,
                             next_point=optimtool,
                             sim_runs_per_param_set=1,  # <-- Replicates
                             max_iterations=max_iterations,   # <-- Iterations
                             plotters=plotters)


run_calib_args = {
    "calib_manager":calib_manager
}

if __name__ == "__main__":
    SetupParser.init()
    cm = run_calib_args["calib_manager"]
    cm.run_calibration()
