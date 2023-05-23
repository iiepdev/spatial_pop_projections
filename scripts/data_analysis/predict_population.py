import numpy as np


def get_adjusted_prediction(
    year,
    observation_timeseries,
    observation_years,
    reference_population,
    output_shape
):
    predict_arr = get_prediction(
        np.array(observation_years), observation_timeseries, year
    )
    predict_arr = predict_arr.reshape(output_shape)
    adjusted_arr = _adjust_to_projection(predict_arr, reference_population)
    return adjusted_arr


def get_prediction(periods, timeseries, year):
    # Format and add one column initialized at 1
    X_mat = np.vstack((np.ones(len(periods)), periods)).T
    # linear regression using matrix-multiplication
    tmp = np.linalg.inv(X_mat.T.dot(X_mat)).dot(X_mat.T)
    intercept, slope = tmp.dot(timeseries.T)
    prediction = _get_value_along_line(intercept, slope, x=year)
    return prediction


def _get_value_along_line(intercept, slope, x):
    return slope * x + intercept


def _adjust_to_projection(predicted_array, reference_value):
    predicted_sum = np.nansum(predicted_array)
    multiplier = reference_value / predicted_sum
    adjusted_arr = np.multiply(predicted_array, multiplier)
    return adjusted_arr
