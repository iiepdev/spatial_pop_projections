from downloading.download import download_parallel


# what the urls look like
# https://data.worldpop.org/GIS/AgeSex_structures/Global_2000_2020/2000/TGO/tgo_f_0_2000.tif
# https://data.worldpop.org/GIS/AgeSex_structures/Global_2000_2020/2020/BEN/ben_m_55_2020.tif


BASE_URL = "https://data.worldpop.org/GIS/AgeSex_structures/Global_2000_2020"


def download_rasters(
    countries: list,
    years: list,
    age_groups: list,
    target_directory: str,
):
    urls_with_paths = _get_urls_with_paths(
        countries, years, age_groups, target_directory
    )
    download_parallel(urls_with_paths)


def _get_urls_with_paths(countries, years, age_groups, target_directory):
    urls_with_paths = []
    for country in countries:
        for year in years:
            for age_group in age_groups:
                for sex in ["f", "m"]:
                    filename = _format_filename(country, year, age_group, sex)
                    url = _format_url(country, year, filename)
                    path = _format_path(target_directory, filename)
                    urls_with_paths.append((url, path))
    return urls_with_paths


def _format_filename(country, year, age_group, sex):
    return f"{country.lower()}_{sex}_{age_group}_{year}.tif"


def _format_url(country, year, filename):
    return f"{BASE_URL}/{year}/{country.upper()}/{filename}"


def _format_path(target_directory, filename):
    return f"{target_directory}/{filename}"
