from functools import partial

from run_sims.build_config import set_ento, set_non_ento_archetype_config_params
from run_sims.importations import build_importation_only_campaign, get_actual_number_imports_from_target_number
from run_sims.sweeps.other_sweeps import set_target_prevalence


def master_sweep_over_toy_scenarios(simulation, value):
    # Need to do this as a single sweep since setup depends on multiple parameters together
    archetype = value[0]
    target_rdt_prevalence = value[1]
    population_size_in_thousands = value[2]
    importations_per_year_per_thousand = value[3]

    # ==============
    # CONFIG SETUP =
    # ==============
    set_non_ento_archetype_config_params(simulation.task.config, archetype=archetype)
    if archetype == "test":
        archetype = "flat"
    set_ento(simulation.task.config, archetype=archetype)
    set_target_prevalence(simulation, archetype=archetype, target_rdt_prev=target_rdt_prevalence)

    # Set demographics file based on population size
    if population_size_in_thousands in [1,10,20,50,100]:
        simulation.task.config.parameters.Demographics_Filenames = [f"demo_{population_size_in_thousands}k.json"]
    else:
        # todo: Create demographics file on the fly using emodpy so we can use any input population size
        raise NotImplementedError("Population size {}k not implemented. Please select from [1k,10k,20k,50k,100k]".format(population_size_in_thousands))

    # ================
    # CAMPAIGN SETUP =
    # ================
    # Campaign only has importations, no interventions
    campaign_builder = partial(build_importation_only_campaign,
                               num_importations_per_year=importations_per_year_per_thousand * population_size_in_thousands)
    simulation.task.create_campaign_from_callback(campaign_builder)

    # Non-schema config parameter, so we can find it with dtk_post_process
    simulation.task.config["archetype"] = archetype

    return {"archetype": archetype,
            "target_rdt_prevalence": target_rdt_prevalence,
            "population_size_in_thousands": population_size_in_thousands,
            "target_num_importations_per_year_per_thousand": importations_per_year_per_thousand,
            "actual_num_importations_per_year_per_thousand": get_actual_number_imports_from_target_number(importations_per_year_per_thousand * population_size_in_thousands)[2]}
