# Crime Data ETL

You must run the [`clean-data.ipynb`](https://github.com/sadatian/cse6242-team175/blob/main/data/clean-data.ipynb) notebook in this folder in order to obtain the proper data for the main project. Consider this directory ([data](https://github.com/sadatian/cse6242-team175/tree/main/data)) as root for the purpose of instructions in this ETL. 

## Prerequisites
#### Hardware
Due to use of RAPIDS in this part of the project you must run this notebook on a system with at least one [CUDA GPU](https://www.nvidia.com/en-us/geforce/technologies/cuda/supported-gpus/). 
#### Software
This notebook was developed and tested on WSL2 Ubuntu 18.04 within the following conda environment:
```
conda create -n rapids -c rapidsai -c nvidia -c conda-forge \
    cudf=0.18.1 cudnn=8.0.0 python=3.8 pandas=1.1.5 geopandas=0.8.1 cudatoolkit=11.0
```
#### Data
Historical crime data of the City of Chicago for all crimes recorded from 2001 to present must be downloaded from [Chicago Data Portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2) as CSV into the root directory and renamed to `crime_big.csv`. Please note the file is ~1.7 GB.
## Process
Given all prerequisites are satisfied, you should be able to open the [`clean-data.ipynb`](https://github.com/sadatian/cse6242-team175/blob/main/data/clean-data.ipynb) notebook in JupyterLab and run it with `rapids` kernel and obtain the necessary `crime-clean.csv` for the main project. 
