from emodpy_malaria.interventions.drug_campaign import add_drug_campaign

from run_sims.other import convert_to_day_365


def add_rcd(campaign, sim_start_date, population_size):
    start_day = convert_to_day_365("2017-06-01", sim_start_date, "%Y-%m-%d")

    number_in_rcd_sweep = 8 #6 in HH, inflated by ~30% because of higher risk in HH compared to population

    add_drug_campaign(campaign,
                      campaign_type='rfMDA',
                      drug_code='AL',
                      start_days=[start_day],
                      coverage=number_in_rcd_sweep/population_size,
                      trigger_coverage=0.8)

