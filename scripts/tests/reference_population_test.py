from pathlib import Path
import pytest
import pandas as pd

from scripts.data_analysis.get_prefec_projection import get_prefec_projection


REFERENCE_PROJECTIONS = pd.read_excel(
    Path("./data/input/population_projections/Project_Prefect_INSEED.xlsx"),
    sheet_name=None,
    skiprows=141,  # We dont want lomé-specific data
    usecols=[0, 1, 2],  # We just need the age, m, f columns
)


def test_correct_value():
    value = get_prefec_projection(REFERENCE_PROJECTIONS, "est-mono", 2024, 20, "f")
    assert int(value) == 8042  # manually checked from input file
