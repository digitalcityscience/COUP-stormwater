import json
import os
import time

import requests
from swmm.toolkit import solver

from swimdock.make_inp_file import make_inp_file
from swimdock.make_result_geojson import get_result_geojson
import swimdock.cityPyo as cp

known_hashes = {}

cwd = os.getcwd()
data_dir = './data/'


# creates an input file from user_input and run the simulation
def perform_swmm_analysis(user_input) -> dict:
    print("making input file")
    make_inp_file(user_input)

    cityPyo = cp.CityPyo() 
    cityPyo.save_subcatchments(user_input["city_pyo_user"])

    print("computing")
    solver.swmm_run('./data/scenario.inp', './data/scenario.rpt', './data/scenario.out')
    time.sleep(1)
    return get_result_geojson()
