from run_sims.archetypes.magude.magude_campaign import build_full_magude_campaign
from run_sims.archetypes.maka.maka_campaign import build_full_maka_campaign
from run_sims.importations import constant_annual_importation

#
# def build_historical_campaign(archetype, num_importations_per_year):
#     if archetype == "maka_historical":
#         campaign = build_full_maka_campaign()
#
#     elif archetype == "magude_historical":
#         campaign = build_full_magude_campaign()
#     else:
#         raise NotImplementedError("Archetype {} not implemented".format(archetype))
#
#     # Assumed that above campaigns do not include importations
#     constant_annual_importation(campaign, total_importations_per_year=num_importations_per_year)
#
#     return campaign