# Drosophila Hemibrain Connectome

## Background
This research project is based on the dataset provided by Google Research and the FlyEM team at Janelia Research Campus. The dataset is a connectome of the Drosophila brain, which is a map of all the neurons and their connections, available at https://www.janelia.org/project-team/flyem/hemibrain. From a graph theory perspective, the dataset is a very large graph of ~25,000 nodes (neurons) and 20+ million edges (connections).

For more information about the dataset: https://ai.googleblog.com/2020/01/releasing-drosophila-hemibrain.html

## Contribution
Researchers at Drexel's Biomedical Engineering department and College of Medicine are studying the escape behavior of a fly when there's a looming stimulus. They have identified 10-12 neurons that play an important role in these looming response circuits of the brain (i.e., they have identified certain nodes in the graph that play an important role in its surrounding network).

We attempt to identify other interesting neurons connected to the identified ones and also find clusters/sub-networks of neurons that play a role in the escape behavior. We do this using graph clustering algorithms (i.e., Louvain) and a greedy algorithm called consensus clustering. We also conducted statistical analyses (i.e., ANOVA) to demonstrate the validity of our findings.

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
