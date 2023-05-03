import numpy as np
import pandas as pd
import rasterio


def raster_to_dataframe(raster: rasterio.DatasetReader, column_name: str):
    xcoords, ycoords = _get_coordinates(raster)
    data_array = raster.read(1)  # assume population rasters -> read a single band

    array_with_coords = np.concatenate((xcoords, ycoords, data_array))
    reshaped = array_with_coords.reshape([3, -1]).T

    dataframe = pd.DataFrame(reshaped, columns=["x", "y", column_name])
    return dataframe


def _get_coordinates(raster):
    height = raster.shape[0]
    width = raster.shape[1]

    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(raster.transform, rows, cols)
    xcoords = np.array(xs)
    ycoords = np.array(ys)
    return xcoords, ycoords
