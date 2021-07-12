import json

import redis

import config


class Cache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=config.redis_host,
            port=config.redis_port,
            password=config.redis_pass,
        )

    def save(self, key: str, value: dict):
        self.redis_client.set(key, json.dumps(value))

    def retrieve(self, key: str) -> dict:
        result = self.redis_client.get(key)
        if result is None:
            return {}

        return json.loads(result)
