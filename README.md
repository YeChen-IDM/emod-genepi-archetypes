# emod-genepi-archetypes

### Purpose
EMOD archetypes to be run as input for end-to-end workflow with Gen-Epi.

Right now, only runs sims with 10k individuals, no seasonality, no interventions, no biting heterogeneity.  Eventually this will probably expand to include a seasonal sim as well as the Maka sims.

### Installation
Run the following command: ( it will install this project in editable/'develop' mode):
```bash
pip install -e . -r requirements.txt
```

### Steps to run
1. Run run_sims/get_latest_binary.py to pull latest EMOD binary and schema
2. Set desired run parameters in the following section of run_sims/run_sim.py
```python
    experiment_name = "test"

    # parameters to sweep over:
    max_individual_infections = [3,6,9]
    larval_habitat_scales = [6.5,7.0,7.5]
    number_of_seeds = 1
    test_run = True
```
- max_individual_infections: the maximum number of concurrent infections an individual in the simulation can have
- larval_habitat_scale: the log10 of the maximum larval habitat (increasing this increases the transmission intensity)
- number of seeds: number of simulation replicates
- test_run: if set to True, the sims are 5-year sims with the reports beginning after 3 years, and sims are submitted to the node_group idm_48cores.  Otherwise, the sims are 40 years long, with reports starting after 30 years, and sims are submitted to node_group idm_abcd

3. Run run_sim.py
4. (Optional) Run post_simulation_steps.py. It will run the following steps automatically: 
   
    4.1. download_output_pycomps.py: This script will download 2 Emod report files('ReportInfectionStatsMalaria.csv' and 'ReportSimpleMalariaTransmission.csv') from each simulation to your local machine. It returns the experiment ids with the filepaths of the downloaded files. 

    4.2. write_mapping_file.py: This script will generate mapping files for each simulation results and save it in the same folder with the report files. It returns a list of filepaths for mapping files.