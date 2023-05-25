# spatial_pop_projections

This is the methodology used to project spatialized school-age populations
until 2030, based on UN SALB boundaries and WorldPop gridded population
estimates. The projections are adjusted to national population projections, and
then transformed into school-age groups with this [plugin](https://github.com/iiepdev/SSAP-QGIS-plugin)
based on this [methodology](https://github.com/iiepdev/Spatialized-school-age-populations)

The first use case is Togo.


## Developing and running the analysis

The analysis is containerized. The only requirement for running it is a
container engine such as Podman or Docker. You can of course run everything in
an ordinary python virtual environment too, if you prefer it, but the following
instructions assume you are running the container.

To start, spin up a container and attach to it:

```console
docker compose up -d
```
```console
docker attach population-analysis
```

After attaching you can use `python` to run code in the container as you
normally would.

If you want to use jupyter lab from the container, run

```console
invoke jupyter
```

and look for the jupyter url in the output.

Automated tests can be run with:

```console
invoke test
```

and formatting with:

```console
invoke format
```


## Analysis workflow and structure 

All of the analysis components are scripted and found in the `scripts/
` directory. The files meant to be run as scripts are at the top-level of
the directory, while more general-purpose functions used by the scripts are
stored in their respective packages. In addition, a minimal example of the
projection methodology is available as an interactive notebook in `notebooks/
example.ipynb`.

Below are brief descriptions of the main analysis steps, and how to run them.


### Step 1 - download all input data

- Download historical population grids for 2000, 2005, 2010, 2015, 2020 for
  Togo, Ghana, Burkina Faso, and Benin from [Worldpop](https://hub.worldpop.org/geodata/listing?id=30)

- **Result**: Input data stored to their respective directories in the local repository

- Download all input data by running:

```console
python scripts/download_all.py
```


### Step 2 - preprocess data

- Using the [SALB official boundaries](https://salb.un.org/en/data/tgo) for
  Togo, create the official Togo dataset for 2000, 2005, 2010, 2015, 2020.
  - This is done by merging all of the input rasters (all different age, sex and
    year combinations), and then clipping the mosaics with the correct boundaries.

- **Result**: The full Togo historical population grids for 2000, 2005, 2010,
  2015, 2020 by 5-year age groups, with official boundaries.

- Preprocess everything by running:

```console
python scripts/preprocess_all.py
```

- If analysing a country where the worldpop raster boundaries match with the
  interest area the preprocessing step is unecessary.


### Step 3 - project population

- Apply a linear model for each pixel for their population values in 2000-2020.

- Based on the linear change estimated from the 2000-2020 data, project the
  population values for the period 2022-2030.

- Adjust the projections to official population projections. Currently this is
  done on prefecture level, so every prefecture's total predicted population for
  a given year matches the official projection for that year.

- **Result**: Adjusted population estimations for each pixel in each prefecture until 2030.

- Create the prefecture-level projections by running:

```console
python scripts/predict_all.py
```

- Find an interactive axample of how creating one prediction works in
`notebooks/example.ipynb`

### Step 3 - merge projections

- Merge all prefecture-level projections to get the projections for the entire
  Togo (all different age, sex and year combinations).

- **Result**: Finished projections for Togo until 2030.

- Merge predictions by running:

```console
python scripts/merge_predictions.py
```
