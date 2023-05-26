import os
from pathlib import Path
import geopandas as gpd
from raster_processing.read import read
from raster_processing.write import write
from raster_processing.clip import clip
from raster_processing.merge import create_mosaic
from raster_processing.get_rasters_in_directory import get_rasters_in_directory
from raster_processing.group import group_and_merge_rasters


def main():
    create_all_mosaics()
    clip_all_mosaics()


def create_all_mosaics():
    READ_PATH = Path("./data/input/worldpop_rasters/")
    WRITE_PATH = Path("./data/output/mosaics/")

    filenames = get_rasters_in_directory(READ_PATH)
    names_without_country = [get_filename_without_country(name) for name in filenames]
    unique_sex_age_year_combinations = set(names_without_country)

    group_and_merge_rasters(
        READ_PATH, WRITE_PATH, group_by=unique_sex_age_year_combinations
    )


def clip_all_mosaics():
    SHAPES_PATH = Path("./data/input/prefecture_shapes/salb_borders.zip")
    MOSAICS_PATH = Path("./data/output/mosaics/")
    WRITE_PATH = Path("./data/output/clipped_population_grids/")

    shapes = gpd.read_file(SHAPES_PATH).geometry
    filenames = get_rasters_in_directory(MOSAICS_PATH)

    for name in filenames:
        path = Path(MOSAICS_PATH / name)
        with read(path) as raster:
            image, meta = clip(raster, shapes)
            out_path = Path(WRITE_PATH / name)
            print(f"saving to {out_path}")
            write(image, meta, out_path)


def get_filename_without_country(filename):
    return filename[4:]


if __name__ == "__main__":
    main()
