from pathlib import Path
from typing import Iterable

from raster_processing.read import read
from raster_processing.write import write
from raster_processing.merge import create_mosaic
from raster_processing.get_rasters_in_directory import get_rasters_in_directory


def group_and_merge_rasters(
    read_directory: Path, write_directory: Path, group_by: Iterable
):
    rasters_to_group = get_rasters_in_directory(read_directory)
    grouped = _group_rasters(rasters_to_group, group_by)
    _merge_raster_groups(read_directory, write_directory, grouped)


def _group_rasters(all_rasters, group_by_groups):
    grouped = {}
    for combination in group_by_groups:
        rasters_to_group = []
        for name in all_rasters:
            if combination in name:
                rasters_to_group.append(name)
        grouped[combination] = rasters_to_group
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
