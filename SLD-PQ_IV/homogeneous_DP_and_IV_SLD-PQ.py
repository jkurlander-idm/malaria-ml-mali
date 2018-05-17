from calibtool.study_sites.site_setup_functions import summary_report_fn
# from dtk.interventions.malaria_drug_campaigns import add_drug_campaign
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.vector.species import set_species_param
from dtk.generic.climate import set_climate_constant
from createSimDirectoryMapBR import createSimDirectoryMap
from malaria.interventions.malaria_drug_campaigns import add_drug_campaign
from dtk.interventions.ivermectin import add_ivermectin
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.ModBuilder import ModBuilder, ModFn
from simtools.SetupParser import SetupParser
from update_drug_params import update_drugs

import pandas as pd
import os


def add_ivermectin_group(cb, coverage=1.0, start_days=[60, 60+365], drug_code=30, smc_code='DP5'):

    add_ivermectin(cb, drug_code=drug_code, coverage=coverage, start_days=start_days,
                   trigger_condition_list=['Received_Campaign_Drugs'])

    return {'Intervention_type': '%s+IV_%i' % (smc_code, drug_code)}


def add_smc_group(cb, coverage=1.0, start_days=[60, 60+365], agemax=10, drug='DP', dp_gam_kill_on=1):

    add_drug_campaign(cb, 'SMC', drug, start_days=start_days, repetitions=3, interval=30,
    coverage=coverage,
    target_group={'agemin': 0, 'agemax': agemax})

    if not dp_gam_kill_on:
        malaria_drug_params = update_drugs(['DHA', 'Drug_Gametocyte02_Killrate'], 0.0)
        malaria_drug_params = update_drugs(['DHA', 'Drug_Gametocyte34_Killrate'], 0.0,
                                           malaria_drug_params=malaria_drug_params)
        malaria_drug_params = update_drugs(['DHA', 'Drug_GametocyteM_Killrate'], 0.0,
                                           malaria_drug_params=malaria_drug_params)
        malaria_drug_params = update_drugs(['Piperaquine', 'Drug_Gametocyte02_Killrate'], 0.0,
                                           malaria_drug_params=malaria_drug_params)

        cb.update_params({"Malaria_Drug_Params": malaria_drug_params})

    return {'Coverage': coverage, 'Start': start_days[0], 'Intervention_type': 'SMC_GK%i_' %dp_gam_kill_on+str(agemax)+drug}


def add_summary_report(cb, start_day=0):

    summary_report_fn(start=start_day+1, interval=1.0, description='Daily_Report',
                      age_bins=[5.0, 15.0, 100.0])(cb)

    return None


def make_simmap(expname, filetype='Inset'):

    simmap = createSimDirectoryMap(expname)
    # simmap = get_filepath(simmap, filetype)

    return simmap


# Get filelist of files in simmap
def get_filepath(simmap, filetype='state-'):

    filelist = []
    for path in simmap['outpath']:
        outputpath = os.path.join(path, 'output')
        for file in os.listdir(outputpath):
            if filetype in file:
                filelist.append(os.path.join(outputpath, file))

    simmap['filelist'] = filelist

    return simmap


def get_outpath_for_serialized_file(simmap, seed):

    temp = simmap[simmap['Run_Number'] == seed]

    return temp[temp['Run_Number'] == seed]['outpath'].values[0]


