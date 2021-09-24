import time
import requests
import os
import json

cwd = os.getcwd()


class CityPyo:
    """Class to handle CityPyo communication and users
        - Logs in all users listed in config and saves their user ids.
        - Gets data from cityPyo
        - Posts data to cityPyo
    """
    def __init__(self):
        self.url = os.getenv('CITY_PYO', 'http://localhost:5000')
        if not self.url:
            raise Exception("Please specify CITY_PYO environment variable")
        

    # returns subcatchments geojson as dict
    def get_subcatchments(self, user_id):
        subcatchments = self.get_layer_for_user(user_id, "subcatchments")
        if not subcatchments:
            # no subcatchments no calculation :p
            raise FileNotFoundError("could not find subcatchments on %s for user %s" % (self.url, self.user_id))

        return subcatchments
        

    def get_layer_for_user(self, user_id, layer_name, recursive_iteration=0):
        data = {
            "userid": user_id,
            "layer": layer_name
        }

        try:
            response = requests.get(self.url + "/getLayer", json=data)

            if response.status_code == 200:
                return response.json()
            else:
                print("could not get from cityPyo")
                print("wanted to get layer: ", layer_name)
                print("Error code", response.status_code)
                return None
        # exit on request exception (cityIO down)
        except requests.exceptions.RequestException as e:
            print("CityPyo error. " + str(e))

            if recursive_iteration > 10:
                raise requests.exceptions.RequestException

            time.sleep(30 * recursive_iteration)
            recursive_iteration += 1

            return self.get_layer_for_user(user_id, layer_name, recursive_iteration)