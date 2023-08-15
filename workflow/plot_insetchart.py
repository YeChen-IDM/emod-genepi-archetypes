from emod_api.legacy import plotAllCharts
import os
import argparse
from typing import Union, Set, List
import shutil
import json


def plot_all_insetchart(insetchart_files: Union[Set[str], List[str]], all_in_one: bool = False) -> None:
    """
    Plot Channels from a list of InsetChart.json files
    Args:
        insetchart_files: List of filepath for the InsetChart.json files.
        all_in_one:       Set to True if you want to plot all InsetChart.json in one plot for comparison.
                          Set to False if you want to save one plot per simulation and save the images in each simulation folder.
    Returns:
    """
    insetchart_files = list(insetchart_files)
    if all_in_one:
        all_data = list()
        for insetchart_file in insetchart_files:
            with open(insetchart_file) as sim_data:
                data = json.loads(sim_data.read())
            all_data.append(data)
        plotAllCharts.plotBunch(all_data, plot_name="InsetChart_all_in_one")
    else:
        for i in range(len(insetchart_files)):
            insetchart_file = insetchart_files[i]
            # # If all_at_one, do not close the figure until the last file.
            # # If not all_at_one, close the figure everytime.
            # closefig = (not all_in_one) if i != len(insetchart_files) - 1 else True
            plot_one_insetchart(insetchart_file, all_in_one, closefig=True)


def plot_one_insetchart(insetchart_file: str, all_in_one: bool = False, closefig: bool = True) -> None:
    reference = comparison = insetchart_file
    folder = os.path.dirname(insetchart_file)
    plotAllCharts.plotCompareFromDisk(reference, comparison, savefig=True, closefig=closefig)
    if not all_in_one:
        shutil.move("InsetChart.png", os.path.join(folder, "InsetChart.png"))


# def plotter_example(exp_id="96d5418a-7efa-ed11-aa06-b88303911bc1"):
#     import emod_api.channelreports.plot_icj_means as plotter
#     from emodpy.emod_task import EMODTask
#     EMODTask.cache_experiment_metadata_in_sql(exp_id)
#     data = plotter.collect(exp_id, tag="iv_cost=SWEEP")
#     plotter.display(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emod output filepaths')
    parser.add_argument('--insetchart_files', '-i', nargs='+', help='a list of filepaths for InsetChart.json',
                        default=[
                            'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9ed5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9ad5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_98d5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9bd5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_99d5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9cd5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_a0d5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9fd5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json', 'emod_output/exp_96d5418a-7efa-ed11-aa06-b88303911bc1/sim_9dd5418a-7efa-ed11-aa06-b88303911bc1/InsetChart.json']
                        )
    parser.add_argument('--all_in_one', '-a', help='call to plot all insetchart into one plot',
                        action='store_true')
    args = parser.parse_args()
    plot_all_insetchart(insetchart_files=args.insetchart_files, all_in_one=args.all_in_one)
