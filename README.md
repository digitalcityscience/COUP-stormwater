# Celery Example

## Description

## TechStack
- Python
- Celery
- Redis
- Flask
- Docker

## Getting Started
1. ```docker-compose up -d```




## Commands
### Start worker
```celery -A tasks worker --loglevel=info```

### Monitoring Redis

List Tasks:
- ```redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME```

List Queues:
- ```redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*```
