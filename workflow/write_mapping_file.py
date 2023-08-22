import os
import argparse
import pandas as pd
from operator import itemgetter

from run_sims import manifest


def write_mapping_file(output_filepath: list, first_only: bool = False, mapping_filepath: str = None) -> list:
    """
    Write mapping file for Emod outputs.
    Args:
        output_filepath (): Emod simulation output filepaths
        first_only (): download the first simulation outputs only
        mapping_filepath (): mapping filepath, use with first_only to save the mapping file to a specific path

    Returns: list of mapping filepaths
    """

    sim_map = {}
    for f in output_filepath:
        filename = os.path.basename(f)
        directory = os.path.abspath(os.path.dirname(f))
        sim = directory.split('sim_')[-1]
        if sim not in sim_map:
            mapping_file = os.path.join(directory, "mapping_file.csv")
            sim_map[sim] = [mapping_file, False, False]

        if filename == manifest.transmission_report:
            sim_map[sim][1] = True
        elif filename == manifest.infection_report:
            sim_map[sim][2] = True

        if sim_map[sim][1] is True and sim_map[sim][2] is True:
            mapping_df = pd.DataFrame({"output_name": "emod_file",
                                       # transmission file
                                       "full_path": os.path.join(directory, manifest.transmission_report),
                                       # infection file
                                       "infection_path": os.path.join(directory, manifest.infection_report)},
                                      index=[0])
            mapping_df.to_csv(sim_map[sim][0], index=False)
            if first_only:
                print(f'We only need first simulation, writing to mapping file: {mapping_filepath}.')
                mapping_df.to_csv(mapping_filepath, index=False)
                print("Done writing the mapping file.")
                break

    return list(map(itemgetter(0), list(sim_map.values())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emod output filepaths')
    parser.add_argument('--output_filepath', '-o', nargs='+', help='Emod simulation output filepaths',
                        default=[
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_747a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_747a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_757a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_757a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_767a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_767a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_777a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_777a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_787a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_787a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_797a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_797a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7a7a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7a7a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7b7a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7b7a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7c7a720c-7cd9-ed11-aa05-b88303911bc1/ReportInfectionStatsMalaria.csv',
                            'emod_output/exp_737a720c-7cd9-ed11-aa05-b88303911bc1/sim_7c7a720c-7cd9-ed11-aa05-b88303911bc1/ReportSimpleMalariaTransmission.csv']
                        )
    parser.add_argument('--first_only', '-f', help='download the first sim only',
                        action='store_true')
    parser.add_argument('--mapping_filepath', '-m', type=str, help='mapping filepaths',
                        default=None)
    args = parser.parse_args()
    print('running with:')
    print(args.output_filepath, args.first_only, args.mapping_filepath)
    write_mapping_file(args.output_filepath, args.first_only, args.mapping_filepath)
