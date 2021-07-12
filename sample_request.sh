#!/bin/bash

curl -X POST http://localhost:5000/grouptasks -H 'Content-type: application/json' \
    -d '{"tasks": [{"paramB" : 5, "paramA": 1}, {"paramB" : 10, "paramA": 9}, {"paramB" : 13, "paramA": 12}, {"paramB" : 1, "paramA": 8}]}'