if __name__ == "__main__":

    sim_duration = 365 * 1
    num_seeds = 50

    expname = 'Primaquine_Ivermectin'

    SetupParser.init('HPC')

    cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

    # intervention_days = [i for i in range(0, 370, 10)]
    intervention_days = [210]
    coverages = [0.6, 0.7, 0.8, 0.9, 1.0]
    # coverages = [0.6]

    exp_name = ['2ac6fce6-9554-e811-a2bf-c4346bcb7274']

    for exp in exp_name:
        temp_sim_map = make_simmap(exp, filetype='Inset')
        if 'sim_map' not in locals():
            sim_map = temp_sim_map
        else:
            sim_map = pd.concat([sim_map, temp_sim_map])

    # DP only (expanded and regular)
    SMC1 = [
                [
                   ModFn(DTKConfigBuilder.set_param, 'Run_Number', seed),
                   ModFn(DTKConfigBuilder.set_param, 'Simulation_Duration', smc_start_day+365),
                   ModFn(add_smc_group,
                             start_days=[smc_start_day],
                             coverage=smc_coverage, drug=drug, agemax=agemax, dp_gam_kill_on=1),
                   ModFn(add_summary_report, start_day=smc_start_day),
                   ModFn(DTKConfigBuilder.set_param, 'Serialized_Population_Path',
                          '{path}/output'.format(path=
                                                 get_outpath_for_serialized_file(simmap, seed)))
                ]
               for smc_start_day in intervention_days
               for smc_coverage in coverages
               for seed in range(num_seeds)
               for simmap in [sim_map]
               for agemax in [5, 15]
               for drug in ['DP']
            ]

    # DP + Primaquine (expanded and regular)
    SMC2 = [
        [
            ModFn(DTKConfigBuilder.set_param, 'Run_Number', seed),
            ModFn(DTKConfigBuilder.set_param, 'Simulation_Duration', smc_start_day + 365),
            ModFn(add_smc_group,
                  start_days=[smc_start_day],
                  coverage=smc_coverage, drug=drug, agemax=agemax, dp_gam_kill_on=gam_kill),
            ModFn(add_summary_report, start_day=smc_start_day),
            ModFn(DTKConfigBuilder.set_param, 'Serialized_Population_Path',
                  '{path}/output'.format(path=
                                         get_outpath_for_serialized_file(simmap, seed)))
        ]
        for smc_start_day in intervention_days
        for smc_coverage in coverages
        for seed in range(num_seeds)
        for simmap in [sim_map]
        for agemax in [5, 15]
        for drug in ['DPP']
        for gam_kill in [0, 1]
    ]

    # DP + Ivermectin (expanded and regular)
    SMC3 = [
        [
            ModFn(DTKConfigBuilder.set_param, 'Run_Number', seed),
            ModFn(DTKConfigBuilder.set_param, 'Simulation_Duration', smc_start_day + 365),
            ModFn(add_smc_group,
                  start_days=[smc_start_day],
                  coverage=smc_coverage, drug=drug, agemax=agemax, dp_gam_kill_on=1),
            ModFn(add_ivermectin_group, start_days=[smc_start_day], drug_code=drug_code, smc_code=drug + str(agemax)),
            ModFn(add_summary_report, start_day=smc_start_day),
            ModFn(DTKConfigBuilder.set_param, 'Serialized_Population_Path',
                  '{path}/output'.format(path=
                                         get_outpath_for_serialized_file(simmap, seed)))
        ]
        for smc_start_day in intervention_days
        for smc_coverage in coverages
        for seed in range(num_seeds)
        for simmap in [sim_map]
        for agemax in [5, 15]
        for drug in ['DP']
        for drug_code in [30, 90]
    ]

    # builder = ModBuilder.from_list(SMC3)
    builder = ModBuilder.from_list(SMC1+SMC2+SMC3)

    set_climate_constant(cb)
    set_species_param(cb, 'gambiae', 'Larval_Habitat_Types',
                      {"LINEAR_SPLINE": {
                          "Capacity_Distribution_Per_Year": {
                              "Times": [0.0, 30.417, 60.833, 91.25, 121.667, 152.083,
                                        182.5, 212.917, 243.333, 273.75, 304.167, 334.583],
                              # "Values": [1, 0.25, 0.1, 1, 1, 0.5, 12, 5, 3, 2, 1.5, 1.5]
                              "Values": [3, 0.8,  1.25, 0.1,  2.7, 8, 4, 35, 6.8,  6.5, 2.6, 2.1]
                          },
                          "Max_Larval_Capacity": 1e9
                      }})
    set_species_param(cb, "gambiae", "Indoor_Feeding_Fraction", 0.9)

    cb.update_params({"Demographics_Filenames": ['Calibration\single_node_demographics.json'],

                      'Antigen_Switch_Rate': pow(10, -9.116590124),
                      'Base_Gametocyte_Production_Rate': 0.06150582,
                      'Base_Gametocyte_Mosquito_Survival_Rate': 0.002011099,
                      'Base_Population_Scale_Factor': 0.1,

                      "Birth_Rate_Dependence": "FIXED_BIRTH_RATE",
                      "Death_Rate_Dependence": "NONDISEASE_MORTALITY_BY_AGE_AND_GENDER",
                      "Disable_IP_Whitelist": 1,

                      "Enable_Vital_Dynamics": 1,
                      "Enable_Birth": 1,
                      'Enable_Default_Reporting': 1,
                      'Enable_Demographics_Other': 1,
                      # 'Enable_Property_Output': 1,

                      'Falciparum_MSP_Variants': 32,
                      'Falciparum_Nonspecific_Types': 76,
                      'Falciparum_PfEMP1_Variants': 1070,
                      'Gametocyte_Stage_Survival_Rate': 0.588569307,

                      'MSP1_Merozoite_Kill_Fraction': 0.511735322,
                      'Max_Individual_Infections': 3,
                      'Nonspecific_Antigenicity_Factor': 0.415111634,

                      'x_Temporary_Larval_Habitat': 1,
                      'logLevel_default': 'ERROR',

                      "Simulation_Duration": sim_duration,
                      "Serialization_Test_Cycles": 0,
                      'Serialized_Population_Filenames': ['state-25550.dtk'],
                      "Vector_Species_Names": ['gambiae']
                      })

    # from malaria.reports.MalariaReport import add_event_counter_report
    # add_event_counter_report(cb, ['Received_Campaign_Drugs', 'Received_Ivermectin'])

    run_sim_args = {'config_builder': cb,
                    'exp_name': expname,
                    'exp_builder': builder}

    exp_manager = ExperimentManagerFactory.from_setup()
    exp_manager.run_simulations(**run_sim_args)
    exp_manager.wait_for_finished(verbose=True)
