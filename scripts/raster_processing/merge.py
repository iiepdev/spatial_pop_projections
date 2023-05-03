from rasterio.merge import merge


def create_mosaic(rasters: list):
    out_meta = rasters[0].meta.copy()
    mosaic, out_transform = merge(rasters)
    out_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_transform,
        }
    )
    return mosaic, out_meta
