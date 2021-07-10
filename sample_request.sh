#!/bin/bash


curl -X POST http://localhost:5000/grouptasks \
    -H 'Content-type: application/json' \
    -d '{"tasks": [{"paramB" : 5, "paramA": 1}]}'
