import redis
import json
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def cache_get(key):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        return None

def cache_set(key, value, ttl=1800):
    try:
        redis_client.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        pass