from functools import partial

from emodpy.emod_task import EMODTask
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

from run_sims import manifest
from run_sims.build_config import set_full_config
from run_sims.helpers import include_post_processing
from run_sims.reports import add_default_reports
from run_sims.sweeps.other_sweeps import set_run_number, set_archetype, set_log10_x_larval_habitat, set_population_size_in_thousands


# Sweep over larval habitat to reach target prevalence for each of the sites


def create_and_submit_experiment():
    # ========================================================
    experiment_name = "e2e habitat sweep"

    # parameters to sweep over:
    # archetypes=["flat","maka","magude"]
    archetypes=["magude", "maka"]
    pop_sizes = [1]
    # log10_x_larval_habitats = [round(x * 0.1, 1) for x in range(-26, 15)]
    log10_x_larval_habitats = [round(x * 0.1, 1) for x in range(0, 18)]
    # log10_x_larval_habitats = [round(x * 0.1, 1) for x in range(-15, 16)]
    # log10_x_larval_habitats = [round(x * 0.1, 1) for x in range(18, 26)]
    # larval_habitat_scales = [7.0,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,
    #                          8.0,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,8.9,
    #                          9.0,9.1,9.2,9.3,9.4,9.5,9.6,9.7,9.8,9.9,
    #                          10.0,10.1,10.2,10.3,10.4,10.5,10.6,10.7]
    number_of_seeds = 4

    platform = Platform("Calculon", num_cores=1, node_group="idm_abcd", priority="Normal")
    # platform = Platform("Calculon", num_cores=1, node_group="idm_cd", priority="BelowNormal")
    # platform = Platform("Calculon", num_cores=1, node_group="idm_48cores", priority="Highest")

    # =========================================================

    build_config = partial(set_full_config, test_run=False)

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

    print("Adding asset dir...")
    task.common_assets.add_directory(assets_directory=manifest.assets_input_dir)
    task.set_sif(manifest.sif)

    add_default_reports(task)

    # Create simulation sweep with builder
    builder = SimulationBuilder()
    builder.add_sweep_definition(set_archetype, archetypes)
    builder.add_sweep_definition(set_population_size_in_thousands, pop_sizes)
    builder.add_sweep_definition(set_log10_x_larval_habitat, log10_x_larval_habitats)
    builder.add_sweep_definition(set_run_number, range(number_of_seeds))

    # create experiment from builder
    print("Prompting for COMPS creds if necessary...")
    experiment = Experiment.from_builder(builder, task, name=experiment_name)
    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()

    print(f"Experiment {experiment.uid} succeeded.")


if __name__ == "__main__":
    create_and_submit_experiment()