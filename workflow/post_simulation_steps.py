from run_sims import manifest
from workflow.download_output_pycomps import download_output
from workflow.write_mapping_file import write_mapping_file
from workflow.plot_insetchart import plot_all_insetchart

import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post simulation steps')
    parser.add_argument('--exp_id_filepath', '-i', type=str,
                        help='emod experiment id file (default to manifest.exp_id_file)',
                        default=manifest.exp_id_file)
    parser.add_argument('--output', '-o', type=str,
                        help='output file name (default to manifest.output)',
                        default=manifest.output)
    args = parser.parse_args()

    output_filepath = download_output(args.exp_id_filepath, False, args.output)
    print(f"Here are the downloaded files: {output_filepath}.")
    mapping_files = write_mapping_file(output_filepath)
    print(f"Here are the mapping file/files: {mapping_files}.")

    print(f"Plotting InsetChart Channels...")
    insetchart_files = set()
    for output_file in output_filepath:
        emod_folder = os.path.dirname(output_file)
        insetchart_file = os.path.join(emod_folder, 'InsetChart.json')
        insetchart_files.add(insetchart_file)
    print(insetchart_files)
    plot_all_insetchart(insetchart_files, all_in_one=False)
    plot_all_insetchart(insetchart_files, all_in_one=True)
