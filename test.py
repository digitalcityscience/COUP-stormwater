from pprint import pprint

from swimdock.main import perform_swmm_analysis

input = {
    "calculation_method": "normal",
    "hash": "yxz123",
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
pprint(perform_swmm_analysis(input))
