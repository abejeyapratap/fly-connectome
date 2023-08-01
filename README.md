# Drosophila Hemibrain Connectome

This research project is based on the dataset provided by Google Research and the FlyEM team at Janelia Research Campus. The dataset is a connectome of the Drosophila brain, which is a map of all the neurons and their connections, available at https://www.janelia.org/project-team/flyem/hemibrain.

For more information about the dataset: https://ai.googleblog.com/2020/01/releasing-drosophila-hemibrain.html

## Setup
1. Install mini-conda from https://docs.conda.io/en/latest/miniconda.html
2. Clone this repo and run the following commands:
3. `cd fly-connectome`
4. `conda env create -f environment.yml`
5. `conda activate neuprint`
6. Install Python and Jupyter extensions in VSCode

### Updated Dependencies
The `environment.yml` file may not contain some of the newest dependencies. Here are the commands used to download them (currently, they are all optional except for seaborn):
1. igraph: `conda install -c conda-forge python-igraph`
2. graph-tool: `conda install -c conda-forge graph-tool`
3. NNGT: `pip install --user nngt`
    - Note: Please follow pre-installation instructions at https://nngt.readthedocs.io/en/stable/user/install.html#simple-install
4. seaborn: `conda install seaborn`

To run any notebook, activate the neuprint kernel in the top right corner.
