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
them at run time for run_sims/run_sim.py
```python
  --exp_id_filepath EXP_ID_FILEPATH, -i EXP_ID_FILEPATH
                        emod experiment id file (default to manifest.exp_id_file)
  --test_run, -t        test_run flag (default to True)
  --exp_name EXP_NAME, -e EXP_NAME
                        emod experiment name in Comps (default to emod_genepi_archetypes)
  --max_individual_infections MAX_INDIVIDUAL_INFECTIONS [MAX_INDIVIDUAL_INFECTIONS ...], -m MAX_INDIVIDUAL_INFECTIONS [MAX_INDIVIDUAL_INFECTIONS ...]
                        list of values for maximum number of concurrent infections to sweep (default to [3, 6, 9])
  --larval_habitat_scales LARVAL_HABITAT_SCALES [LARVAL_HABITAT_SCALES ...], -l LARVAL_HABITAT_SCALES [LARVAL_HABITAT_SCALES ...]
                        list of values for the log10 of the maximum larval habitat to sweep (default to [6.5, 7.0, 7.5])
  --seeds SEEDS, -s SEEDS
                        number of simulation replicates (default to 1)
  --reporting_interval REPORTING_INTERVAL, -r REPORTING_INTERVAL
                        reporting interval for ReportInfectionStatsMalaria (default to 30 days)
```
- max_individual_infections: the maximum number of concurrent infections an individual in the simulation can have
- larval_habitat_scale: the log10 of the maximum larval habitat (increasing this increases the transmission intensity)
- number of seeds: number of simulation replicates
- test_run: if set to True, the sims have 1k individuals and are 3-year sims with the reports beginning after 1 years, and sims are submitted to the node_group idm_48cores.  Otherwise, the sims have 10k individuals and are 40 years long, with reports starting after 30 years, and sims are submitted to node_group idm_abcd

3. Run run_sim.py
4. (Optional) Run post_simulation_steps.py. It will run the following steps automatically: 
   
    4.1. download_output_pycomps.py: This script will download 2 Emod report files('ReportInfectionStatsMalaria.csv' and 'ReportSimpleMalariaTransmission.csv') from each simulation to your local machine. It returns the experiment ids with the filepaths of the downloaded files. 

    4.2. write_mapping_file.py: This script will generate mapping files for each simulation results and save it in the same folder with the report files. It returns a list of filepaths for mapping files.

---
### Potential future work/features
- Have dtk_post_process make data-comparison plots for the historical archetypes (need help knowing how to find archetype with dtk_post_process)
- 