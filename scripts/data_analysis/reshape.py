import numpy as np


def shape_image_array_to_time_series(image_array: np.ndarray, n_observations: int):
    """Shapes a 3-D array of images to 2D.
    
    Stacks an array of images along its 3rd dimenstion and reshapes the stacked
    array. Each element of the reshaped array contains a time series of values
    of a given pixel in the input 3-D array.

    Args:
        image_array: A 3-D array containing images
        n_observations: The number of observations (the number of images)
    
    Returns:
        time_series: The reshaped array
    """
    stack = np.dstack(image_array)
    time_series = stack.reshape((-1, n_observations))
    return time_series
