import os

import pandas as pd
from emodpy_malaria.interventions.drug_campaign import add_drug_campaign

from run_sims import manifest
from run_sims.helpers import convert_to_day_365


def add_mda(campaign, sim_start_date):
    df = pd.read_csv(os.path.join(manifest.magude_archetype_folder, "mda_magude.csv"))

    # Add simday column for adding to campaign file
    df['simday'] = [convert_to_day_365(x, sim_start_date, "%Y-%m-%d") for x in df.fulldate]

    for i, row in df.iterrows():
        add_drug_campaign(campaign,
                          start_days=[row.simday],
                          coverage=row.cov_all,
                          campaign_type="MDA",
                          drug_code="DP",
                          repetitions=1)