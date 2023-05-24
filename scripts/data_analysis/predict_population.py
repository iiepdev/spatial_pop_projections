import numpy as np


def solve_intercepts_and_slopes(periods, time_series):
    # Format and add one column initialized at 1
    X_mat = np.vstack((np.ones(len(periods)), periods)).T
    # linear regression using matrix-multiplication
    tmp = np.linalg.inv(X_mat.T.dot(X_mat)).dot(X_mat.T)
    intercepts, slopes = tmp.dot(time_series.T)
    return intercepts, slopes


def get_adjusted_prediction(
    intercepts, slopes, predict_year, reference_sum, output_shape
):
    predict_arr = _get_predicted_array(intercepts, slopes, x=predict_year)
    predict_arr = predict_arr.reshape(output_shape)
    adjusted_arr = _adjust_prediction(predict_arr, reference_sum)
    return adjusted_arr


def _get_predicted_array(intercepts, slopes, x):
    return slopes * x + intercepts


def _adjust_prediction(predicted_array, reference_sum):
    predicted_sum = np.nansum(predicted_array)
    multiplier = reference_sum / predicted_sum
    adjusted_arr = np.multiply(predicted_array, multiplier)
    return adjusted_arr
