from emod_api.config import default_from_schema_no_validation
from emodpy_malaria.malaria_config import add_species, get_species_params, set_species_param, set_team_defaults

from run_sims import manifest


def set_full_config(config
                    ):
    set_core_config_params(config)
    set_project_config_params(config)


    config.parameters["logLevel_default"] = "WARNING"
    config.parameters["logLevel_JsonConfigurable"] = "WARNING" # Note: this makes it hard to debug
    config.parameters["Enable_Log_Throttling"] = 1

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

    config.parameters.Enable_Demographics_Risk = 1

    config.parameters.Climate_Model = "CLIMATE_CONSTANT"
    config.parameters.Base_Air_Temperature = 27
    config.parameters.Base_Land_Temperature = 27

def set_non_ento_archetype_config_params(config, archetype):
    if archetype == "test":
        config.parameters.Simulation_Duration = 3 * 365
    if archetype in ["flat", "maka_like", "magude_like"]:
        config.parameters.Simulation_Duration = 40 * 365
    elif archetype == "maka_historical":
        config.parameters.Simulation_Duration = 60 * 365
    elif archetype == "magude_historical":
        raise NotImplementedError
        # config.parameters.Simulation_Duration = 40 * 365
    else:
        return NotImplementedError("Archetype {} not implemented".format(archetype))


def set_ento(config, archetype="flat", habitat_scale=-1):
    if habitat_scale == -1:
        print("No habitat scale provided!")

    if archetype == "flat":
        if habitat_scale == -1:
            print("Using default habitat_scale (7)")
            habitat_scale = 7
        add_species(config, manifest, "gambiae")
        set_ento_params(config, anthropophily=0.65, indoor_feeding_fraction=1.0)
        set_ento_habitat(config, archetype=archetype, habitat_scale=habitat_scale)

    elif archetype == "maka_historical" or archetype == "maka_like":
        if habitat_scale == -1:
            print("Using default maka habitat_scale (~8.75)")
            habitat_scale = 8.75
        add_species(config, manifest, "gambiae")
        set_ento_params(config, anthropophily=0.5, indoor_feeding_fraction=0.5)
        set_ento_habitat(config, archetype=archetype, habitat_scale=habitat_scale)

    elif archetype == "magude_historical" or archetype == "magude_like":
        if habitat_scale == -1:
            print("Using default magude habitat_scales (~7.93 for both species)")
            habitat_scale = 7.93

        add_species(config, manifest, ["arabiensis", "funestus"])

        set_ento_params(config, species="arabiensis", anthropophily=0.65, indoor_feeding_fraction=0.95)
        set_ento_habitat(config, archetype=archetype, species="arabiensis", habitat_scale=habitat_scale)

        set_ento_params(config, species="funestus", anthropophily=0.65, indoor_feeding_fraction=0.6)
        set_ento_habitat(config, archetype=archetype, species="funestus", habitat_scale=habitat_scale)


def set_ento_params(config, anthropophily, indoor_feeding_fraction, species="gambiae"):
    set_species_param(config, species, "Adult_Life_Expectancy", 20)
    set_species_param(config, species, "Acquire_Modifier", 0.8)
    set_species_param(config, species, "Transmission_Rate", 0.9)
    set_species_param(config, species, "Anthropophily", anthropophily)
    set_species_param(config, species, "Vector_Sugar_Feeding_Frequency", "VECTOR_SUGAR_FEEDING_NONE")
    set_species_param(config, species, "Indoor_Feeding_Fraction", indoor_feeding_fraction)

