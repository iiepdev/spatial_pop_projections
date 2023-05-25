import os
from pathlib import Path


def get_rasters_in_directory(directory: Path):
    """A function to get all raster filenames from a firectory"""
    return [name for name in os.listdir(directory) if name.endswith(".tif")]
