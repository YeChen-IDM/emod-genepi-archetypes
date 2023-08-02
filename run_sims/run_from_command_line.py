import argparse

from run_sims import manifest
from run_sims.create_sim_sweeps import create_and_run_sim_sweep

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emod experiment id file')
    parser.add_argument('--exp_id_filepath', '-i', type=str,
                        help='emod experiment id file (default to manifest.exp_id_file)',
                        default=manifest.exp_id_file)
    parser.add_argument('--test_run', '-t', help='test_run flag (default to True)', action='store_false')
    parser.add_argument('--exp_name', '-e', type=str,
                        help='emod experiment name in Comps (default to emod_genepi_archetypes)',
                        default='emod_genepi_archetypes')
    parser.add_argument('--max_individual_infections', '-m', nargs='+', type=int,
                        help='list of values for maximum number of concurrent infections to sweep '
                             '(default to [3, 6, 9])',
                        default=[3, 6, 9])
    parser.add_argument('--larval_habitat_scales', '-l', nargs='+', type=float,
                        help='list of values for the log10 of the maximum larval habitat to sweep '
                             '(default to [6.5, 7.0, 7.5])',
                        default=[6.5, 7.0, 7.5])
    parser.add_argument('--seeds', '-s', type=int, help='number of simulation replicates (default to 1)',
                        default=1)
    parser.add_argument('--reporting_interval', '-r', type=int,
                        help='reporting interval for ReportInfectionStatsMalaria (default to 30 days)', default=30)
    args = parser.parse_args()
    # create_and_submit_experiment(exp_id_file=args.exp_id_filepath, test_run=args.test_run,
    #                              experiment_name=args.exp_name,
    #                              max_individual_infections=args.max_individual_infections,
    #                              larval_habitat_scales=args.larval_habitat_scales,
    #                              number_of_seeds=args.seeds, reporting_interval=args.reporting_interval)


    create_and_run_sim_sweep(archetypes=["magude_historical"],
                             pop_sizes_in_thousands=[1,10,50],
                             importations_per_year_per_1000=[50],
                             max_num_infections=3,
                             number_of_seeds=5,
                             experiment_name="mpg e2e test")