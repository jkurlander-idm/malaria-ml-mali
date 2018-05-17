import pandas as pd
from simtools.Utilities.Experiments import retrieve_experiment
from COMPS import Client

# def get_expt(expname, is_name=True) :
#
#     from COMPS import Client
#     Client.login('https://comps.idmod.org')
#
#     from simtools.DataAccess.ExperimentDataStore import ExperimentDataStore
#
#     if is_name :
#         return ExperimentDataStore.get_most_recent_experiment(expname)
#     return ExperimentDataStore.get_experiment(expname)


def createSimDirectoryMap(expname):

    #from simtools.OutputParser import CompsDTKOutputParser
    # from COMPS.Data import Suite, QueryCriteria
    # from COMPS import Client
    # Client.login('https://comps.idmod.org')

    # ste = Suite.get(expname)
    # expts = ste.get_experiments()
    #
    # for exp in expts:
    #     expt = get_expt(str(exp.id), is_name)
    #     if 'df' not in locals():
    #         df = pd.DataFrame( [x.tags for x in expt.simulations] )
    #         df['simid'] = pd.Series( [x.id for x in expt.simulations])
    Client.login('https://comps.idmod.org')

    expt = retrieve_experiment(expname)
    # expt = retrieve_experiment(expname)
    df = pd.DataFrame( [x.tags for x in expt.simulations] )
    df['simid'] = pd.Series( [x.id for x in expt.simulations])

    """
    sdf = get_status(expname)

    if not (sdf['status'].str.contains('Succeeded')).all() :
        print 'Warning: not all jobs in %s succeeded' % expname, ':',
        print len(sdf[sdf['status'] != 'Succeeded']), 'unsucceeded'
        df = pd.merge(left=df, right=sdf, on='simid')
        df = df[df['status'] == 'Succeeded']

        e = Experiment.get(expt.exp_id)
        sims = e.get_simulations(QueryCriteria().select(['id', 'state']).where('state=Succeeded').select_children('hpc_jobs'))
        sdf = pd.DataFrame( { 'simid' : [x.id for x in sims],
                              'outpath' : [x.hpc_jobs[-1].working_directory for x in sims] } )
        sdf['simid'] = sdf['simid'].astype(unicode)
        df = pd.merge(left=df, right=sdf, on='simid')
    else :
    """
    df['outpath'] = pd.Series([x.get_path() for x in expt.simulations])

    return df


def createSimDirectoryMap_suite(sname):

    #from simtools.OutputParser import CompsDTKOutputParser
    from COMPS.Data import Suite, QueryCriteria
    from simtools.Utilities.Experiments import retrieve_experiment
    from COMPS import Client
    Client.login('https://comps.idmod.org')

    ste = Suite.get(sname)
    expts = ste.get_experiments()
    tagstemp = []
    simidstemp = []

    for exp in expts:
        expt = retrieve_experiment(str(exp.id))
        tagstemp.append([x.tags for x in expt.simulations])
        simidstemp.append([x.id for x in expt.simulations])
    tags = [item for sublist in tagstemp for item in sublist]
    simids = [item for sublist in simidstemp for item in sublist]
    df = pd.DataFrame(tags)
    df['simid'] = simids

    """
    sdf = get_status(expname)

    if not (sdf['status'].str.contains('Succeeded')).all() :
        print 'Warning: not all jobs in %s succeeded' % expname, ':',
        print len(sdf[sdf['status'] != 'Succeeded']), 'unsucceeded'
        df = pd.merge(left=df, right=sdf, on='simid')
        df = df[df['status'] == 'Succeeded']

        e = Experiment.get(expt.exp_id)
        sims = e.get_simulations(QueryCriteria().select(['id', 'state']).where('state=Succeeded').select_children('hpc_jobs'))
        sdf = pd.DataFrame( { 'simid' : [x.id for x in sims],
                              'outpath' : [x.hpc_jobs[-1].working_directory for x in sims] } )
        sdf['simid'] = sdf['simid'].astype(unicode)
        df = pd.merge(left=df, right=sdf, on='simid')
    else :
    """
    df['outpath'] = pd.Series([x.get_path() for x in expt.simulations])

    return df


def get_status(expname) :

    expt = get_expt(expname)
    from simtools.ExperimentManager.BaseExperimentManager import BaseExperimentManager
    from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
    expt_manager = ExperimentManagerFactory.from_experiment(expt)
    states, msgs = BaseExperimentManager.get_simulation_status(expt_manager)

    df = pd.DataFrame( { 'simid' : states.keys(),
                         'status' : states.values() } )
    return df

def rescue_expts(expname) :

    from COMPS.Data import Experiment, QueryCriteria
    from simtools.Utilities.COMPSUtilities import COMPS_login
    from simtools.Utilities.Experiments import COMPS_experiment_to_local_db

    experiment_name = "%%" + expname + "%%"
    endpoint = 'https://comps.idmod.org'
    user = 'jgerardin'

    def get_experiments_by_name(name,user):
        return Experiment.get(query_criteria=QueryCriteria().where(['name~%s' % name, 'owner=%s' % user]))

    COMPS_login(endpoint)
    for experiment_data in get_experiments_by_name(experiment_name,user):
        # Create a new experiment
        print(experiment_data)
        experiment = COMPS_experiment_to_local_db(exp_id=str(experiment_data.id),
                                                  endpoint=endpoint,
                                                  verbose=False,
                                                  save_new_experiment=True)

if __name__ == '__main__' :

    rescue_expts('munyumbwe_calib170116_comparison_1000x')
