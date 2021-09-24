from celery import group
from celery.result import GroupResult
import json
import hashlib
import re

import swimdock.cityPyo as cp
from swimdock.main import perform_swmm_analysis

cityPyo = cp.CityPyo() ## put cityPyo container here

def calculate_and_return_result(scenario, subcatchments):
    return perform_swmm_analysis(scenario, subcatchments)


def get_calculation_input(complex_task):
    # hash noise scenario settings
    calculation_settings = get_calculation_settings(complex_task)
    scenario_hash = hash_dict(calculation_settings)

    # hash subcatchments geojson
    subcatchments = get_subcatchments_geojson_from_cityPyo(complex_task["city_pyo_user"])
    subcatchments_hash = hash_dict(subcatchments)

    return scenario_hash, subcatchments_hash, calculation_settings, subcatchments


def get_calculation_settings(scenario):
    print("scenario", scenario)

    return {
        "model_updates": scenario["model_updates"],
        "rain_event": scenario["rain_event"]
    }


def get_subcatchments_geojson_from_cityPyo(cityPyo_user_id):
    return cityPyo.get_subcatchments(cityPyo_user_id)


def hash_dict(dict_to_hash):
    dict_string = json.dumps(dict_to_hash, sort_keys=True)
    hash_buildings = hashlib.md5(dict_string.encode())

    return hash_buildings.hexdigest()


def is_valid_md5(checkme):
    if type(checkme) == str:
        if re.findall(r"([a-fA-F\d]{32})", checkme):
            return True

    return False


def get_cache_key(**kwargs):
    return kwargs["scenario_hash"] + "_" + kwargs["subcatchments_hash"]

