import pandas as pd

from task_clean.utils import clean_text, standardize_date


def cleansing(config, **kwargs):
    """

    :param csv_path: csv file path to clean
    :param config: cleansing config
    :param kwargs:
    :return:
    """
    data = pd.read_csv(
        filepath_or_buffer=config["path"],
        header=0 if config.get("header", "auto") == "auto" else "infer",
        names=None if config.get("header", "auto") == "auto" else config.get("header"),
    )

    # text cleaning
    if config.get("text_cleaning"):
        for col in config.get("text_cleaning"):
            data[col] = data[col].apply(clean_text)

    # date cleaning
    if config.get("date_cleaning"):
        for col in config.get("date_cleaning"):
            data[col] = data[col].apply(standardize_date)

    # # atc_code_cleaning cleaning
    # if config.get("atc_code_cleaning"):
    #     # data = data[data[config.get("atc_code_cleaning")].apply(func=atc_code_valid)]

    data.drop_duplicates().to_csv(
        path_or_buf=config["output_path"],
        index=False,
    )
