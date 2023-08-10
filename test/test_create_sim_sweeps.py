import shutil
import unittest
import os

from run_sims import manifest
from run_sims.create_sim_sweeps import create_and_run_sim_sweep
from idmtools.entities.experiment import Experiment

run_exp = False


class TestCreateAndRunSimSweep(unittest.TestCase):
    def test_default_values(self):
        exp = create_and_run_sim_sweep(run_exp=False)
        self.assertIsInstance(exp, Experiment)

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
            run_exp=run_exp
        )
        shutil.move(manifest.exp_id_file, os.path.join(manifest.output, 'toy_emod_exp.id'))

        if run_exp:
            self.assertTrue(exp.succeeded)
        self.assertTrue(exp.simulation_count, 4)
        archetypes = [x if x != 'test' else 'flat' for x in archetypes]
        actual_archetypes = list()
        for sim in exp.simulations:
            actual_archetypes.append(sim.tags['archetype'])

        self.assertListEqual(archetypes, actual_archetypes)

    def test_historical_archetype(self):
        archetypes = ["maka_historical", "magude_historical"]
        pop_sizes = [1]
        importations = [40]
        max_infections = [3]
        number_of_seeds = 1

        exp = create_and_run_sim_sweep(
            archetypes=archetypes,
            pop_sizes_in_thousands=pop_sizes,
            importations_per_year_per_1000=importations,
            target_prevalences=None,
            max_num_infections=max_infections,
            number_of_seeds=number_of_seeds,
            run_exp=run_exp
        )
        shutil.move(manifest.exp_id_file, os.path.join(manifest.output, 'historical_emod_exp.id'))

        if run_exp:
            self.assertTrue(exp.succeeded)
        self.assertTrue(exp.simulation_count, 2)
        actual_archetypes = list()
        for sim in exp.simulations:
            actual_archetypes.append(sim.tags['archetype'])

        self.assertListEqual(archetypes, actual_archetypes)

    def test_pop_size_sweep(self):
        archetypes = ["test"]
        pop_sizes = [1, 10, 20, 50, 100]
        importations = [50]
        max_infections = [3]
        number_of_seeds = 5

        exp = create_and_run_sim_sweep(
            archetypes=archetypes,
            pop_sizes_in_thousands=pop_sizes,
            importations_per_year_per_1000=importations,
            max_num_infections=max_infections,
            number_of_seeds=number_of_seeds,
            run_exp=False
        )
        self.assertTrue(exp.simulation_count, len(pop_sizes) * number_of_seeds)
        actual_pop_sizes = set()
        for sim in exp.simulations:
            actual_pop_sizes.add(sim.tags['population_size_in_thousands'])

        self.assertSetEqual(set(pop_sizes), actual_pop_sizes)

    def test_importation_sweep(self):
        archetypes = ["test"]
        pop_sizes = [20]
        importations = [10, 50, 100]
        max_infections = [3]
        number_of_seeds = 5

        exp = create_and_run_sim_sweep(
            archetypes=archetypes,
            pop_sizes_in_thousands=pop_sizes,
            importations_per_year_per_1000=importations,
            max_num_infections=max_infections,
            number_of_seeds=number_of_seeds,
            run_exp=False
        )
        self.assertTrue(exp.simulation_count, len(importations) * number_of_seeds)
        actual_importations = set()
        for sim in exp.simulations:
            actual_importations.add(sim.tags['target_num_importations_per_year_per_thousand'])

        self.assertSetEqual(set(importations), actual_importations)

    def test_max_infections_sweep(self):
        archetypes = ["test"]
        pop_sizes = [50]
        importations = [100]
        max_infections = [3, 6, 9]
        number_of_seeds = 5

        exp = create_and_run_sim_sweep(
            archetypes=archetypes,
            pop_sizes_in_thousands=pop_sizes,
            importations_per_year_per_1000=importations,
            max_num_infections=max_infections,
            number_of_seeds=number_of_seeds,
            run_exp=False
        )
        self.assertTrue(exp.simulation_count, len(max_infections) * number_of_seeds)
        actual_max_infections = set()
        for sim in exp.simulations:
            actual_max_infections.add(sim.tags['max_individual_infections'])

        self.assertSetEqual(set(max_infections), actual_max_infections)


if __name__ == '__main__':
    unittest.main()
