import os
import json
import pandas as pd
import numpy as np

from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.SetupParser import SetupParser

from simtools.ModBuilder import ModBuilder, ModFn

from dtk.vector.study_sites import configure_site
from dtk.interventions.novel_vector_control import add_ATSB
from dtk.vector.species import update_species_param, set_larval_habitat
from dtk.interventions.outbreakindividual import recurring_outbreak
exp_name = 'Test 2d sweep'
cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

species = 'gambiae'
years = 5

cb.update_params( {
    'Config_Name' : 'ATSB_Test_Kangaba_EIR',
    'Simulation_Duration' : 365*years,
    'Vector_Species_Names' : [species],
    'Demographics_Filenames': ['demographics.json'],

    'Base_Population_Scale_Factor': 1,

    "Birth_Rate_Dependence": "FIXED_BIRTH_RATE",
    "Climate_Model": 'CLIMATE_BY_DATA',

    "Air_Temperature_Filename": 'Burkina Faso_30arcsec_air_temperature_daily.bin',
    "Land_Temperature_Filename": 'Burkina Faso_30arcsec_air_temperature_daily.bin',
    "Rainfall_Filename": 'Burkina Faso_30arcsec_rainfall_daily.bin',
    "Relative_Humidity_Filename": 'Burkina Faso_30arcsec_relative_humidity_daily.bin',
    #"Serialization_Time_Steps": [365*years],

    # 50-year burn-in with a 12-year climate cycle based on Burkina Faso
    #"Serialized_Population_Path": '\\\\internal.idm.ctr\\IDM\\Home\\jkurlander\\output\\50 year burn-in_20180801_171145\\b43\\765\\05a\\b4376505-ae95-e811-a2c0-c4346bcb7275\\output',
    #"Serialized_Population_Filenames": ['state-18250.dtk'],
    "logLevel_VectorHabitat": 'ERROR',
})

update_species_param(cb, 'gambiae', 'Indoor_Feeding_Fraction', 0.5)
update_species_param(cb, 'gambiae', 'Vector_Sugar_Feeding_Frequency', 'VECTOR_SUGAR_FEEDING_EVERY_DAY', overwrite=False)
update_species_param(cb, 'gambiae', 'Anthropophily', 0.8)
update_species_param(cb, 'gambiae', 'Adult_Life_Expectancy', 20)


# Habitat is based on a 1-year calibration of the control site of the Mali study.
#CDC Habitats 0.001022239,  0.001720589,     0.001294523,   0.032008412,    0.044822194,    0.014206219,        0.617550763,    3.537562285,    3.907661784,    1.487261934,    0.579478307,    0.068954299     Gambiae, anthropophily .8, life expectancy 20, CDC Control larval habitat  7.08 Gambiae max
#HLC Habitats 0.001,        0.001236706,    0.001933152,    0.056693638,    0.057953358,    0.015,              0.95,           2.159928736,    3.205076212,    0.43290933,     0.391090655,    0.138816133     Gambiae, anthropophily .8, life expectancy 20, HLC Control larval habitat, 7.44 Gambiae_max
hab = {'Capacity_Distribution_Number_Of_Years': 1, 'Capacity_Distribution_Over_Time': {
    'Times': [0, 30.4166666666667, 60.8333333333333, 91.25, 121.6666666666667, 152.0833333333334, 182.5,
              213.9166666666666, 243.3333333333334, 273.75, 304.5833333333333, 335],
    'Values': [0.001, 0.001236706, 0.001933152, 0.056693638, 0.057953358, 0.015, 0.95, 2.159928736, 3.205076212,
               0.43290933, 0.391090655, 0.138816133]}, 'Max_Larval_Capacity': 2.75e7}
set_larval_habitat(cb, {species: {'LINEAR_SPLINE': hab}})

recurring_outbreak(cb, outbreak_fraction=0.01, start_day=152, repetitions=years, tsteps_btwn= 365)


def atsb_fn(cb, killing, startDay):

    # Start of June in Mali
    start_day = startDay+152

    add_ATSB(cb, start = start_day,
             coverage = 1.0, kill_cfg = {'Species': species,
                                    'Killing_Config': {"class": 'WaningEffectConstant',
                                                       "Initial_Effect": killing,
                                    }},
             duration = 10000)
    # add_ATSB(cb, coverage=coverage, start=100, duration=365, kill_cfg=killing_cfg[1])
    return {'killing': killing,
            'startDay': startDay}


# add_ATSB(cb, start=100, coverage=1, duration=365)

builder = ModBuilder.from_list([[
    ModFn(atsb_fn, killing, (years-2)*365),
    ModFn(DTKConfigBuilder.set_param, 'x_Temporary_Larval_Habitat', hab)
    # Run simulation with coverage, duration, or repetitions spread.
    # Don't leave duration over 210 because we don't know how ATSBs act after 210 days, or how they act after Dec 31.

    ] for killing in np.linspace(0, 0.25, 20) for hab in np.arange(0.2, 1, 0.478/10)
])


run_sim_args = {'config_builder': cb,
                'exp_name': exp_name,
                'exp_builder': builder
                }

if __name__ == "__main__":
    SetupParser.init('HPC')
    exp_manager = ExperimentManagerFactory.init()
    exp_manager.run_simulations(**run_sim_args)
    # Wait for the simulations to be done
    exp_manager.wait_for_finished(verbose=True)
    assert (exp_manager.succeeded())
