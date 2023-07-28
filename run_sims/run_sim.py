import argparse
from functools import partial
from typing import Optional

from emodpy.emod_task import EMODTask
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

from run_sims import manifest
from run_sims.build_config import set_full_config
from run_sims.other import build_demographics_from_file, include_post_processing
from run_sims.reports import add_default_reports
from run_sims.sweeps import set_habitat_scale
from run_sims.sweeps.other_sweeps import set_max_individual_infections, set_run_number


def create_and_submit_experiment(exp_id_file: str = manifest.exp_id_file,
                                 archetype: Optional[str] = "flat", #flat, maka, magude
                                 prevalence: Optional[float] = -1,
                                 importation_seasonality: Optional[bool] = False,
                                 importations_per_thousand_per_year: Optional[int] = 0,
                                 population_size: Optional[int] = 10000, #1k, 10k, 100k??
                                 max_individual_infections: Optional[float] = None,
                                 test_run: bool = True,
                                 experiment_name: str = "Emod_genepi_archetypes",
                                 reporting_interval = 30):
    """fixme Update docstring
    Submit and run Emod experiment in Comps
    Args:
        exp_id_file:                   Filepath of experiment id.
        test_run:                      If set to True, the sims have 1k individuals and are 3-year sims with the reports
                                       beginning after 1 year, and sims are submitted to the node_group idm_48cores.
                                       Otherwise, the sims have 10k individuals and are 40 years long, with reports
                                       starting after 30 years, and sims are submitted to node_group idm_abcd.
        experiment_name:               Name of experiment in Comps.
        max_individual_infections:     The maximum number of concurrent infections an individual in the simulation can have.
        larval_habitat_scales:         The log10 of the maximum larval habitat (increasing this increases the
                                       transmission intensity).
        number_of_seeds:               Number of simulation replicates.
        reporting_interval:            Reporting interval for ReportInfectionStatsMalaria.

    Returns: Comps id for experiment

    """

    if test_run:
        platform = Platform(manifest.platform_name, num_cores=1, node_group="idm_48cores", priority="AboveNormal")
    else:
        platform = Platform(manifest.platform_name, num_cores=1, node_group="idm_abcd", priority="Normal")

    # =========================================================

    build_config = partial(set_full_config,
                           test_run=test_run,
                           archetype=archetype,
                           prevalence=prevalence,
                           population_size=population_size)

    print("Creating EMODTask (from files)...")
    task = EMODTask.from_default2(
        config_path="config.json",
        eradication_path=manifest.eradication_path,
        campaign_builder=None,
        schema_path=manifest.schema_file,
        param_custom_cb=build_config,
        demog_builder=None,
        ep4_custom_cb=include_post_processing
    )

    # Add demographics, reporter, assets
    demographics_callback = partial(build_demographics_from_file, test_run=test_run)
    task.create_demog_from_callback(demographics_callback)

    add_default_reports(task, test_run=test_run, reporting_interval=reporting_interval)
    task.common_assets.add_directory(assets_directory=manifest.assets_input_dir)
    task.set_sif(manifest.sif)

    # Create simulation sweeps
    builder = SimulationBuilder()
    builder.add_sweep_definition(set_habitat_scale, larval_habitat_scales)
    builder.add_sweep_definition(set_max_individual_infections, max_individual_infections)
    builder.add_sweep_definition(set_run_number, range(number_of_seeds))

    # create experiment from builder
    print("Prompting for COMPS creds if necessary...")
    experiment = Experiment.from_builder(builder, task, name=experiment_name)
    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()

    # Save experiment id to file
    with open(exp_id_file, "w") as fd:
        fd.write(experiment.uid.hex)
    print(experiment.uid.hex)

    print(f"Experiment {experiment.uid} succeeded.")
    return experiment.uid.hex


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
    create_and_submit_experiment(exp_id_file=args.exp_id_filepath, test_run=args.test_run,
                                 experiment_name=args.exp_name,
                                 max_individual_infections=args.max_individual_infections,
                                 larval_habitat_scales=args.larval_habitat_scales,
                                 number_of_seeds=args.seeds, reporting_interval=args.reporting_interval)
