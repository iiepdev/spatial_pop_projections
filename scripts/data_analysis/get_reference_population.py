AGE_GROUPS = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]


def get_reference_population(projections, prefec, year, age_group, sex):
    """A function for extracting prefecture-level population projections

    This is highly specific to the excact excel file used in the togo analysis,
    and will need a redo if another type of projection data is used.
    """
    year_projections = _get_df_by_year(projections, year)
    prefec_idx = _get_starting_idx(year_projections, prefec)
    if prefec_idx.empty:
        new_spelling = _try_different_spelling(prefec)
        prefec_idx = _get_starting_idx(year_projections, new_spelling)
        if prefec_idx.empty:
            return None
    prefec_idx = prefec_idx.item()
    prefec_projections = year_projections.iloc[
        prefec_idx + 1 : prefec_idx + 18  # number of rows to extract
    ]
    prefec_projections = prefec_projections.assign(prefec_age=AGE_GROUPS)
    return prefec_projections[prefec_projections["prefec_age"] == age_group][sex].item()


def _get_df_by_year(projections, year):
    year_projections = projections[f"Projec_{year}"]
    year_projections.columns = ["prefec_age", "m", "f"]
    return year_projections


def _try_different_spelling(prefec):
    names = {
        "tandjouare": "tandjoare",
        "kpendjal-ouest": "kpendjal ouest",
        "oti-sud": "oti sud",
        "mo": " mo",
        "agoe-nyive": "agoe",
    }
    if prefec in names:
        return names[prefec]
    return None


def _get_starting_idx(df, prefec):
    prefec_idx = df.index[df["prefec_age"].str.lower() == prefec]
    return prefec_idx
