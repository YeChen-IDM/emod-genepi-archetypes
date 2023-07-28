import os

import pandas as pd
from emodpy_malaria.interventions.irs import add_scheduled_irs_housing_modification

from run_sims import manifest
from run_sims.other import convert_to_day_365


def add_irs(campaign, sim_start_date):
    df = pd.read_csv(os.path.join(manifest.magude_archetype_folder, "irs_magude.csv"))

    # Add simday column for adding to campaign file
    df['simday'] = [convert_to_day_365(x, sim_start_date, "%Y-%m-%d") for x in df.fulldate]

    for i, row in df.iterrows():
        add_scheduled_irs_housing_modification(campaign,
                                               start_day=row.simday,
                                               demographic_coverage=row.cov_all,
                                               killing_initial_effect=row.killing,
                                               killing_decay_time_constant=row.exp_duration,
                                               killing_box_duration=row.box_duration)