import argparse
import os
import shutil
import time
import threading
import math

from run_sims import manifest

from COMPS import Client
from COMPS.Data import Experiment


class MyThread(threading.Thread):
    def __init__(self, paths, optional_paths, output_path, sims_):
        self.sims = sims_
        self.paths = paths
        self.optional_paths = optional_paths
        self.output_path = output_path
        threading.Thread.__init__(self)

    def run(self):
        for sim in self.sims:
            start = time.time()

            asset_byte_arrays = sim.retrieve_output_files(paths=self.paths)
            optional_asset_byte_arrays = []
            found_optional_paths = []

            for path in self.optional_paths:
                try:
                    optional_asset_byte_arrays.append(sim.retrieve_output_files(paths=[path])[0])
                    found_optional_paths.append(path)
                except RuntimeError as e:
                    print(e)

            p = os.path.join(self.output_path, 'exp_' + str(sim.experiment_id), 'sim_' + str(sim.id))
            if not os.path.exists(p):
                os.makedirs(p)
            for i in range(len(self.paths)):
                with open(os.path.join(p, os.path.basename(self.paths[i])), 'wb') as outfile:
                    outfile.write(asset_byte_arrays[i])

            for i in range(len(optional_asset_byte_arrays)):
                with open(os.path.join(p, os.path.basename(found_optional_paths[i])), 'wb') as outfile:
                    outfile.write(optional_asset_byte_arrays[i])

            print('| -> downloading/saving %d asset(s) took %.2f sec' % (len(self.paths), time.time() - start))


def download_output(exp_id_filepath: str, first_only: bool = False, output_path: str = manifest.output) -> list:
    """
    Download Emod simulation output csv files to output folder from Comps.
    Args:
        exp_id_filepath ():          experiment id filepath
        first_only ():               download the first simulation outputs only
        output_path ():              output file path

    Returns: list of results file paths

    """
    with open(exp_id_filepath, 'r') as id_file:
        exp_id = id_file.readline().rstrip()

    exp_ids = [
        exp_id
    ]

    paths = [os.path.join("output", manifest.infection_report),
             os.path.join("output", manifest.transmission_report),
             os.path.join("output", manifest.insetchart)]
    optional_paths = ['magude_inc.png', 'magude_prev.png', 'sac_prev.png', 'u5_prev.png']

    Client.login(manifest.compshost)

    all_sims = []

    for exp_id in exp_ids:
        all_sims.extend(Experiment.get(exp_id).get_simulations())

        # clear the output dir for that experiment if it already exists
        outputpath = os.path.join(output_path, 'exp_' + exp_id)
        if os.path.exists(outputpath):
            shutil.rmtree(outputpath, True)

    # collect result filepaths
    result_files = []
    for sim in all_sims:
        p = os.path.join(output_path, 'exp_' + str(sim.experiment_id), 'sim_' + str(sim.id))
        for i in range(len(paths)):
            result_files.append(os.path.join(p, os.path.basename(paths[i])))
        # if 'archetype' in sim.tags:
        #     if 'magude_historical' == sim.tags['archetype']:
        #         optional_paths.append('magude_inc.png')
        #         optional_paths.append('magude_prev.png')
        #     elif 'maka_historical' == sim.tags['archetype']:
        #         optional_paths.append('sac_prev.png')
        if first_only:
            break
    if first_only:
        all_sims = [all_sims[0]]
    print(result_files)

    sims_per_thread = math.ceil(len(all_sims) / manifest.download_num_threads)

    overall_start = time.time()
    threads = []

    for i in range(manifest.download_num_threads):
        t = MyThread(paths, optional_paths, output_path, all_sims[:sims_per_thread])
        all_sims = all_sims[sims_per_thread:]
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('total download time = %.2f sec' % (time.time() - overall_start))

    return result_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emod experiment id file')
    parser.add_argument('--exp_id_filepath', '-i', type=str, help='Emod experiment id file',
                        default=manifest.exp_id_file)
    parser.add_argument('--first_only', '-f', help='download the first sim only',
                        action='store_true')
    parser.add_argument('--output_path', '-o', type=str, help='output file path',
                        default=manifest.output)
    args = parser.parse_args()
    download_output(args.exp_id_filepath, args.first_only, args.output_path)
