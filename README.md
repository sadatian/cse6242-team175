# Crime and Settlement <br/> <sup>Chicago Crime Clustering and Real Estate Value</sup>
## [CSE6242 - Team 175](https://github.com/sadatian/cse6242-team175/)

## Overview
In this project we've developed an interactive presentation of the crime data in the city of Chicago for (2010-2020). This project was designed to showcase two novel techniques:  
&nbsp;&nbsp; [1.](https://github.com/sadatian/cse6242-team175/tree/main/data) Use of VRAM (GPU memory) and *embarrassingly parallel* approach for processing big data using [RAPIDS](https://rapids.ai/). </br>
&nbsp;&nbsp; [2.](https://github.com/sadatian/cse6242-team175/blob/main/crime_clustering.py) GMM clustering sped up by a K-Means hybrid-step.

## Demo
Basic Functionality  
![demo1](https://github.com/sadatian/cse6242-team175/blob/main/residuals/demo1.gif)

## Prerequisites
### Data
Please make sure the data prerequisites are met by following instructions presented in the `README.md` file [here](https://github.com/sadatian/cse6242-team175/tree/main/data).
### Tokens
Please obtain Google API and Mapbox API keys and place them in their approperiate files `*-token.txt` within the `tokens` folder.
### Environment
Run the following code in terminal and use the `chicago` kernel to run the [`main.ipynb`](https://github.com/sadatian/cse6242-team175/blob/main/main.ipynb) notebook:
```
conda create -n chicago -c conda-forge python==3.8 -y;
conda activate chicago;
pip install -r requirements.txt
```
As long as you have the `nb_conda_kernels` package installed in your Jupyter environment, you should be able to access `chicago` kernel inside the Jupyter. We recommend using JupyterLab instead of Jupyter Notebook.


## Team
**Barsotz Bak**  
**Jacob Bigham**  
**Robert Clark**  
**Dan Sadatian**  
**Elliot Wright**
