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
#     get_representative_spline_multipliers

from MagudeMultiYearEntoCalibSite import MagudeMultiYearEntoCalibSite

# Which simtools.ini block to use for this calibration
SetupParser.default_block = 'HPC'

# Start from a base MALARIA_SIM config builder
# This config builder will be modify by the different sites defined below
cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')
update_species_param(cb, 'gambiae', 'Indoor_Feeding_Fraction', 0.5)
update_species_param(cb, 'funestus', 'Indoor_Feeding_Fraction', 0.9)

datadir = 'C:\\Users\\jkurlander\\Dropbox (IDM)'

# List of sites we want to calibrate on
throwaway = 1
species  = 'gambiae'
# reference_fname = 'combined_funestus_count.csv'
reference_fname = 'cluster_mosquito_counts_per_house_by_month.csv'
reference_spline = 'Multi_year_calibration_by_HFCA_180404/best_180409/Panjane_funestus.csv'
irs_fn = os.path.join(datadir,
                      'Malaria Team Folder/projects/Mozambique/entomology_calibration/cluster_all_irs_events_pyrethroid_2014.csv')
itn_fn = os.path.join(datadir,
                      'Malaria Team Folder/projects/Mozambique/entomology_calibration/cluster_all_itn_events.csv')


hfca = 'Mali'
sites = [MagudeMultiYearEntoCalibSite(species, hfca=hfca, throwaway=throwaway,
                                      reference_fname = os.path.join(datadir, 'Malaria Team Folder/projects/Mozambique/entomology_calibration/', reference_fname),
                                      )
         ]

expname = '%sEntoCalib%s_TEST' %(hfca, species)
max_iterations = 2

# The default plotters used in an Optimization with OptimTool
# plotters = [LikelihoodPlotter(combine_sites=True),
plotters = [SiteDataPlotter(num_to_plot=20, combine_sites=True),
            OptimToolPlotter()  # OTP must be last because it calls gc.collect()
]


#############################################################################################################
ref = sites[0].analyzers[0].reference.copy()
duration = int(max(ref.reset_index()['Month'])/12) + 1

params = [
    {
        'Name': '%s_max' % (species),
        'Dynamic': False,
        'Guess': 9.4,
        'Min': 6,
        'Max': 14,
    }
]
spline = get_spline_values(ref, species)
fname = os.path.join(datadir, 'Malaria Team Folder/projects/Mozambique/entomology_calibration/', reference_spline)
for i, row in spline.iterrows() :
    d = row.to_dict()
    d['Name'] = '%s_%i' % (species, row['Month'])
    params.append(d)

ls_hab_ref = { 'Capacity_Distribution_Number_Of_Years' : throwaway + duration,
               'Capacity_Distribution_Over_Time' : {
                   'Times' : [0],
                   'Values' : [0.01]
               },
               'Max_Larval_Capacity' : 1e8}


def map_sample_to_model_input(cb, sample):

    tags = {}

    hab = copy.copy(ls_hab_ref)
    timepoints = sorted([int(x.split('_')[1]) for x in sample.keys() if ('max' not in x and 'Multiplier' not in x)])
    dates = [365*throwaway + (x-1)*365/12 for x in timepoints] + [365*(duration + throwaway)-1]
    hab['Capacity_Distribution_Over_Time']['Times'] = [0] + dates
    hab['Capacity_Distribution_Over_Time']['Values'] = [0.01]*len(hab['Capacity_Distribution_Over_Time']['Times'])

    for mindex, month in enumerate(timepoints) :
        name = '%s_%i' %(species, month)
        if name in sample:
            splinevalue = sample.pop(name)
            hab['Capacity_Distribution_Over_Time']['Values'][mindex+1] = splinevalue
            tags.update({name: splinevalue})

    # Updating max habitat values
    max_habitat_name = '%s_max' % species
    if max_habitat_name in sample:
        maxvalue = sample.pop(max_habitat_name)
        hab['Max_Larval_Capacity'] = pow(10, maxvalue)
        tags.update({max_habitat_name: maxvalue})
    for catchment in hfcas :
        name = '%s.Multiplier' % catchment
        if name in sample :
            catchment_mult = sample[name]
            tags.update(cb.set_param(name, catchment_mult))

    set_larval_habitat(cb, { species : {'LINEAR_SPLINE' : hab}})

    # for name,value in sample.items():
    #     print('UNUSED PARAMETER:'+name)
    # assert( len(sample) == 0 ) # All params used

    # For testing only, the duration should be handled by the site !! Please remove before running in prod!
    tags.update(cb.set_param("Simulation_Duration", (throwaway+duration)*365))
    tags.update(cb.set_param('Run_Number', 0))

    return tags


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
volume_fraction = 0.05   # desired fraction of N-sphere area to unit cube area for numerical derivative (automatic radius scaling with N)
num_params = len([p for p in params if p['Dynamic']])
r = math.exp(1/float(num_params)*(math.log(volume_fraction) + gammaln(num_params/2.+1) - num_params/2.*math.log(math.pi)))
r *= 0.5

optimtool = OptimTool(params,
    mu_r = r,           # <-- radius for numerical derivatve.  CAREFUL not to go too small with integer parameters
    sigma_r = r/10.,    # <-- stdev of radius
    center_repeats=1, # <-- Number of times to replicate the center (current guess).  Nice to compare intrinsic to extrinsic noise
    samples_per_iteration=10 # was 32  # 32 # <-- Samples per iteration, includes center repeats.  Actual number of sims run is this number times number of sites.
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
