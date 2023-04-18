from run_sims import manifest
from run_sims.download_output_pycomps import download_output
from run_sims.write_mapping_file import write_mapping_file


if __name__ == '__main__':
    output_filepath = download_output(manifest.exp_id_file, False, manifest.output)
    mapping_files = write_mapping_file(output_filepath)
    print(mapping_files)
    pass
