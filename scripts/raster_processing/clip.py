from typing import Iterable
import rasterio
from rasterio.mask import mask


def clip(raster: rasterio.io.DatasetReader, geometries: Iterable):
    out_meta = raster.meta.copy()
    out_image, out_transform = mask(raster, geometries, crop=True, all_touched=False)
    out_meta.update(
        {
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
        }
    )
    return out_image, out_meta
