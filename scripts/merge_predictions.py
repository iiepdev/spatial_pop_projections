from pathlib import Path
from raster_processing.group import group_and_merge_rasters
from raster_processing.get_rasters_in_directory import get_rasters_in_directory


READ_PATH = Path("./data/output/predictions/prefectures/")
WRITE_PATH = Path("./data/output/predictions/togo/")


def main():
    rasters = get_rasters_in_directory(READ_PATH)
    names_without_prefec = [get_filename_without_prefec(raster) for raster in rasters]
    unique_sex_age_year_combinations = set(names_without_prefec)
    group_and_merge_rasters(
        READ_PATH, WRITE_PATH, group_by=unique_sex_age_year_combinations
    )


def get_filename_without_prefec(filename):
    return filename[filename.find("_") + 1 :]


if __name__ == "__main__":
    main()
