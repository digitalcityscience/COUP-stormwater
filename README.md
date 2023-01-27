# Celery Example

## Description

Stormwater Simulation using the SWMM engine. 

A cityPyo user provides a subcatchment.geojson that describes the subcatchments of the area. This input is matched with the preconfigured baseline.inp file to describe the subcatchments to swmm.

Further more the simulation request can specify input preset input values like the water flow path and amount of intensive green roofs. 

The draining target of specific subcatchments can be specified in the request like this: "model_updates": [ { "outlet_id": "outfall1", "subcatchment_id": "Sub003" }]

This repository creates the simulation input files for SWMM with the aforementioned inputs.

The result is the runoff values over time for each subcatchment as a geojson.

## Caching

After a task has been successfully processed, the result is cached on Redis along with the input parameters. The result is then returned when a (different) task has the same input parameters and is requested.

## TechStack

- Python
- Celery
- Redis
- Flask
- Docker

## Start

1. ``docker-compose build``
2. ``docker-compose up -d``

## Usage

### Create a Simulation Task

Request:

sh sample_request.sh

Response:

```json
{
  "taskId": "33c3cdb8-a5ea-42d2-996a-97a9f2bc1b7c"
}
```

### Get Task-Result

Request:

```
curl -X GET http://localhost:5001/tasks/33c3cdb8-a5ea-42d2-996a-97a9f2bc1b7c
```

Response:

```json
result	{…}
resultReady	true
taskId	"33c3cdb8-a5ea-42d2-996a-97a9f2bc1b7c"
taskState	"SUCCESS"
taskSucceeded	true
```

#### Result format

Repeating the input rain values troughout the duration of the storm in 5min steps.

The result as geojson containing  the subcatchment areas (multi)polygons, with several properties describing it, plus the runoff results and runoff timestamps as arrays. Math runoff result and its timestamp by array keys. Timestamps in minutes since storm start.

```json
{
"rain": [
      2.9,
      2.9,
      2.9,
      2.9,
      ...
      ],
"geojson": {
	features: [ {
          "geometry": {
            "coordinates": [
              [
                [
                  [
                    10.018143924679784,
                    53.53274191411173
                  ], 
                  ...
                ]
              ]
            ],
            "type": "MultiPolygon"
          },
          "properties": {
            "area_ha": 0.1867,
            "area_m": 1867,
            "area_plann": "planningTopography",
            "building_i": null,
            "city_scope": "S-369",
            "floor_area": null,
            "id": "369",
            "id2": 503.0,
            "land_use_d": "promenade",
            "land_use_g": "publicOS",
            "name_sub": "Sub503",
            "out_1": "outfall1",
            "out_2": "outfall1",
            "out_3": "outfall1",
            "roof_1": null,
            "roof_2": null,
            "runoff_results": {
              "runoff_value": [
                0.07943444699048996,
                0.1913873553276062,
                ...
              ],
              "timestamps": [
                0,
                1
              ]
            },
            "space_id": null,
            "tree_count": 12.0,
            "type_sub": "PT_promenade"
          },
	...
	}
}
```

## Commands

### Start worker

``celery -A tasks worker --loglevel=info``

### Monitoring Redis

List Tasks:

- ``redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME``

List Queues:

- ``redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*``
