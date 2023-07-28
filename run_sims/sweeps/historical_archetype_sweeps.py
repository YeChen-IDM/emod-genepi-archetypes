from functools import partial

from run_sims.archetypes.magude.magude_campaign import build_full_magude_campaign
from run_sims.archetypes.maka.maka_campaign import build_full_maka_campaign
from run_sims.build_config import set_ento, set_non_ento_archetype_config_params
from run_sims.importations import constant_annual_importation, get_actual_number_imports_from_target_number


def master_sweep_over_historical_scenarios(simulation, value):
    # Need to do this as a single sweep since setup depends on multiple parameters together
    archetype = value[0]
    population_size_in_thousands = value[1]
    importations_per_year_per_thousand = value[2]

    # ==============
    # CONFIG SETUP =
    # ==============
    set_non_ento_archetype_config_params(simulation.task.config, archetype=archetype)
    set_ento(simulation.task.config, archetype=archetype)

    # Set demographics file based on population size
    if population_size_in_thousands in [1,10,20,50,100]:
        simulation.task.config.parameters.Demographics_Filenames = [f"demo_{population_size_in_thousands}k.json"]
    else:
        # todo: Create demographics file on the fly using emodpy so we can use any input population size
        raise NotImplementedError("Population size {}k not implemented. Please select from [1k,10k,20k,50k,100k]".format(population_size_in_thousands))

    # ================
    # CAMPAIGN SETUP =
    # ================
    def _campaign_builder(archetype):
        if archetype == "maka_historical":
            campaign = build_full_maka_campaign()
        elif archetype == "magude_historical":
            campaign = build_full_magude_campaign(population_size=population_size_in_thousands*1000)
        else:
            raise NotImplementedError("Archetype {} not implemented".format(archetype))

        # Assumed that above campaigns do not include importations
        num_importations_per_year = importations_per_year_per_thousand * population_size_in_thousands
        constant_annual_importation(campaign, total_importations_per_year_target=num_importations_per_year)
        return campaign

    campaign_builder = partial(_campaign_builder, archetype=archetype)
    simulation.task.create_campaign_from_callback(campaign_builder)

    return {"archetype": archetype,
            "population_size_in_thousands": population_size_in_thousands,
            "importations_per_year_per_thousand": importations_per_year_per_thousand,
            "actual_num_importations_per_year_per_thousand": get_actual_number_imports_from_target_number(
                importations_per_year_per_thousand * population_size_in_thousands)[2]}
