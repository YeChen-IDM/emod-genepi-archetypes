from run_sims import manifest
from run_sims.archetypes.magude.hs import add_hs
from run_sims.archetypes.magude.irs import add_irs
from run_sims.archetypes.magude.itn import add_itn
from run_sims.archetypes.magude.mda import add_mda
from run_sims.archetypes.magude.rcd import add_rcd



def add_custom_events(campaign):
    # Add to custom events (used to do this by directly editing config.parameters.Custom_Individual_Events
    campaign.get_send_trigger("Received_Treatment", old=True)
    campaign.get_send_trigger("Received_Test", old=True)
    campaign.get_send_trigger("Received_Campaign_Drugs", old=True)
    campaign.get_send_trigger("Received_RCD_Drugs", old=True)
    campaign.get_send_trigger("Bednet_Got_New_One", old=True)
    campaign.get_send_trigger("Bednet_Using", old=True)
    campaign.get_send_trigger("Bednet_Discarded", old=True)
    campaign.get_send_trigger("InfectionDropped", old=True)

def build_full_magude_campaign(population_size):
    import emod_api.campaign as campaign
    campaign.set_schema(manifest.schema_file)

    sim_start_date = f"{2019 - 60}-01-01"  # sim ends at beginning of 2019. Assume 60-year burnin

    add_itn(campaign, sim_start_date=sim_start_date)
    add_hs(campaign, sim_start_date=sim_start_date)
    add_irs(campaign, sim_start_date=sim_start_date)
    add_mda(campaign, sim_start_date=sim_start_date)
    add_rcd(campaign, sim_start_date=sim_start_date, population_size=population_size)

    add_custom_events(campaign)

    return campaign