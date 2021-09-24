#!/bin/bash

curl -X POST http://localhost:5002/grouptasks -H 'Content-type: application/json' \
    -d '{"tasks": [ {"city_pyo_user": "90af2ace6cb38ae1588547c6c20dcb36", "calculation_method": "normal", "hash": "yxz123", "model_updates": [ { "outlet_id": "J_out19", "subcatchment_id": "Sub000" } ], "rain_event": { "duration": 120, "return_period": 10 } } ]}'