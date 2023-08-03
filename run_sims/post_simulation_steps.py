import os
from run_sims import manifest
from run_sims.download_output_pycomps import download_output
from run_sims.write_mapping_file import write_mapping_file
from run_sims.plot_insetchart import plot_all_insetchart


if __name__ == '__main__':
    output_filepath = download_output(manifest.exp_id_file, False, manifest.output)
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
    pass
