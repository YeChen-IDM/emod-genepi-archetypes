import argparse
from functools import partial

from emodpy.emod_task import EMODTask
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

from run_sims import manifest
from run_sims.build_config import set_full_config
from run_sims.other import build_demographics_from_file, include_post_processing
from run_sims.reports import add_default_reports
from run_sims.sweeps import set_habitat_scale, set_max_individual_infections, set_run_number


def create_and_submit_experiment(exp_id_file: str = None):
    # ========================================================
    experiment_name = "emod_MPG"

    # parameters to sweep over:
    max_individual_infections = [3,6,9]
    larval_habitat_scales = [6.5,7.0,7.5]
    number_of_seeds = 1
    test_run = True

    if test_run:
        platform = Platform(manifest.platform_name, num_cores=1, node_group="idm_48cores", priority="AboveNormal")
    else:
        platform = Platform(manifest.platform_name, num_cores=1, node_group="idm_abcd", priority="Normal")

    # =========================================================

    build_config = partial(set_full_config, test_run=test_run)

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

    add_default_reports(task, test_run=test_run)
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
    parser.add_argument('--exp_id_filepath', '-i', type=str, help='Emod experiment id file',
                        default=manifest.exp_id_file)
    args = parser.parse_args()
    create_and_submit_experiment(args.exp_id_filepath)
