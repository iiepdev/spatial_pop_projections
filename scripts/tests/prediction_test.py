import pytest
import numpy as np

from scripts.data_analysis.predict_population import (
    solve_intercepts_and_slopes,
    _get_predicted_array,
    get_adjusted_prediction,
)
from scripts.data_analysis.reshape import shape_image_array_to_time_series


TEST_ARR = np.array([
    [[1, 2],
    [1, 2]],

    [[2, 3],
    [2, 3]],

    [[3, 4],
    [3, 4]],
])

PERIODS = np.array([1, 2, 3])

TIME_SERIES = shape_image_array_to_time_series(TEST_ARR, len(PERIODS))

INTERCEPTS, SLOPES = solve_intercepts_and_slopes(PERIODS, TIME_SERIES)


def test_intercepts():
    assert INTERCEPTS[0] == pytest.approx(0)


def test_slopes():
    assert SLOPES[0] == pytest.approx(1)


def test_predicted_values():
    predictions = _get_predicted_array(INTERCEPTS, SLOPES, x=4)
    assert predictions[0] == pytest.approx(4)


def test_adjusted_prediction_shape():
    reshaped_prediction = get_adjusted_prediction(
        INTERCEPTS,
        SLOPES,
        predict_year=4,
        reference_sum=18,
        output_shape=TEST_ARR[0].shape,
    )
    assert reshaped_prediction.shape == TEST_ARR[0].shape


def test_adjusted_prediction_content():
    reshaped_prediction = get_adjusted_prediction(
        INTERCEPTS,
        SLOPES,
        predict_year=4,
        reference_sum=18,
        output_shape=TEST_ARR[0].shape,
    )
    assert np.array_equal(np.rint(reshaped_prediction), np.array([
        [4, 5],
        [4, 5],
    ]))


def test_prediction_adjusting():
    sum_to_scale_to = 18*2
    reshaped_prediction = get_adjusted_prediction(
        INTERCEPTS,
        SLOPES,
        predict_year=4,
        reference_sum=sum_to_scale_to,
        output_shape=TEST_ARR[0].shape,
    )
    assert np.array_equal(np.rint(reshaped_prediction), np.array([
        [8, 10],
        [8, 10],
    ]))

