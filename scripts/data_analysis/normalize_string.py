import pandas as pd


def normalize_string_col(string_col: pd.Series):
    string_col = string_col.str.lower()
    mapping = {
        "â": "a",
        "á": "a",
        "é": "e",
        "è": "e",
        "ô": "o",
        #        "-": " ",
    }
    for old, new in mapping.items():
        string_col = string_col.str.replace(old, new, regex=False)
    return string_col
