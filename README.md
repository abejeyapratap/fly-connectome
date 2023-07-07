# Drosophila Hemibrain Connectome

## Setup
1. Install mini-conda from https://docs.conda.io/en/latest/miniconda.html
2. Clone this repo and run the following commands:
3. `cd fly-connectome`
4. `conda env create -f environment.yml`
5. `conda activate neuprint`
6. Install Python and Jupyter extensions in VSCode

### Updated Dependencies
The `environment.yml` file may not contain some of the newest dependencies. Here are the commands used to download them (currently, they are optional):
1. igraph: `conda install -c conda-forge python-igraph`
2. graph-tool: `conda install -c conda-forge graph-tool`
3. NNGT: `pip install --user nngt`
    - Note: Please follow pre-installation instructions at https://nngt.readthedocs.io/en/stable/user/install.html#simple-install

To run any notebook, activate the neuprint kernel in the top right corner.
