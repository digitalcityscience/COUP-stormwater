# Broker config
redis_host = 'localhost'
redis_port = 6379
redis_pass = 'G0rDkQtRcl!E'
broker_url = 'redis://:{}@{}:{}/0'.format(
    redis_pass,
    redis_host,
    redis_port,
)

# Result config
result_expires = '604800'  # Keep results for 1 week.
result_persistent = True
result_backend = 'redis://:{}@{}:{}/1'.format(
    redis_pass,
    redis_host,
    redis_port,
)
