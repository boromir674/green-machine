import os
from pypet import Environment, cartesian_product, progressbar

from green_magic import strain_master, clustering_factory, extr_eval, strain_logger
from green_magic.clustering.extrinsic_evaluation import PropertySeparationEvaluation


all_vars = ['type', 'flavors', 'effects', 'medical', 'negatives']
wd = 'new-dt'
strain_master.datasets_dir='/data/projects/knowfly/WIP'
dt = strain_master.load_dataset(wd + '-clean.pk')
qr = strain_master.model_quality



#####  PARAMETERS #####
# this structures defines: 'parameter-name': 'comment'
parameters = {
    'nb_clusters': 'Number of clusters to assume',
    'rowsncolumns': 'Number of rows in the map grid',
    'map_type': 'Map type',
    'grid_type': 'Grid type'
}
init_vals = [20, 20 ,'toroid', 'rectangular']  # per parameter
exploration_ranges = [range(10, 11), range(30, 35, 5), ['toroid'], ['rectangular', 'hexagonal']]  # per parameter

assert len(parameters) == len(init_vals) == len(exploration_ranges)


def make_filename(traj):
    """Function to create generic filenames based on what has been explored"""
    explored_parameters = traj.f_get_explored_parameters()
    return '{}.png'.format('__'.join(map(lambda x: '{}_{}'.format(x.v_name, x.f_get()), explored_parameters.values())))

    # filename = ''
    # for param in explored_parameters.values():
    #     short_name = param.v_name
    #     val = param.f_get()
    #     filename += '%s_%s__' % (short_name, str(val))
    #
    # return filename[:-2] + '.png' # get rid of trailing underscores and add file type


def simulate_type_separation(traj):
    """A sophisticated simulation that involves clustering strain data using self-organizing map model.\n
    :param traj: Trajectory containing the parameters in a particular combination, it also serves as a container for results.
    :type traj: pypet.Trajectory
    """
    som = strain_master.map_manager.get_som('{}.{}'.format('.'.join(str(x) for x in [traj.map_type, traj.grid_type, traj.rowsncolumns, traj.rowsncolumns]), '.pca'))
    clustering = clustering_factory.create_clusters(som, 'kmeans', nb_clusters=traj.nb_clusters, vars=all_vars, ngrams=1)
    # TODO automate adding result
    traj.f_add_result('silhouette', qr.measure(clustering, metric='silhouette').score, comment='Silhouette of clusters score. In range [-1, 1]; higher indicated better defined clusters')
    traj.f_add_result('homogeneity', qr.evaluate(clustering, metric='homogeneity').score, comment='Homogeneity of clusters score. Automatic labeling is used based on dominant feature')
    traj.f_add_result('completeness', qr.evaluate(clustering, metric='completeness').score, comment='Completeness of clusters score. Automatic labeling is used based on dominant feature')
    traj.f_add_result('v_measure', qr.evaluate(clustering, metric='v-measure').score, comment='V-measure of clusters score. Automatic labeling is used based on dominant feature')
    traj.f_add_result('extr_type_separation', extr_eval.evaluate(clustering), comment='Assuming that each cluster should contain mostly strains of one type (indica or sativa or hybrid, measures how well are types separated in clusters by examining distributions')


def gen_parameters(traj_file):
    pass


def get_env(trajectory='test-eval10', filename='/data/projects/knowfly/WIP/example_01.hdf5', file_title='Example_01',  comment='I am a simple example!', large_overview_tables=True):
    # Create an environment that handles running our simulation
    env = Environment(trajectory=trajectory, filename=filename, file_title=file_title, comment=comment, large_overview_tables=large_overview_tables)
    # Get the trajectory from the environment
    traj = env.trajectory
    return env, traj


def load_data(traj, fields):
    assert all(fields in ['silhouette', 'homogeneity', 'completeness', 'v_measure', 'extr_type_separation'])
    traj.f_load(load_data=2)

    strain_logger.info('Printing data')
    for idx, run_name in enumerate(traj.f_iter_runs()):
        filename = os.path.join(folder, make_filename(traj))
        strain_logger.info(filename)  # plot_pattern(traj.crun.pattern, traj.rule_number, filename)
        strain_logger.info('{} {} {}'.format(traj..__get_attribute__(attr)[idx], traj.homogeneity[idx], traj.extr_type_separation[idx]))
        progressbar(idx, len(traj), logger=strain_logger)


class GraphFactory:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.graphs = {}

    def save_graph(self, params):
        pass

    def show_graph(self, params):
        pass


def get_graph_fct():
    return GraphFactory('/data/projects/knowfly/WIP/rep-graphs')


def main():

    # Create an environment that handles running our simulation
    env = Environment(trajectory='test-eval10', filename='/data/projects/knowfly/WIP/example_01.hdf5',
                      file_title='Example_01',
                      comment='I am a simple example!',
                      large_overview_tables=True)

    # Get the trajectory from the environment
    traj = env.trajectory

    for param in
    traj.f_add_parameter('nb_clusters', 20, comment='Number of clusters to assume')
    traj.f_add_parameter('rowsncolumns', 20, comment='Number of rows in the map grid')
    traj.f_add_parameter('map_type', 'toroid', comment='Map type')
    traj.f_add_parameter('grid_type', 'rectangular', comment='Grid type')

    # Explore the parameters with a cartesian product
    params_dct = {
        'nb_clusters': range(10, 11),
        'rowsncolumns': range(30, 40, 5),
        'map_type': ['toroid'],
        'grid_type': ['rectangular', 'hexagonal']
    }
    # params_dct = {
    #     'nb_clusters': range(3, 31),
    #     'rowsxcolumns': range(30, 55, 5),
    #     'map_type': ['toroid', 'planar'],
    #     'grid_type': ['rectangular', 'hexagonal']
    # }
    traj.f_explore(cartesian_product(params_dct))

    # Run the simulation with all parameter combinations
    env.run(simulate_type_separation)

    folder = '/data/projects/knowfly/WIP/'

    try:
        # Load all data
        traj.f_load(load_data=2)

        strain_logger.info('Printing data')
        for idx, run_name in enumerate(traj.f_iter_runs()):
            # Plot all patterns
            filename = os.path.join(folder, make_filename(traj))
            print(filename)  #  plot_pattern(traj.crun.pattern, traj.rule_number, filename)
            print(traj.silhouette[idx], traj.homogeneity[idx], traj.extr_type_separation[idx])
            progressbar(idx, len(traj), logger=strain_logger)
    except RuntimeError as e:
        print(e)

    # Finally disable logging and close all log-files
    env.disable_logging()


if __name__ == '__main__':
    main()
