from pathlib import Path
from downloading.download import download_from_url
from downloading.worldpop import download_rasters


def main():
    download_rasters(
        countries=["BEN", "BFA", "GHA", "TGO"],
        years=[2000, 2005, 2010, 2015, 2020],
        age_groups=[
            0,
            1,
            5,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
            65,
            70,
            75,
            80,
        ],
        target_directory=Path("./data/input/worldpop_rasters"),
    )

    download_from_url(
        args=[
            "https://geoportal.un.org/arcgis/sharing/rest/content/items/fc0d66dc47114c79abe228ae7e98f973/data",
            Path("./data/input/prefecture_shapes/salb_borders.zip"),
        ]
    )


if __name__ == "__main__":
    main()
