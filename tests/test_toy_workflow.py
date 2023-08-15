import unittest
import os
import pytest
import json
import shutil

from run_sims import manifest
from run_sims.create_sim_sweeps import create_and_run_sim_sweep
from workflow.download_output_pycomps import download_output
from workflow.write_mapping_file import write_mapping_file

from helper import build_folder_structure

run_exp = True


class TestToyWorkflow(unittest.TestCase):
    @pytest.mark.order(2)
    def test_toy_archetype(self):
        archetypes = ["test", "flat", "maka_like", "magude_like"]
        pop_sizes = [1]
        importations = [40]
        target_prevalences = [0.05]
        max_infections = [3]
        number_of_seeds = 1

        exp = create_and_run_sim_sweep(
            archetypes=archetypes,
            pop_sizes_in_thousands=pop_sizes,
            importations_per_year_per_1000=importations,
            target_prevalences=target_prevalences,
            max_num_infections=max_infections,
            number_of_seeds=number_of_seeds,
            run_exp=run_exp,
            exp_id_filepath=os.path.join(manifest.output, 'toy_emod_exp.id')
        )
        # shutil.move(manifest.exp_id_file, os.path.join(manifest.output, 'toy_emod_exp.id'))

        if run_exp:
            self.assertTrue(exp.succeeded)
        self.assertEqual(exp.simulation_count, 4)
        archetypes = [x if x != 'test' else 'flat' for x in archetypes]
        actual_archetypes = list()
        for sim in exp.simulations:
            actual_archetypes.append(sim.tags['archetype'])

        self.assertListEqual(archetypes, actual_archetypes)

    @pytest.mark.order(3)
    def test_download_toy_archetypes(self):
        exp_id_filepath = os.path.join(manifest.output, 'toy_emod_exp.id')
        output_path = os.path.join(manifest.output, 'toy_emod_exp')
        if os.path.exists(output_path):
            try:
                shutil.rmtree(output_path)
                print(f"Path '{output_path}' and its contents have been deleted.")
            except Exception as e:
                print(f"Error deleting path '{output_path}': {e}")
        else:
            print(f"Path '{output_path}' does not exist.")

        toy_emod_exp_output = download_output(exp_id_filepath=exp_id_filepath, first_only=False,
                                              output_path=output_path)
        with open(os.path.join(manifest.output, 'toy_emod_exp.txt'), 'w') as file:
            json.dump(toy_emod_exp_output, file)
        folder_structure = build_folder_structure(output_path)
        self.assertEqual(4, len(folder_structure))
        for folder, files in folder_structure.items():
            self.assertIn(manifest.infection_report, files.keys())
            self.assertIn(manifest.transmission_report, files.keys())
            self.assertIn(manifest.insetchart, files.keys())
            self.assertEqual(len(files.keys()), 3)

    def mapping_file_test(self, output_file, output_folder, mapping_file_count):
        with open(output_file, 'r') as file:
            output_paths = json.load(file)
        mapping_files = write_mapping_file(output_filepath=output_paths)
        self.assertEqual(len(mapping_files), mapping_file_count)
        folder_structure = build_folder_structure(output_folder)
        self.assertEqual(mapping_file_count, len(folder_structure))
        for files in folder_structure.values():
            self.assertIn('mapping_file.csv', files)

    @pytest.mark.order(4)
    def test_write_mapping_file_toy(self):
        output_file = os.path.join(manifest.output, 'toy_emod_exp.txt')
        output_folder = os.path.join(manifest.output, 'toy_emod_exp')
        mapping_file_count = 4
        self.mapping_file_test(output_file, output_folder, mapping_file_count)


if __name__ == '__main__':
    unittest.main()
