import argparse
from run_sims import manifest

from idmtools.core.platform_factory import Platform
from idmtools_platform_comps.utils.download.download import DownloadWorkItem

"""
There is performance issue with Download Work Item. Please use download_output_pycomps.py instead.
"""


def download_output(filename: str, platform: Platform = None) -> bool:
    """
    Download Emod simulation output csv files to output folder from Comps.
    Args:
        filename ():
        platform ():

    Returns: status of download work item

    """
    if not platform:
        platform = Platform(manifest.platform_name)
    with open(filename, 'r') as id_file:
        exp_id = id_file.readline().rstrip()

    dl_wi = DownloadWorkItem(name="Download Malaria reports",
                             related_experiments=[exp_id],
                             file_patterns=["output/ReportInfectionStatsMalaria.csv",
                                            "output/ReportSimpleMalariaTransmission.csv"],
                             delete_after_download=False,
                             verbose=True,
                             output_path=manifest.simulation_output_filepath
                             )
    dl_wi.run(wait_on_done=True, platform=platform)

    if not dl_wi.succeeded:
        print(f"Download work item {dl_wi.uid} failed.\n")
    else:
        print(f"Download work item {dl_wi.uid} succeeded.")
        download_id_file = manifest.download_wi_id_file
        with open(download_id_file, 'w') as id_file:
            id_file.write(dl_wi.uid.hex)

    return dl_wi.succeeded


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emod experiment id file')
    parser.add_argument('--filename', '-f', type=str, help='Emod experiment id file',
                        default=manifest.exp_id_file)
    args = parser.parse_args()
    download_output(args.filename)