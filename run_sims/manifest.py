import os

base_folder = os.path.dirname(os.path.realpath(__file__))

# Ensure the following locations exist
schema_file = os.path.join(base_folder, "download/schema.json")
eradication_path = os.path.join(base_folder, "download/Eradication")
assets_input_dir = os.path.join(base_folder, "Assets")
plugins_folder = os.path.join(base_folder, "download/reporter_plugins")
current_directory = ""
ep4_path = os.path.join(base_folder, "Assets")
burnin_directory = os.path.join(base_folder, "Assets")
sif = os.path.join(base_folder, "Assets/sif.id")
test_demographics_file_path = os.path.join(base_folder, "Assets/demo_for_testing.json")
demographics_file_path = os.path.join(base_folder, "Assets/demo.json")

# CSVs for intervention setup
additional_csv_folder = os.path.join(base_folder, "Assets/")
output = "emod_output"
if not os.path.isdir(output):
    os.mkdir(output)
exp_id_file = os.path.join(output, "emod_exp.id")
download_wi_id_file = os.path.join(output, "download_wi.id")
simulation_output_filepath = "emod_monthly_testing"
infection_report = 'ReportInfectionStatsMalaria.csv'
transmission_report = 'ReportSimpleMalariaTransmission.csv'

# archetypes
maka_archetype_folder = os.path.join(base_folder, "archetypes/maka")
magude_archetype_folder = os.path.join(base_folder, "archetypes/magude")

# Comps
compshost = 'https://comps.idmod.org'
platform_name = "Calculon"
download_num_threads = 8