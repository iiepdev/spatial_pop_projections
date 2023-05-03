import rasterio


def read(path):
    return rasterio.open(path)
