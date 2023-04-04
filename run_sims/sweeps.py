
import numpy as np
import pandas as pd
import os

from emodpy_malaria.reporters.builtin import add_report_vector_stats

from run_sims import manifest
from run_sims.build_config import set_ento


def set_run_number(simulation, value):
    simulation.task.config.parameters.Run_Number = value
    return {"Run_Number": value}



def set_habitat_scale(simulation, value):
    habitat_scale = value

    set_ento(simulation.task.config,
             habitat_scale=habitat_scale
             )

    return {"habitat_scale": habitat_scale}


def set_max_individual_infections(simulation, value):
    max_individual_infections = value

    simulation.task.config.parameters.Max_Individual_Infections = max_individual_infections
    # Scale antigenic space linearly with max_individual_infections
    simulation.task.config.parameters.Falciparum_MSP_Variants = int(np.round(32*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_Nonspecific_Types = int(np.round(76*max_individual_infections/3))
    simulation.task.config.parameters.Falciparum_PfEMP1_Variants = int(np.round(1070*max_individual_infections/3))

    return {"max_individual_infections": max_individual_infections}

