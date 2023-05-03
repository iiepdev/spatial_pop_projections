import numpy as np


def predict_population(periods, timeseries, year):
    # Format and add one column initialized at 1
    X_mat = np.vstack((np.ones(len(periods)), periods)).T
    # cf formula : linear-regression-using-matrix-multiplication
    tmp = np.linalg.inv(X_mat.T.dot(X_mat)).dot(X_mat.T)
    intercept, slope = tmp.dot(timeseries.T)
    return _get_value_along_line(intercept, slope, x=year)


def _get_value_along_line(intercept, slope, x):
    return slope * x + intercept


# https://stackoverflow.com/questions/59555560/sklearn-linear-regression-for-2d-array
