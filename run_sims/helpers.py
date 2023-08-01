from datetime import datetime

from emodpy import emod_task

from run_sims import manifest

import emod_api.demographics.Demographics as Demographics

def build_demographics_from_file(test_run=False):
    if test_run:
        return Demographics.from_file(manifest.test_demographics_file_path)
    else:
        return Demographics.from_file(manifest.demographics_file_path)


def include_post_processing(task):
    task = emod_task.add_ep4_from_path(task, manifest.ep4_path)
    return task


def convert_to_day_365(convert_date, ref_date, date_format="%Y-%m-%d"):
    # Converts date to day of simulation starting from reference date
    # Assumes a calendar year has exactly 365 days
    return 365 * (datetime.strptime(convert_date, date_format).year - \
                  datetime.strptime(ref_date, date_format).year) + \
           datetime.strptime(convert_date, date_format).timetuple().tm_yday
