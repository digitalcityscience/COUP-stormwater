import json
import os
import time
import pandas as pd

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


# reads the relevant rain_data file for the calculation settings and returns the rain data as list
# I did try to read it directly from the scenario.inp/out/rpt files instead, 
def get_rain_for_calc_settings(return_period):
    
    """ 
    example timeseries file
    SWIMM needs this format. 

    ;;[TIMESERIES]
    ;;Name YY MM DD HH mm Value
    ;;---- -- -- -- -- -- -----
    2-yr 2021 01 01 00 00 1.143
    2-yr 2021 01 01 00 05 1.143
    """

    df =  pd.read_csv(
        "data/rain_data/timeseries_" + str(return_period) + ".txt",  # get file for return period
        header=1, # set row 1 as header
        delimiter=" ", # delimiter is space
        skiprows=[2] # ignore row number 2 
    )

    return df["Value"].to_list()  # the rain amounts are in the column "Value"



# creates an input file from user_input and run the simulation
def perform_swmm_analysis(calculation_settings, subcatchments) -> dict:
    print("making input file")
    make_inp_file(calculation_settings)
    save_subcatchments(subcatchments)

    print("computing")
    solver.swmm_run('./data/scenario.inp', './data/scenario.rpt', './data/scenario.out')
    time.sleep(1)
    return {
        "rain": get_rain_for_calc_settings(calculation_settings["return_period"]),
        "geojson": get_result_geojson()
        }



def test(): 

    with open("data/subcatchments.json", "r") as f:
        subcatchment_json = json.load(f)


    test_data = {
        "city_pyo_user": "90af2ace6cb38ae1588547c6c20dcb36",
        "flow_path":"blockToPark",
        "roofs":"extensive",
        "return_period": 2,
        "model_updates": []
    }

    perform_swmm_analysis(test_data, subcatchment_json)


