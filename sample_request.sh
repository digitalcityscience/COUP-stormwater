#!/bin/bash

curl -X POST http://localhost:5002/task -H 'Content-type: application/json' \
    -d '{"city_pyo_user": "90af2ace6cb38ae1588547c6c20dcb36", "flow_path":"blockToStreet", "roofs":"intensive", "return_period": 100, "model_updates": [ { "outlet_id": "outfall1", "subcatchment_id": "Sub003" } ]}'