# emod-genepi-archetypes

### Purpose
EMOD archetypes to be run as input for end-to-end workflow with Gen-Epi.

Right now, only runs sims with 10k individuals, no seasonality, no interventions, no biting heterogeneity.  Eventually this will probably expand to include a seasonal sim as well as the Maka sims.

### Installation
Run the following command: ( it will install this project in editable/'develop' mode):
```bash
pip install --upgrade pip
pip install setuptools (only if you don't have it)
pip install -e . -r requirements.txt
```

### Steps to run
1. Run run_sims/get_latest_binary.py to pull latest EMOD binary and schema
2. Set desired run parameters in the argparse section if you don't want to use the default values. Or you can overrride
them at run time for run_sims/run_from_command_line.py
```python
  --exp_id_filepath EXP_ID_FILEPATH, -i EXP_ID_FILEPATH
                        emod experiment id file (default to manifest.exp_id_file)
  --archetypes ARCHETYPES [ARCHETYPES ...], -a ARCHETYPES [ARCHETYPES ...]
                        list of values for Archetypes: test, flat, maka_like, magude_like, maka_historical, magude_historical (default to ["test"]).
  --pop_sizes_in_thousands POP_SIZES_IN_THOUSANDS [POP_SIZES_IN_THOUSANDS ...], -p POP_SIZES_IN_THOUSANDS [POP_SIZES_IN_THOUSANDS ...]
                        list of values for population size in thousands (possible values are 1k,10k,20k,50k,100k, default to [1, 10])
  --importations_per_year_per_1000 IMPORTATIONS_PER_YEAR_PER_1000 [IMPORTATIONS_PER_YEAR_PER_1000 ...], -r IMPORTATIONS_PER_YEAR_PER_1000 [IMPORTATIONS_PER_YEAR_PER_1000 ...]
                        list of values for importation rate per 1000 people in population (default to [50])
  --target_prevalences TARGET_PREVALENCES [TARGET_PREVALENCES ...], -t TARGET_PREVALENCES [TARGET_PREVALENCES ...]
                        list of values for target (RDT) prevalence for test/flat/maka_like/magude_like scenarios (possible values are 5%, 10%, 20%, 30%, 40%, default to [0.05])
  --max_individual_infections MAX_INDIVIDUAL_INFECTIONS [MAX_INDIVIDUAL_INFECTIONS ...], -m MAX_INDIVIDUAL_INFECTIONS [MAX_INDIVIDUAL_INFECTIONS ...]
                        list of values for maximum number of concurrent infections to sweep (default to [3])
  --seeds SEEDS, -s SEEDS
                        number of simulation replicates (default to 3)
  --exp_name EXP_NAME, -e EXP_NAME
                        emod experiment name in Comps (default to emod_genepi_archetypes)
```
Please see Readme in the run_sims folder for details of these parameters.

3(Optional) Run workflow/post_simulation_steps.py. It will run the following steps automatically: 
   
    3.1. download_output_pycomps.py: This script will download multiple Emod report files('ReportInfectionStatsMalaria.csv', 'ReportSimpleMalariaTransmission.csv', 'InsetChart.json' and some image files if there are any.) from each simulation to your local machine. It returns the experiment ids with the filepaths of the downloaded files. 

    3.2. write_mapping_file.py: This script will generate mapping files for each simulation results and save it in the same folder with the report files. It returns a list of filepaths for mapping files.

Jenkins pipeline to test this workflow: https://jenkins.apps.portal.idmod.org/job/emod-genepi-archetypes_pipeline/