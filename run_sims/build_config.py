from emod_api.config import default_from_schema_no_validation
from emodpy_malaria.malaria_config import add_species, get_species_params, set_species_param, set_team_defaults

from run_sims import manifest


def set_full_config(config, test_run=False):
    set_core_config_params(config)
    set_project_config_params(config)

    if test_run:
        config.parameters.Simulation_Duration = 2 * 365#5 * 365
    else:
        config.parameters.Simulation_Duration = 40 * 365

    config.parameters.Memory_Usage_Halting_Threshold_Working_Set_MB = 16000
    config.parameters.Memory_Usage_Warning_Threshold_Working_Set_MB = 15000

    return config


def set_core_config_params(config):
    set_team_defaults(config, manifest)

    config.parameters.Simulation_Type = "MALARIA_SIM"
    config.parameters.Malaria_Model = "MALARIA_MECHANISTIC_MODEL_WITH_CO_TRANSMISSION"
    config.parameters.Vector_Sampling_Type = "TRACK_ALL_VECTORS"


def set_project_config_params(config):
    config.parameters.Enable_Initial_Prevalence = 1
    config.parameters.Age_Initialization_Distribution_Type = "DISTRIBUTION_SIMPLE"

    config.parameters.Enable_Vital_Dynamics = 1
    config.parameters.Enable_Natural_Mortality = 1
    config.parameters.Enable_Demographics_Birth = 1

    config.parameters.Enable_Disease_Mortality = 0

    config.parameters.Climate_Model = "CLIMATE_CONSTANT"
    config.parameters.Base_Air_Temperature = 27
    config.parameters.Base_Land_Temperature = 27

    # Set dummy ento because Report Vector Stats complains otherwise
    add_species(config, manifest, "gambiae")
    set_ento(config=config,
             habitat_scale=1,
             life_expectancy=20,
             anthropophily=1,
             acquire_modifier=1,
             transmission_rate=1
             )


def set_ento(config, habitat_scale, life_expectancy=20, anthropophily=1.0, acquire_modifier=0.8, transmission_rate=0.9):
    species = "gambiae"

    # add_species(config, manifest, species)
    set_species_param(config, species, "Adult_Life_Expectancy", life_expectancy)
    set_species_param(config, species, "Anthropophily", anthropophily)
    set_species_param(config, species, "Acquire_Modifier", acquire_modifier)
    set_species_param(config, species, "Transmission_Rate", transmission_rate)
    # nuisance params
    set_species_param(config, species, "Vector_Sugar_Feeding_Frequency", "VECTOR_SUGAR_FEEDING_NONE")
    set_species_param(config, species, "Indoor_Feeding_Fraction", 1.0)
    # Remove any habitats that are set by default
    set_species_param(config, species, "Habitats", [], overwrite=True)

    # Flat seasonality
    set_linear_spline_habitat(config, species, habitat_scale, [1.0]*12)


def set_linear_spline_habitat(config, species, log10_max_larval_capacity, capacity_distribution_over_time):
    lhm = default_from_schema_no_validation.schema_to_config_subnode(manifest.schema_file,
                                                                     ["idmTypes", "idmType:VectorHabitat"])
    lhm.parameters.Habitat_Type = "LINEAR_SPLINE"
    lhm.parameters.Max_Larval_Capacity = 10 ** log10_max_larval_capacity
    lhm.parameters.Capacity_Distribution_Number_Of_Years = 1
    lhm.parameters.Capacity_Distribution_Over_Time.Times = [0.0, 30.4, 60.8, 91.3, 121.7, 152.1,
                                                            182.5, 212.9, 243.3, 273.8, 304.2, 334.6]
    lhm.parameters.Capacity_Distribution_Over_Time.Values = capacity_distribution_over_time

    get_species_params(config, species).Habitats.append(lhm.parameters)