def set_ento_habitat(config, archetype, habitat_scale, species="gambiae"):
    # Remove any habitats that are set by default
    set_species_param(config, species, "Habitats", [], overwrite=True)

    lhm = default_from_schema_no_validation.schema_to_config_subnode(manifest.schema_file, ["idmTypes", "idmType:VectorHabitat"])
    lhm.parameters.Habitat_Type = "LINEAR_SPLINE"
    lhm.parameters.Max_Larval_Capacity = 10 ** habitat_scale

    month_start_times = [0.0, 30.4, 60.8, 91.3, 121.7, 152.1, 182.5, 212.9, 243.3, 273.8, 304.2, 334.6]

    if archetype == "flat":
        # Flat seasonality
        lhm.parameters.Capacity_Distribution_Number_Of_Years = 1
        lhm.parameters.Capacity_Distribution_Over_Time.Times = month_start_times
        lhm.parameters.Capacity_Distribution_Over_Time.Values = [1.0] * 12
        get_species_params(config, species).Habitats.append(lhm.parameters)

    elif archetype == "maka_like" or archetype == "maka_historical":
        # Makacoulibantang seasonality
        lhm.parameters.Capacity_Distribution_Number_Of_Years = 1
        lhm.parameters.Capacity_Distribution_Over_Time.Times = month_start_times
        lhm.parameters.Capacity_Distribution_Over_Time.Values = [0.02, 0.01, 0.01, 0.01, 0.1, 0.2, 0.3, 0.45, 1, 0.25,
                                                                 0.133, 0.05]
        get_species_params(config, species).Habitats.append(lhm.parameters)

    elif archetype == "magude_like" or archetype == "magude_historical":
        # Magude-Sede seasonality
        lhm.parameters.Capacity_Distribution_Number_Of_Years = 5
        lhm.parameters.Capacity_Distribution_Over_Time.Times = [month_start_time + year_offset * 365 for year_offset in range(5) for month_start_time in month_start_times]
        if species == "arabiensis":
            spline_values = [
                3.13403706, 6.477181329, 4.646525543, 1.266288643, 1.805642935, 0.012810537,
                0.012810537, 0.921133806, 0.839535134, 0.096459878, 2.672613579, 0.13416778,
                3.13403706, 0.504076546, 7.200840631, 0.012810537, 0.25493831, 0.015894707,
                0.012810537, 0.28338864, 0.663339004, 0.029708279, 0.796607506, 0.248538589,
                0.012810537, 0.504076546, 7.200840631, 0.012810537, 0.704230108, 2.796920281,
                0.339927348, 0.01953714, 0.824856237, 4.309893117, 4.357161007, 0.076344378,
                3.13403706, 6.477181329, 4.646525543, 1.266288643, 1.805642935, 0.012810537,
                0.012810537, 0.921133806, 0.839535134, 0.096459878, 2.672613579, 0.13416778,
                0.069094447, 5.245201305, 3.041716874, 0.63954959, 0.921603784, 0.941875175,
                0.121849474, 0.408019862, 0.775910125, 1.478687091, 2.608794031, 0.153016915
            ]

        elif species == "funestus":
            spline_values = [
                0.550532405, 0.277873921, 0.598301883, 1.104333627, 0.423640247, 0.050567909,
                0.277962223, 0.1349002, 8.668074306, 1.609996538, 0.430187668, 0.050820004,
                0.550532405, 0.145055419, 0.013468929, 0.359361544, 3.995523387, 1.652689007,
                2.152176582, 1.179803015, 0.610473624, 0.827921375, 0.059934404, 0.244205788,
                0.073614774, 0.145055419, 0.013468929, 0.359361544, 0.277893432, 0.247039019,
                0.186844672, 0.013468929, 0.117102225, 0.278687927, 0.078546842, 0.053226178,
                0.550532405, 0.277873921, 0.598301883, 1.104333627, 0.423640247, 0.050567909,
                0.277962223, 0.1349002, 8.668074306, 1.609996538, 0.430187668, 0.050820004,
                0.511385711, 0.804934271, 0.281763759, 0.731847586, 1.565685689, 0.650098645,
                0.872327826, 0.442724048, 3.131883385, 0.90553528, 0.189556305, 0.11608399
            ]
        else:
            raise NotImplementedError("Species {} not implemented for archetype {}".format(species, archetype))
        lhm.parameters.Capacity_Distribution_Over_Time.Values = spline_values
        get_species_params(config, species).Habitats.append(lhm.parameters)

