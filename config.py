import os

# Available configs:
# https://docs.celeryproject.org/en/stable/userguide/configuration.html#new-lowercase-settings

# Redis config
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_pass = os.getenv('REDIS_PASS', 'G0rDkQtRcl!E')

broker_url = 'redis://:{}@{}:{}/0'.format(
    redis_pass,
    redis_host,
    redis_port,
)

# Worker config
worker_concurrency = 10

# Result config
result_expires = '604800'  # Keep results for 1 week.
result_persistent = True
result_backend = 'redis://:{}@{}:{}/1'.format(
    redis_pass,
    redis_host,
    redis_port,
)

enable_utc = True
