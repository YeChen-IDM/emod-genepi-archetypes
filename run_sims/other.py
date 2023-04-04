from emodpy import emod_task

from run_sims import manifest

import emod_api.demographics.Demographics as Demographics

def build_demographics_from_file():
    return Demographics.from_file(manifest.demographics_file_path)


def include_post_processing(task):
    task = emod_task.add_ep4_from_path(task, manifest.ep4_path)
    return task
