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
            {
                "calculation_method": "normal",
                "hash": "yxssz123",
                "model_updates": [
                    {
                        "outlet_id": "J_out19",
                        "subcatchment_id": "Sub000"
                    }
                ],
                "rain_event": {
                    "duration": 120,
                    "return_period": 10
                }
            }
        ]
    }
)

response = requests.post('http://localhost:5000/grouptasks', headers=headers, data=data)

grouptask_id = response.json()['grouptaskId']
print(grouptask_id)

results_completed = False

while not results_completed:
    response = requests.get('http://localhost:5000/grouptasks/{}'.format(grouptask_id)).json()
    # pprint(response)
    results_completed = response['grouptaskProcessed']
    time.sleep(1)

print("Fertig!")
