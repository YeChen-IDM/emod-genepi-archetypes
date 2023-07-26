import numpy as np
from emodpy_malaria.interventions.outbreak import add_outbreak_individual

from run_sims import manifest


def import_infections_through_outbreak(campaign,
                                       days_between_outbreaks,
                                       start_day=1,
                                       num_infections=1,
                                       import_through_travelers_only=False):

    if import_through_travelers_only:
        property_restrictions = [{"TravelerStatus": "IsTraveler"}]
    else:
        property_restrictions = []

    # if outbreak_fraction > 0:
    add_outbreak_individual(campaign=campaign,
                            target_num_individuals=num_infections,
                            repetitions=-1,  # repeats forever
                            timesteps_between_repetitions=days_between_outbreaks,
                            broadcast_event="InfectionDropped",
                            ind_property_restrictions=property_restrictions,
                            start_day=start_day)
    campaign.get_send_trigger("InfectionDropped", old=True)

    return {'number_imported_per_outbreak': num_infections,
            'days_between_importations': days_between_outbreaks}


def constant_annual_importation(campaign, total_importations_per_year):

    if total_importations_per_year <= 365:
        days_between_importations = int(np.round(365/total_importations_per_year))
        num_infections = 1
    else:
        days_between_importations = 1
        num_infections = int(np.round(total_importations_per_year/365))


    import_infections_through_outbreak(campaign,
                                       days_between_outbreaks=days_between_importations,
                                       start_day=1,
                                       num_infections=num_infections)

    return campaign


def build_standard_campaign_object():
    import emod_api.campaign as campaign
    campaign.set_schema(manifest.schema_file)
    return campaign

def build_importation_only_campaign(num_importations_per_year):
    # Only importations, no other interventions
    campaign = build_standard_campaign_object()
    constant_annual_importation(campaign, total_importations_per_year=num_importations_per_year)
    return campaign
