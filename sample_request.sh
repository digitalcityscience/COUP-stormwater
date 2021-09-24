#!/bin/bash

curl -X POST http://localhost:5002/task -H 'Content-type: application/json' \
    -d '{"city_pyo_user": "90af2ace6cb38ae1588547c6c20dcb36", "model_updates": [ { "outlet_id": "J_out19", "subcatchment_id": "Sub000" } ], "rain_event": { "duration": 120, "return_period": 10 }}'