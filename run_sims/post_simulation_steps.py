from run_sims import manifest
from run_sims.download_output_pycomps import download_output
from run_sims.write_mapping_file import write_mapping_file


if __name__ == '__main__':
    output_filepath = download_output(manifest.exp_id_file, False, manifest.output)
    print(f"Here are the downloaded files: {output_filepath}.")
    mapping_files = write_mapping_file(output_filepath)
    print(f"Here are the mapping file/files: {mapping_files}.")
    pass
