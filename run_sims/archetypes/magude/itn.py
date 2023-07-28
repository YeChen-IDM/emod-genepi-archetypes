import os

import numpy as np
import pandas as pd

from run_sims import manifest
from run_sims.archetypes.maka.maka_campaign import add_bednets_for_population_and_births
from run_sims.other import convert_to_day_365

month_times = [
    0.0,
    30.417,
    60.833,
    91.25,
    121.667,
    152.083,
    182.5,
    212.917,
    243.333,
    273.75,
    304.167,
    334.583
]

old_net_usage = [
    0.9521528827448246,
    0.9968962224187727,
    0.9876766366776979,
    0.9268987891345297,
    0.8304148322138744,
    0.7233898293962878,
    0.6337381726270144,
    0.5848429165167919,
    0.5894569814803964,
    0.6463769214588317,
    0.7407568081902138,
    0.8479803643504683
]
new_net_usage = list(np.array(old_net_usage)*0.7) #new ento showed 30% of indoor biting happens before people go to bed

new_ento_itn_seasonal_dependence = {"Times": month_times, "Values": new_net_usage}

itn_age_dependence = {'youth_cov': 0.9,
                      'youth_min_age': 5,
                      'youth_max_age': 20}

flat_annual_itn_discard_rates = {
    "Expiration_Period_Distribution": "CONSTANT_DISTRIBUTION",
    "Expiration_Period_Constant": 365 * 3  # distributions every 3 years
}

fast_discarding_itn_discard_rates = {
    "Expiration_Period_Distribution": "DUAL_EXPONENTIAL_DISTRIBUTION",
    "Expiration_Period_Mean_1": 260,
    "Expiration_Period_Mean_2": 2106,
    "Expiration_Period_Proportion_1": 0.6
}

slow_discard_rates = {
    "Expiration_Period_Distribution": "EXPONENTIAL_DISTRIBUTION",
    "Expiration_Period_Exponential": 2500
}

# net_type_flag:
# 0: constant killing/blocking, no discarding. only for historical bednet distributions
# 1: waning killing/blocking, fast discarding
# 2: waning killing/blocking, slow discarding
discard_config_dict = {
    0: flat_annual_itn_discard_rates,
    1: fast_discarding_itn_discard_rates,
    2: slow_discard_rates
}

def add_itn(campaign, sim_start_date):
    df = pd.read_csv(os.path.join(manifest.magude_archetype_folder, "itn_magude.csv"))

    # Add simday column for adding to campaign file
    df['simday'] = [convert_to_day_365(x, sim_start_date, "%Y-%m-%d") for x in df.fulldate]

    for index, row in df.iterrows():
        net_type = row["net_type_flag"]

        killing_initial_effect = row["initial_killing"]
        blocking_initial_effect = row["initial_blocking"]
        killing_decay_time_constant = 781
        blocking_decay_time_constant = 2046

        if net_type == 0:
            killing_box_duration = 3*365
            blocking_box_duration = 3*365
        else:
            killing_box_duration = 0
            blocking_box_duration = 0

        add_bednets_for_population_and_births(campaign,
                                              start_day=row["simday"],
                                              coverage=row["cov_all"],
                                              seasonal_dependence=new_ento_itn_seasonal_dependence,
                                              age_dependence=itn_age_dependence,
                                              discard_config=discard_config_dict[row["net_type_flag"]],
                                              killing_initial_effect=killing_initial_effect,
                                              killing_box_duration=killing_box_duration,
                                              killing_decay_time_constant=killing_decay_time_constant,
                                              blocking_initial_effect=blocking_initial_effect,
                                              blocking_box_duration=blocking_box_duration,
                                              blocking_decay_time_constant=blocking_decay_time_constant,
                                              include_birthnets=True,
                                              birthnet_listening_duration=row["birthnet_listening_duration"],
                                              )
