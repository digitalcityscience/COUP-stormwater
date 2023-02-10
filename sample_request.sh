#!/bin/bash
# PLEASE SPECIFY YOUR AUTH TOKEN AND CITYPYO USER ID BELOW

curl --location --request POST 'http://localhost:5001/task' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic WU9VUl9JRDpZT1VSX1BBU1NXT1JE' \
--data-raw '{
    "city_pyo_user": "YOUR_CITYPYO_ID",
     "flowPath":"blockToStreet",
     "roofs":"intensive",
     "returnPeriod": 100,
     "model_updates": [ { "outlet_id": "outfall1", "subcatchment_id": "Sub003" }]
     }'