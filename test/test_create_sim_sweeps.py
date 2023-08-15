import shutil
import unittest
import pytest

from run_sims.create_sim_sweeps import create_and_run_sim_sweep
from idmtools.entities.experiment import Experiment

run_exp = True


class TestCreateAndRunSimSweep(unittest.TestCase):
    @pytest.mark.order(2)
    def test_default_values(self):
        exp = create_and_run_sim_sweep(run_exp=False)
        self.assertIsInstance(exp, Experiment)

    @pytest.mark.order(2)
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

    @pytest.mark.order(2)
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

    @pytest.mark.order(2)
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
