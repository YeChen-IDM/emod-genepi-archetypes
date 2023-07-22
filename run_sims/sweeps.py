
import numpy as np

from run_sims.build_config import set_ento


def set_run_number(simulation, value):
    simulation.task.config.parameters.Run_Number = value
    return {"Run_Number": value}

def set_archetype(simulation, value):
    archetype = value
    set_ento(simulation.task.config, archetype=archetype)
    return {"archetype": archetype}

def set_log10_x_larval_habitat(simulation, value):
    simulation.task.config.parameters.x_Temporary_Larval_Habitat = 10**value
    return {"log10_x_larval_habitat": value}

def set_population_size_in_thousands(simulation, value):
    if value in [1,10,20,50,100]:
        simulation.task.config.parameters.Demographics_Filenames = [f"demo_{value}k.json"]
    else:
        # todo: Create demographics file on the fly using emodpy so we can use any input population size
        raise NotImplementedError("Population size {}k not implemented. Please select from [1k,10k,20k,50k,100k]".format(value))
    return {"population_size_in_thousands": value}

def set_prevalence_level(simulation, value):
    # Use lookup table to set larval habitat scale based on desired prevalence level
    raise NotImplementedError



def set_max_individual_infections(simulation, value):
    max_individual_infections = value

    simulation.task.config.parameters.Max_Individual_Infections = max_individual_infections
    # Scale antigenic space linearly with max_individual_infections
    simulation.task.config.parameters.Falciparum_MSP_Variants = int(np.round(32*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_Nonspecific_Types = int(np.round(76*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_PfEMP1_Variants = int(np.round(1070*max_individual_infections/3))

    return {"max_individual_infections": max_individual_infections}

