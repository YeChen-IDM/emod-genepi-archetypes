import json
import os

import numpy as np


def application(output_folder="output"):
    print("starting dtk post process!")

    # Summarize endpoint
    event_recorder_filepath = os.path.join(output_folder, "InsetChart.json")
    with open(event_recorder_filepath, 'r') as f:
        d = json.load(f)

    endpoint_data = {
        "rdt_prev": np.mean(np.array(d["Channels"]["PfHRP2 Prevalence"]["Data"])[-365:]),
        "true_prev": np.mean(np.array(d["Channels"]["True Prevalence"]["Data"])[-365:])
        # "average_biting"
    }

    json.dump(endpoint_data, open(os.path.join(output_folder, "endpoint.json"), 'w'))

if __name__ == "__main__":
    # Placeholder for now
    application(output_folder="output")
    # application(output_folder='.') #for testing