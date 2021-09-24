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


def save_subcatchments(subcatchments_geojson):
    # save geojson with subcatchments to disk
    with open("data/subcatchments.json", "w") as fp:
        json.dump(subcatchments_geojson, fp)


# creates an input file from user_input and run the simulation
def perform_swmm_analysis(calculation_settings, subcatchments) -> dict:
    print("making input file")
    make_inp_file(calculation_settings)
    save_subcatchments(subcatchments)

    print("computing")
    solver.swmm_run('./data/scenario.inp', './data/scenario.rpt', './data/scenario.out')
    time.sleep(1)
    return get_result_geojson()
