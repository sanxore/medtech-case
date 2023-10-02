import re
from datetime import date

from cleantext import clean
from dateutil.parser import parse


# Removing Unicode Characters
def remove_unicode_chars(text: str) -> str:
    """

    :param text:
    :return:
    """

    return re.sub(
        r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)|^rt|http.+?", "", text
    )


def clean_text(text: str) -> str:
    """

    :param text:
    :return:
    """

    return clean(text, no_punct=True, no_line_breaks=True, lang="en")


def standardize_date(str_date: str) -> date:
    """

    :param str_date:
    :return:
    """

    return parse(str_date).date()


def atc_code_valid(atc_code: str) -> bool:
    """

    :param atc_code:
    :return:
    """

    p = re.compile("^[ABCDGHJLMNPRSV]([0-9][0-9]([A-Z]([A-Z]([0-9][0-9])?)?)?)?$")

    return bool(p.match(str(atc_code)))
