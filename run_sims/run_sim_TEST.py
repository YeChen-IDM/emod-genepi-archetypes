from functools import partial

from emodpy.emod_task import EMODTask
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

from run_sims import manifest
from run_sims.archetypes.archetype_campaigns import build_historical_campaign
from run_sims.build_config import set_full_config
from run_sims.importations import build_importation_only_campaign
from run_sims.other import include_post_processing
from run_sims.reports import add_default_reports
from run_sims.sweeps import set_archetype, \
    set_log10_x_larval_habitat, set_population_size_in_thousands, set_target_prevalence
from run_sims.sweeps.other_sweeps import set_max_individual_infections, set_run_number, set_sim_tag

# possible archetypes: test, flat, maka_like, magude_like, maka_historical, magude_historical


# test_archetypes = ["test"]
toy_archetypes = ["test", "flat", "maka_like", "magude_like"]
historical_archetypes = ["maka_historical", "magude_historical"]
def create_and_run_single_run(archetype="flat",
                              pop_size_in_thousands=10,
                              importations_per_year_per_1000=0,
                              target_prevalence=None,
                              max_num_infections=3,
                              number_of_seeds=1,
                              comps_node_group="idm_abcd",
                              comps_run_priority="Normal",
                              experiment_name=None):
    # Initial checks
    if archetype not in toy_archetypes and archetype not in historical_archetypes:
        raise NotImplementedError("Unsupported archetype")

    if archetype in historical_archetypes and target_prevalence is not None:
        raise ValueError("Cannot set target_prevalence if running a historical archetype! Either remove target_prevalence keyword or change to one of the toy archetypes: flat, maka_like, or magude_like")
    elif archetype in toy_archetypes and target_prevalence is None:
        raise ValueError("Must set target_prevalence if running a toy archetype! Either add target_prevalence keyword or change to one of the historical archetypes: maka_historical or magude_historical")

    # If toy archetype, the campaign file is just for importations. Conversely, historical archetypes have extensive campaign files.
    num_importations_per_year = importations_per_year_per_1000 * pop_size_in_thousands
    if archetype == "maka_historical":
        campaign_builder = partial(build_historical_campaign, archetype=archetype, num_importations_per_year=num_importations_per_year)
    elif archetype == "magude_historical":
        raise NotImplementedError("Magude historical archetype not yet implemented")
    elif archetype in toy_archetypes:
        if importations_per_year_per_1000 > 0:
            campaign_builder = partial(build_importation_only_campaign, num_importations_per_year=importations_per_year_per_1000*pop_size_in_thousands)
        else:
            print("Note: Importation rate set to 0!")
            campaign_builder = None

    # Set up experiment
    if archetype == "test":
        comps_node_group = "idm_48cores"
        comps_run_priority = "Highest"

    platform = Platform("Calculon", num_cores=1, node_group=comps_node_group, priority=comps_run_priority)
    task = EMODTask.from_default2(
        eradication_path=manifest.eradication_path,
        schema_path=manifest.schema_file,
        param_custom_cb=set_full_config,
        campaign_builder=campaign_builder,
        ep4_custom_cb=include_post_processing
    )
    task.common_assets.add_directory(assets_directory=manifest.assets_input_dir)
    task.set_sif(manifest.sif)
    add_default_reports(task, include_debugging_reports=(archetype=="test"))

    builder = SimulationBuilder()
    builder.add_sweep_definition(set_archetype, [archetype])
    builder.add_sweep_definition(set_population_size_in_thousands, [pop_size_in_thousands])
    if target_prevalence is not None:
        builder.add_sweep_definition(partial(set_target_prevalence, archetype=archetype), [target_prevalence])
    builder.add_sweep_definition(set_run_number, range(number_of_seeds))
    builder.add_sweep_definition(set_max_individual_infections, [max_num_infections])
    # Add this here so importation is also a COMPS sim tag
    builder.add_sweep_definition(partial(set_sim_tag, tag_name="importations_per_year_per_1000"), [importations_per_year_per_1000])

    if experiment_name is None:
        print("No experiment name provided. Using default name: mpg e2e test")
        experiment_name = "mpg e2e test"
    experiment = Experiment.from_builder(builder, task, name=experiment_name)

    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()
    print(f"Experiment {experiment.uid} succeeded.")


if __name__ == "__main__":
    # create_and_run_single_run(archetype="maka_like", pop_size_in_thousands=1, target_prevalence=0.2, importations_per_year_per_1000=100)
    create_and_run_single_run(archetype="maka_historical", pop_size_in_thousands=1, importations_per_year_per_1000=200)