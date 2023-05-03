from os.path import isfile
from typing import Iterable
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import requests


def download_from_url(args: Iterable):
    """Downloads a file from a url and saves it to a file.

    Args:
        args: An iterable containing 2 things: a url to download from and a file
            path to save results to.

    Returns:
        path: The path to the result file.
        None: If the file already exists.
    """
    url, path = args[0], args[1]
    if isfile(path):
        print(f"skipped {path}, already exists")
        return None
    print(f"downloading: {url}")
    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)
    return path


def download_parallel(args: list):
    """downloads files in parallel.

    Args:
        args: A list of iterables. Each iterable should contain 2 things: a url
            to download from and a file path to save results to.
    """
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(download_from_url, args)
    for result in results:
        if result:
            print(f"saved to {result}")
