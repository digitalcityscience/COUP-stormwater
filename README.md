# Celery Example

## Description
This sample project shows how to use Celery to process task batches asynchronously. 
For simplicity, the sum of two integers are computed here. In order to simulate the 
complexity, a random duration (3-10 seconds are put on the processing).
Using Celery, this tech stack offers high scalability. For ease of installation, 
Redis is used here. Through Redis the tasks are distributed to the workers and also 
the results are stored on Redis.

Wrapped with an API (Flask), the stack provides an interface for other services. 
The whole thing is then deployed with Docker.

## Design
The task batches are commissioned via a endpoint (```POST, /grouptasks```) (see Usage). 
The client receives a response with a Group-Task-Id and a list of TaskIds. 
Using polling, the client can query the status of the GroupTask 
(```GET, /grouptasks/<grouptask_id>```) or the status of a Task 
(```GET, /tasks/<task_id>```).

## Caching
After a task has been successfully processed, the result is cached on Redis along with 
the input parameters. The result is then returned when a (different) task has the same 
input parameters and is requested.

## TechStack
- Python
- Celery
- Redis
- Flask
- Docker

## Start
1. ```docker-compose build```
2. ```docker-compose up -d```


## Usage
### Create a GroupTask
Request:
```bash
curl -X POST http://localhost:5000/grouptasks -H 'Content-type: application/json' \
    -d '{"tasks": [{"paramB" : 5, "paramA": 1}, {"paramB" : 10, "paramA": 9}, \
    {"paramB" : 13, "paramA": 12}, {"paramB" : 1, "paramA": 8}]}'
```

Response:
```json
{
    "groupTaskId" : "858c8724-03c4-4027-b1e9-4185545aa54d",
    "taskIds" : [
        "55de4727-c7ad-4c5d-9c72-242a6558d65a",
        "12ae3364-f69b-41b9-ad82-c1b8a3e077b8",
        "4012aa3e-d5a0-4654-8290-00537de97eaf",
        "16fbda42-a4c4-4022-b373-e2fc7f13cbcd"
    ]
}
```

### Get GroupTask-Result
Request:
```
curl -X GET http://localhost:5000/grouptasks/858c8724-03c4-4027-b1e9-4185545aa54d
```

**Hint**: This request can be used for polling. The poll abort condition can be set to "groupTaskProcessed != True". 
While processing the results of processed tasks are published in "results" and can be used to display the progress.


Response:
```json
{
    "groupTaskId" : "858c8724-03c4-4027-b1e9-4185545aa54d",
    "grouptaskProcessed" : false,
    "grouptaskSucceeded" : true,
    "results": [
      6,
      19,
      25
    ],
    "tasksCompleted" : 3,
    "tasksTotal" : 5
}
```
### Get single Task-Result
Request:
```
curl -X GET http://localhost:5000/grouptasks/858c8724-03c4-4027-b1e9-4185545aa54d
```
Response:
```json
{
    "result" : 6,
    "resultReady" : true,
    "taskId" : "55de4727-c7ad-4c5d-9c72-242a6558d65a",
    "taskState" : "SUCCESS",
    "taskSucceeded" : true
}
```

## Commands
### Start worker
```celery -A tasks worker --loglevel=info```

### Monitoring Redis

List Tasks:
- ```redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME```

List Queues:
- ```redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*```
