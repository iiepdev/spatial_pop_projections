import pandas as pd
import geopandas as gpd


def normalize_input_strings(
    projection_excel: dict, prefec_gdf: gpd.GeoDataFrame, prefec_name_col: str
):
    for sheet, df in projection_excel.items():
        df.iloc[:, 0] = _normalize_string_col(df.iloc[:, 0])
    prefec_gdf[prefec_name_col] = _normalize_string_col(prefec_gdf[prefec_name_col])


def _normalize_string_col(string_col: pd.Series):
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
