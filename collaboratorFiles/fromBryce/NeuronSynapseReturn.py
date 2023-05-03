# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 23:04:19 2023

@author: madis
"""
import neuprint
from neuprint import Client
from neuprint import fetch_adjacencies, NeuronCriteria as NC, SynapseCriteria as SC
from neuprint import fetch_roi_hierarchy, fetch_synapse_connections, fetch_neurons, fetch_shortest_paths, fetch_simple_connections

import numpy as np
import pandas as pd
import time

import bokeh
import bokeh.palettes
from bokeh.plotting import figure, show, output_notebook
from pandas import ExcelWriter
import networkx as nx
import matplotlib.pyplot as plt

# %matplotlib inline

# Establish client
c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1' ,token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJyeWNlaGluYUBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS8tU3U4SUdNeHlGRzQvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbjdtY0hTdWFSeXljWVNTaWpMT25KbXlNN3ZLZy9zOTYtYy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE4MDQ5ODkzMjd9.0IearuWh8pVLWARTPB6UJGa0sBY8ZtyMEn1kFmYVmS8')
c.fetch_version()



def NeuronSynapseReturn():
    Connection_Info = []
    Connection_Info_2 = []
    NeuronToSearch = input("What neuron would you like synapse information for?: ")
    Connection_Info,Connection_Info_2 = fetch_adjacencies(targets=NC(type = NeuronToSearch),include_nonprimary = True)
    FinalSheet = pd.concat([Connection_Info,Connection_Info_2], axis=1)
    Excel_Response = input("Would you like this data exported to excel?: ")
    if Excel_Response == "Yes" or Excel_Response == "yes":
        Path_Response = input("Please input the path that you would like the data stored at: ") + "\\"
        Excel_Sheet_Name = input("Please indicate the name of the file that you would like (without .xlsx): ")
        Full_Path = Path_Response + Excel_Sheet_Name + '.xlsx'
        FinalSheet.to_excel(Full_Path, index = False)
    return FinalSheet