import pytest
import numpy as np

from scripts.data_analysis.reshape import shape_image_array_to_time_series


TEST_ARR = np.array([
    [[1, 2],
    [1, 2]],

    [[2, 3],
    [2, 3]],

    [[3, 4],
    [3, 4]],
])


def test_reshape_shape():
    reshaped = shape_image_array_to_time_series(TEST_ARR, n_observations=3)
    assert reshaped.shape == (4, 3)
    

def test_reshape_content():
    reshaped = shape_image_array_to_time_series(TEST_ARR, n_observations=3)
    assert np.array_equal(reshaped, np.array([
        [1, 2, 3],
        [2, 3, 4],
        [1, 2, 3],
        [2, 3, 4],
    ]))     
