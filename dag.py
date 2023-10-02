import json
import os

from task_clean.tasks import cleansing
from task_transform.tasks import transform


def get_dict_from_json(path):

    with open(path, "r") as f:
        result = json.loads(f.read())

    return result


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    root_path = os.path.dirname(os.path.abspath(__file__))
    configs_path = os.path.join(root_path, "configs")

    # get cleaning configs
    drugs_clean_config = get_dict_from_json(
        os.path.join(configs_path, "clean_drugs.json")
    )
    pubmed_clean_config = get_dict_from_json(
        os.path.join(configs_path, "clean_pubmed.json")
    )
    clinical_trials_clean_config = get_dict_from_json(
        os.path.join(configs_path, "clean_clinical_trials.json")
    )

    # run cleaning it can be run in parallel
    cleansing(drugs_clean_config)
    cleansing(pubmed_clean_config)
    cleansing(clinical_trials_clean_config)

    # get transform config
    transform_config = get_dict_from_json(os.path.join(configs_path, "transform.json"))

    # run transform
    transform(transform_config)
