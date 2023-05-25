from pathlib import Path
from typing import Iterable

from raster_processing.read import read
from raster_processing.write import write
from raster_processing.merge import create_mosaic
from raster_processing.get_rasters_in_directory import get_rasters_in_directory


def group_and_merge_rasters(
    read_directory: Path, write_directory: Path, group_by: Iterable
):
    """Groups all rasters in a diractory and merges the groups

    Grouping is done based on the raster file names. All names that contain
    a unifying factor are grouped, and each group is merged to form a raster
    mosaic. The mosaics are saved to disk.

    Args:
        read_directory: directory containing the input rasters
        write_directory: directory to write the results to
        group_by: the group by factors

    """
    rasters_to_group = get_rasters_in_directory(read_directory)
    grouped = _group_raster_names(rasters_to_group, group_by)
    _merge_raster_groups(read_directory, write_directory, grouped)


def _group_raster_names(raster_names, group_by_groups):
    grouped = {}
    for group_by in group_by_groups:
        rasters_to_group = []
        for name in raster_names:
            if group_by in name:
                rasters_to_group.append(name)
        grouped[group_by] = rasters_to_group
    return grouped


def _merge_raster_groups(read_directory, write_directory, grouped_rasters):
    for group_name, merge_group in grouped_rasters.items():
        rasters_to_merge = [
            read(Path(read_directory / raster)) for raster in merge_group
        ]
        mosaic, meta = create_mosaic(rasters_to_merge)
        output_path = Path(write_directory / group_name)
        print(f"\nsaving mosaic of: {merge_group}\nto file: {output_path}")
        write(mosaic, meta, output_path)
