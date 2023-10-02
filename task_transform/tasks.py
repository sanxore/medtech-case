import json

import pandas as pd

from task_transform.utils import process_edges, process_nodes


def transform(paths, **kwargs):
    """

    :param csv_path: csv file path to clean
    :param config: cleansing config
    :param kwargs:
    :return:
    """

    # get data
    drugs = pd.read_csv(
        filepath_or_buffer=paths["drugs_data_path"],
    )
    pubmed = pd.read_csv(
        filepath_or_buffer=paths["pubmed_data_path"],
    )
    clinical_trials = pd.read_csv(
        filepath_or_buffer=paths["clinical_trials_data_path"],
    )

    nodes = process_nodes(drugs, pubmed, clinical_trials)
    edges = process_edges(drugs, pubmed, clinical_trials)

    # build graph
    graph = {"nodes": nodes, "edges": edges}

    # Serializing graph json
    with open(paths["output_path"], "w") as f:
        json.dump(graph, f)
