import json
import time
from pprint import pprint

import requests

headers = {
    'Content-type': 'application/json',
}

data = json.dumps(
    {
        "tasks": [
            {"paramB": 7, "paramA": 1},
            {"paramB": 11, "paramA": 9},
            {"paramB": 10, "paramA": 12},
            {"paramB": 3, "paramA": 8}
        ]
    }
)

response = requests.post('http://localhost:5000/grouptasks', headers=headers, data=data)

grouptask_id = response.json()['grouptaskId']
print(grouptask_id)

results_completed = False

while not results_completed:
    response = requests.get('http://localhost:5000/grouptasks/{}'.format(grouptask_id)).json()
    pprint(response)
    results_completed = response['grouptaskProcessed']
    time.sleep(1)

print("Fertig!")
