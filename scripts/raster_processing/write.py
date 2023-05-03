import rasterio


def write(dataset, out_meta, path):
    with rasterio.open(path, "w", **out_meta) as file:
        file.write(dataset)
