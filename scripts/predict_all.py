from pathlib import Path
import rasterio
import numpy as np
import geopandas as gpd
import pandas as pd

from raster_processing.clip import clip
from data_analysis.get_reference_population import get_reference_population
from data_analysis.normalize_string import normalize_input_strings
from data_analysis.predict_population import (
    solve_intercepts_and_slopes,
    get_adjusted_prediction,
)
from data_analysis.reshape import shape_image_array_to_time_series


AGE_GROUPS = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
OBSERVATION_YEARS = [2000, 2005, 2010, 2015, 2020]
PREDICTION_YEARS = [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

INPUT_RASTER_DIRECTORY = Path("./data/output/population_grids_togo/")
OUTPUT_RASTER_DIRECTORY = Path(f"./data/output/predictions/prefectures/")

PREFECTURES = gpd.read_file(Path("./data/input/borders/togo/salb_borders.zip"))
PREFECTURE_NAME_COLUMN = "adm2nm"

REFERENCE_PROJECTIONS = pd.read_excel(
    Path("./data/input/population_projections/Project_Prefect_INSEED.xlsx"),
    sheet_name=None,
    skiprows=141,  # We dont want lomé-specific data
    usecols=[0, 1, 2],  # We just need the age, m, f columns
)


def main():
    normalize_input_strings(
        REFERENCE_PROJECTIONS, PREFECTURES, prefec_name_col=PREFECTURE_NAME_COLUMN
    )
    for prefec_name in PREFECTURES[PREFECTURE_NAME_COLUMN].values:
        prefec_shape = PREFECTURES.loc[
            PREFECTURES[PREFECTURE_NAME_COLUMN] == prefec_name
        ]
        for age_group in AGE_GROUPS:
            for sex in ["m", "f"]:
                images, meta = get_input_rasters(
                    sex,
                    age_group,
                    OBSERVATION_YEARS,
                    INPUT_RASTER_DIRECTORY,
                    area=prefec_shape,
                )
                time_series = shape_image_array_to_time_series(
                    images, n_observations=len(OBSERVATION_YEARS)
                )
                intercepts, slopes = solve_intercepts_and_slopes(
                    periods=OBSERVATION_YEARS,
                    time_series=time_series,
                )
                for year in PREDICTION_YEARS:
                    reference_population = get_reference_population(
                        REFERENCE_PROJECTIONS,
                        prefec_name,
                        year,
                        age_group,
                        sex,
                    )
                    adjusted_prediction = get_adjusted_prediction(
                        intercepts,
                        slopes,
                        predict_year=year,
                        reference_sum=reference_population,
                        output_shape=images[0].shape,  # all images have same shape
                    )
                    out_path = format_filepath(
                        OUTPUT_RASTER_DIRECTORY, sex, age_group, year, prefec_name
                    )
                    save_to_raster(out_path, adjusted_prediction, meta)


def get_input_rasters(sex, age_group, observation_years, directory, area):
    raster_names = get_raster_names(sex, age_group, observation_years)
    images, meta = read_rasters_to_array(
        raster_names,
        directory,
        age_group,
        area,
    )
    return images, meta


def get_raster_names(sex, age_group, years):
    raster_names = [f"{sex}_{age_group}_{year}.tif" for year in years]
    if age_group == 0:
        raster_names = zip(raster_names, [f"{sex}_1_{year}.tif" for year in years])
    return raster_names


def read_rasters_to_array(raster_names, directory, age_group, area):
    if age_group == 0:
        images = []
        for name_tuple in raster_names:
            images_to_sum, meta = read_and_clip_rasters_to_list(
                name_tuple, directory, area
            )
            summed = images_to_sum[0] + images_to_sum[1]
            images.append(summed)
    else:
        images, meta = read_and_clip_rasters_to_list(raster_names, directory, area)
    images = np.array(images)
    images[images < 0] = np.nan
    return images, meta


def read_and_clip_rasters_to_list(raster_names, directory, region):
    images = []
    for name in raster_names:
        with rasterio.open(Path(directory / name)) as raster:
            image, meta = clip(raster, region.geometry)
            images.append(image[0])
    return images, meta


def format_filepath(directory, sex, age_group, year, region):
    filename = f"{region}_{sex}_{age_group}_{year}.tif"
    path = Path(directory / filename)
    return path


def save_to_raster(path, image, meta):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",  # output file type
        height=image.shape[0],  # shape of array
        width=image.shape[1],
        count=1,  # number of bands
        dtype=image.dtype,  # output datatype
        crs="+proj=latlong",  # CRS
        transform=meta["transform"],  # location and resolution of upper left cell
        nodata=np.nan,  # nans to nodata
    ) as dst:
        # write single band
        dst.write(image, 1)
        print(f"saved to {path}")


if __name__ == "__main__":
    main()
