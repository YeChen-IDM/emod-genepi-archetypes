import itertools
from typing import List, Optional, Union

from emodpy.emod_task import EMODTask
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

from run_sims.sweeps.historical_archetype_sweeps import master_sweep_over_historical_scenarios
from run_sims.sweeps.other_sweeps import set_log10_x_larval_habitat, set_max_individual_infections, set_run_number

from run_sims import manifest
from run_sims.build_config import set_full_config
from run_sims.helpers import include_post_processing
from run_sims.reports import add_default_reports
from run_sims.sweeps.toy_archetype_sweeps import master_sweep_over_toy_scenarios

# possible archetypes: test, flat, maka_like, magude_like, maka_historical, magude_historical


# test_archetypes = ["test"]
toy_archetypes = ["test", "flat", "maka_like", "magude_like"]
historical_archetypes = ["maka_historical", "magude_historical"]


def create_and_run_sim_sweep(archetypes: Union[List[str], str] = "flat",
                             pop_sizes_in_thousands: Union[List[int], int] = 10,
                             importations_per_year_per_1000: Union[List[int], int] = 0,
                             target_prevalences: Union[List[float], float] = 0.05,
                             max_num_infections: Union[List[int], int] = 3,
                             number_of_seeds: int = 1,
                             comps_node_group: str = "idm_abcd",
                             comps_run_priority: str = "Normal",
                             experiment_name: Optional[str] = None,
                             exp_id_filepath: str = manifest.exp_id_file,
                             run_exp: bool = True) -> Experiment:

    """
    Submit and run Emod experiment in Comps
    Args:
        archetypes:                      list of values for Archetypes: test, flat, maka_like, magude_like, maka_historical, magude_historical.
        pop_sizes_in_thousands:          list of values for population size in thousands (possible values are 1k,10k,20k,50k,100k).
        importations_per_year_per_1000:  list of values for importation rate per 1000 people in population.
        target_prevalences:              list of values for target (RDT) prevalence for test/flat/maka_like/magude_like scenarios,
                                         (possible values are 5%, 10%, 20%, 30%, 40%).
        max_num_infections:              list of values for maximum number of concurrent infections to sweep.
        number_of_seeds:                 number of simulation replicates.
        comps_node_group:                comps node_group.
        comps_run_priority:              comps job priority.
        experiment_name:                 comps experiment name.
        exp_id_filepath:                 emod experiment id file path.
        run_exp:                         For test purpose, set it to False to skip running experiment on Comps.

    Returns: Comps experiment object

    """
    historical_archetype_flag = False
    test_flag = False

    def _to_list_if_not(input_data):
        if not isinstance(input_data, list) and input_data is not None:
            input_data = [input_data]
        return input_data
    archetypes = _to_list_if_not(archetypes)
    pop_sizes_in_thousands = _to_list_if_not(pop_sizes_in_thousands)
    importations_per_year_per_1000 = _to_list_if_not(importations_per_year_per_1000)
    target_prevalences = _to_list_if_not(target_prevalences)
    max_num_infections = _to_list_if_not(max_num_infections)

    if set(archetypes).intersection(set(toy_archetypes)) and set(archetypes).intersection(set(historical_archetypes)):
        raise ValueError("Cannot mix toy and historical archetypes, since one requires target_prevalence to be set and the other ignores it.")

    for a in archetypes:
        if a in historical_archetypes and target_prevalences is not None:
            raise ValueError("Cannot set target_prevalence if running a historical archetype! Either remove target_prevalence keyword or change to one of the toy archetypes: flat, maka_like, or magude_like")
        if a in toy_archetypes and target_prevalences is None:
            raise ValueError("Must set target_prevalence if running a toy archetype! Either add target_prevalence keyword or change to one of the historical archetypes: maka_historical or magude_historical")

        if a in historical_archetypes:
            historical_archetype_flag = True

    # # If toy archetype, the campaign file is just for importations. Conversely, historical archetypes have extensive campaign files.
    # num_importations_per_year = importations_per_year_per_1000 * pop_size_in_thousands
    # if archetype == "maka_historical":
    #     campaign_builder = partial(build_historical_campaign, archetype=archetype, num_importations_per_year=num_importations_per_year)
    # elif archetype == "magude_historical":
    #     raise NotImplementedError("Magude historical archetype not yet implemented")
    # elif archetype in toy_archetypes:
    #     if importations_per_year_per_1000 > 0:
    #         campaign_builder = partial(build_importation_only_campaign, num_importations_per_year=importations_per_year_per_1000*pop_size_in_thousands)
    #     else:
    #         print("Note: Importation rate set to 0!")
    #         campaign_builder = None

    # Set up experiment
    if archetypes == ["test"]:
        test_flag = True
        comps_node_group = "idm_48cores"
        comps_run_priority = "Highest"

    platform = Platform("Calculon", num_cores=1, node_group=comps_node_group, priority=comps_run_priority)
    task = EMODTask.from_default2(
        eradication_path=manifest.eradication_path,
        schema_path=manifest.schema_file,
        param_custom_cb=set_full_config,
        ep4_custom_cb=include_post_processing
    )
    task.common_assets.add_directory(assets_directory=manifest.assets_input_dir)
    task.set_sif(manifest.sif)
    add_default_reports(task, include_debugging_reports=test_flag)

    builder = SimulationBuilder()
    builder.add_sweep_definition(set_run_number, range(number_of_seeds))
    builder.add_sweep_definition(set_max_individual_infections, max_num_infections)
    if historical_archetype_flag:
        sweep_values = list(itertools.product(archetypes, pop_sizes_in_thousands, importations_per_year_per_1000))
        builder.add_sweep_definition(master_sweep_over_historical_scenarios, sweep_values)
    else:
        sweep_values = list(itertools.product(archetypes, target_prevalences, pop_sizes_in_thousands, importations_per_year_per_1000))
        builder.add_sweep_definition(master_sweep_over_toy_scenarios, sweep_values)
    # builder.add_sweep_definition(set_log10_x_larval_habitat, [round(x * 0.1, 1) for x in range(-12, -9)]) # TESTING ONLY

    if experiment_name is None:
        print("No experiment name provided. Using default name: mpg e2e test")
        experiment_name = "mpg e2e test"
    experiment = Experiment.from_builder(builder, task, name=experiment_name)

    if run_exp:
        experiment.run(wait_until_done=True, platform=platform)

        # Check result
        if not experiment.succeeded:
            print(f"Experiment {experiment.uid} failed.\n")
            exit()
        print(f"Experiment {experiment.uid} succeeded.")

    # Save experiment id to file
    with open(exp_id_filepath, "w") as fd:
        print(f"writing to {exp_id_filepath}...")
        fd.write(str(experiment.uid))
    print(str(experiment.uid))
    return experiment


if __name__ == "__main__":
    # create_and_run_single_run(archetype="maka_like", pop_size_in_thousands=1, target_prevalence=0.2, importations_per_year_per_1000=100)
    # create_and_run_sim_sweep(archetypes=["maka_like", "flat"],
    #                          pop_sizes_in_thousands=1,
    #                          importations_per_year_per_1000=[200, 400],
    #                          target_prevalences=[0.2, 0.4],
    #                          max_num_infections=3,
    #                          number_of_seeds=1,
    #                          experiment_name="mpg e2e test")
    # create_and_run_sim_sweep(archetypes=["magude_historical"],
    #                          pop_sizes_in_thousands=[1,10,50],
    #                          importations_per_year_per_1000=[50],
    #                          max_num_infections=3,
    #                          number_of_seeds=5,
    #                          experiment_name="mpg e2e test")
    create_and_run_sim_sweep(archetypes=["flat"],
                             pop_sizes_in_thousands=[1,10,50],
                             importations_per_year_per_1000=[50],
                             target_prevalences=[0.05],
                             max_num_infections=[3],
                             number_of_seeds=5,
                             experiment_name="mpg e2e test")