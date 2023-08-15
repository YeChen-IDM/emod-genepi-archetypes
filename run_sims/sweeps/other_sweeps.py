import os

import numpy as np
import pandas as pd

from run_sims import manifest
from run_sims.build_config import set_ento, set_non_ento_archetype_config_params


def set_sim_tag(simulation, tag_name, tag_value):
    return {tag_name: tag_value}


def set_run_number(simulation, value):
    simulation.task.config.parameters.Run_Number = value
    return {"Run_Number": value}


def set_max_individual_infections(simulation, value):
    max_individual_infections = value

    simulation.task.config.parameters.Max_Individual_Infections = max_individual_infections
    # Scale antigenic space linearly with max_individual_infections
    simulation.task.config.parameters.Falciparum_MSP_Variants = int(np.round(32*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_Nonspecific_Types = int(np.round(76*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_PfEMP1_Variants = int(np.round(1070*max_individual_infections/3))

    return {"max_individual_infections": max_individual_infections}


def set_population_size_in_thousands(simulation, value):
    if value in [1,10,20,50,100]:
        simulation.task.config.parameters.Demographics_Filenames = [f"demo_{value}k.json"]
    else:
        # todo: Create demographics file on the fly using emodpy so we can use any input population size
        raise NotImplementedError("Population size {}k not implemented. Please select from [1k,10k,20k,50k,100k]".format(value))
    return {"population_size_in_thousands": value}


def set_archetype(simulation, value):
    archetype = value
    set_non_ento_archetype_config_params(simulation.task.config, archetype=archetype)
    if archetype == "test":
        archetype = "flat"
    set_ento(simulation.task.config, archetype=archetype)
    return {"archetype": archetype}


def set_target_prevalence(simulation, archetype, target_rdt_prev):
    # Use lookup table to set larval habitat scale based on desired prevalence level
    df = pd.read_csv(os.path.join(manifest.additional_csv_folder, "prevalence_lookup.csv"))
    if archetype == "test": # Treat test archetype same as flat
        archetype = "flat"
    if target_rdt_prev in [0.05,0.1,0.2,0.3,0.4]:
        cut = np.logical_and(df["archetype"] == archetype,df["target_rdt_prevalence"] == target_rdt_prev)
        log10_x_larval_habitat = df.loc[cut, "log10_x_larval_habitat"].values[0]
    else:
        raise ValueError("Target prevalence {} not implemented. Please select from [0.05,0.1,0.2,0.3,0.4]".format(target_rdt_prev))
    simulation.task.config.parameters.x_Temporary_Larval_Habitat = 10 ** log10_x_larval_habitat
    return {"target_rdt_prevalence": target_rdt_prev}


def set_log10_x_larval_habitat(simulation, value):
    simulation.task.config.parameters.x_Temporary_Larval_Habitat = 10**value
    return {"log10_x_larval_habitat": value}


# def lookup_x_larval_habitat_from_target_prevalence(archetype, target_rdt_prevalence):
#     df = pd.read_csv(os.path.join(manifest.additional_csv_folder, "prevalence_lookup.csv"))
#     return df.loc[np.logicaldf["target_rdt_prevalence"] == target_rdt_prevalence, "log10_x_larval_habitat"].values[0]
